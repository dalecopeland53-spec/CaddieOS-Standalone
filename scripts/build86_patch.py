from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD86_LIVE_TARGET_FIX' not in s:
 s=s.replace('const BUILD85_LIVE_COURSE=true;','const BUILD85_LIVE_COURSE=true;\nconst BUILD86_LIVE_TARGET_FIX=true;',1)
# Build 85 referenced realCourse inside Round without guaranteeing it was in Round's props.
m=re.search(r'function Round\(([^)]*)\)\{',s)
if not m: raise SystemExit('Build86 Round signature missing')
props=m.group(1)
if 'realCourse' not in props:
 newprops=props.rstrip()+',realCourse'
 s=s[:m.start(1)]+newprops+s[m.end(1):]
# Make target calculation resilient: prefer imported OpenGolf targets, then API hole coordinates.
old="const idx=Math.min(17,Math.max(0,n(hole)-1)),apiHole=openGolfHoleContext(realCourse,idx+1),coord=v=>{if(!v)return null;const lat=Number(v.lat??v.latitude),lon=Number(v.lon??v.lng??v.longitude);return Number.isFinite(lat)&&Number.isFinite(lon)?{lat,lon}:null},rawHole=apiHole.raw||{},apiTarget={front:coord(rawHole.front||rawHole.green_front||rawHole.front_coordinate),center:coord(rawHole.center||rawHole.green_center||rawHole.center_coordinate||rawHole.green),back:coord(rawHole.back||rawHole.green_back||rawHole.back_coordinate)},currentTarget={...targets[idx],front:apiTarget.front||targets[idx]?.front,center:apiTarget.center||targets[idx]?.center,back:apiTarget.back||targets[idx]?.back},gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null,targetDistances={front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)};"
new="const idx=Math.min(17,Math.max(0,(typeof n==='function'?n(hole):Number(hole))-1)),apiHole=openGolfHoleContext(realCourse,idx+1),coord=v=>{if(!v)return null;const lat=Number(v.lat??v.latitude),lon=Number(v.lon??v.lng??v.longitude);return Number.isFinite(lat)&&Number.isFinite(lon)?{lat,lon}:null},rawHole=apiHole?.raw||{},apiTarget={front:coord(rawHole.front??rawHole.green_front??rawHole.front_coordinate),center:coord(rawHole.center??rawHole.green_center??rawHole.center_coordinate??rawHole.green),back:coord(rawHole.back??rawHole.green_back??rawHole.back_coordinate)},baseTarget=targets&&targets[idx]?targets[idx]:{},currentTarget={...baseTarget,front:apiTarget.front??baseTarget.front??null,center:apiTarget.center??baseTarget.center??null,back:apiTarget.back??baseTarget.back??null},gp=gps&&Number.isFinite(Number(gps.lat))&&Number.isFinite(Number(gps.lon))?{lat:Number(gps.lat),lon:Number(gps.lon)}:null,targetDistances={front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null};"
if old in s:s=s.replace(old,new,1)
# Build 85 auto-GPS effect must depend on the actual shared course prop and avoid repeat starts.
s=s.replace("const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse&&!gpsLive)startLiveGPS?.()},[realCourse]);","const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse&&!gpsLive)startLiveGPS?.()},[realCourse,gpsLive]);",1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 86',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.86\"',t,count=1);g.write_text(t)
print('Build 86 Round realCourse + safe live target fix applied')
