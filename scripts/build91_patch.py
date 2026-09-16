from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
marker='const BUILD90_GPS_TARGET_DIAGNOSTIC=true;'
if marker in s and 'BUILD91_LIVE_COURSE_CHAIN' not in s:
    s=s.replace(marker,marker+'\nconst BUILD91_LIVE_COURSE_CHAIN=true;',1)
# Harden haversine exactly as supplied: reject incomplete coordinate objects.
s=re.sub(r"function haversine\(a,b,u\)\{if\(!a\|\|!b\)return null;", "function haversine(a,b,u){if(!a||!b||!a.lat||!a.lon||!b.lat||!b.lon)return null;", s, count=1)
# Replace the inline target chain with memoized live front/centre/back distances and feed centre into Caddie distance.
old=r"const idx=Math\.min\(17,Math\.max\(0,n\(hole\)-1\)\),currentTarget=targets\[idx\],gp=gps\?\{lat:Number\(gps\.lat\),lon:Number\(gps\.lon\)\}:null,targetDistances=\{front:haversine\(gp,currentTarget\?\.front,units\),center:haversine\(gp,currentTarget\?\.center,units\),back:haversine\(gp,currentTarget\?\.back,units\)\};"
new="const idx=Math.min(17,Math.max(0,n(hole)-1)),currentTarget=targets[idx],gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null;\n const targetDistances=useMemo(()=>({front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)}),[gps?.lat,gps?.lon,currentTarget,units]);\n const isGpsFix=!!(gps?.lat&&gps?.lon),isHoleTargetValid=!!(currentTarget?.center?.lat&&currentTarget?.center?.lon);\n useEffect(()=>{if(targetDistances.center!==null)setDistance(String(targetDistances.center))},[targetDistances.center]);"
s,n=re.subn(old,new,s,count=1)
if not n: raise SystemExit('Build 91 live target chain anchor missing')
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 91',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.91\"',t,count=1);g.write_text(t)
print('Build 91 supplied Live Course GPS chain applied')
