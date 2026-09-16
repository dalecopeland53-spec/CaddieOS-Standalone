from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD85_LIVE_COURSE' not in s:s=s.replace('const BUILD84_ACTIVE_COURSE_FIX=true;','const BUILD84_ACTIVE_COURSE_FIX=true;\nconst BUILD85_LIVE_COURSE=true;',1)
# OpenGolf gives us the selected course; OpenStreetMap supplies mapped golf-hole ways.
# Convert each real OSM hole way into a real green-centre GPS target so Round distance,
# club selection and Caddie advice use the golfer's moving phone position.
anchor=" useEffect(()=>{let mounted=true;cachedOpenGolfCourse()"
effect=""" useEffect(()=>{let alive=true;const c=realCourse?.course||realCourse||{},lat=Number(c.latitude??c.lat??c.location?.lat??c.coordinates?.lat),lon=Number(c.longitude??c.lon??c.lng??c.location?.lon??c.location?.lng??c.coordinates?.lon??c.coordinates?.lng);if(!Number.isFinite(lat)||!Number.isFinite(lon))return()=>{alive=false};const q=`[out:json][timeout:18];way(around:3000,${lat},${lon})[\"golf\"=\"hole\"];out geom;`;fetch('https://overpass-api.de/api/interpreter',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'data='+encodeURIComponent(q)}).then(r=>r.ok?r.json():Promise.reject()).then(j=>{if(!alive)return;const ways=(j?.elements||[]).filter(x=>x.type==='way'&&Array.isArray(x.geometry)&&x.geometry.length>1),next={};ways.forEach((w,k)=>{const raw=String(w.tags?.ref??w.tags?.hole??w.tags?.name??''),m=raw.match(/(?:^|\\D)(1[0-8]|[1-9])(?:\\D|$)/),hn=m?Number(m[1]):null;if(!hn)return;const g=w.geometry,last=g[g.length-1];if(last&&Number.isFinite(Number(last.lat))&&Number.isFinite(Number(last.lon)))next[hn]={lat:Number(last.lat),lon:Number(last.lon)}});if(Object.keys(next).length)setTargets(a=>a.map((x,i)=>next[i+1]?{...x,center:next[i+1]}:x))}).catch(()=>{});return()=>{alive=false}},[realCourse]);\n"""
if 'overpass-api.de/api/interpreter' not in s:
 pos=s.find(anchor)
 if pos<0:raise SystemExit('Build85 startup effect anchor missing')
 s=s[:pos]+effect+s[pos:]
# Start live GPS when a genuine course is active. Permission handling stays in existing startLiveGPS.
round_anchor="function Round("
m=re.search(r"function Round\([^)]*\)\{",s)
if not m:raise SystemExit('Build85 Round missing')
if 'BUILD85_AUTOGPS' not in s:
 insert="const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse&&!gpsLive)startLiveGPS?.()},[realCourse]);"
 s=s[:m.end()]+insert+s[m.end():]
# Never label generated fallback art as live mapped geometry.
s=s.replace('OpenGolfAPI · OpenStreetMap</MiniText>','LIVE COURSE · OpenStreetMap</MiniText>',1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 85',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.85\"',t,count=1);g.write_text(t)
print('Build 85 live course targets + automatic live GPS applied')
