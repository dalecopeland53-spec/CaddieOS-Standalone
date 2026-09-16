from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
marker='const BUILD90_GPS_TARGET_DIAGNOSTIC=true;'
if marker in s and 'BUILD91_LIVE_COURSE_CHAIN' not in s:
    s=s.replace(marker,marker+'\nconst BUILD91_LIVE_COURSE_CHAIN=true;',1)
# Harden haversine: reject incomplete coordinate objects.
s=re.sub(r"function haversine\(a,b,u\)\{if\(!a\|\|!b\)return null;", "function haversine(a,b,u){if(!a||!b||!a.lat||!a.lon||!b.lat||!b.lon)return null;", s, count=1)
# Apply supplied live target chain to Shell, where setDistance exists.
shell_old="const idx=Math.min(17,Math.max(0,n(hole)-1)),currentTarget=targets[idx],gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null,targetDistances={front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)};"
shell_new="const idx=Math.min(17,Math.max(0,n(hole)-1)),currentTarget=targets[idx],gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null;const targetDistances=useMemo(()=>({front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)}),[gps?.lat,gps?.lon,currentTarget,units]);const isGpsFix=!!(gps?.lat&&gps?.lon),isHoleTargetValid=!!(currentTarget?.center?.lat&&currentTarget?.center?.lon);useEffect(()=>{if(targetDistances.center!==null)setDistance(String(targetDistances.center))},[targetDistances.center]);"
if shell_old in s:s=s.replace(shell_old,shell_new,1)
# Round has its own API/OpenGolf target chain. Keep it hook-free: setDistance is Shell state and is not guaranteed in Round props.
round_old="targetDistances={front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null};"
if round_old not in s: raise SystemExit('Build 91 real live target chain anchor missing')
round_new="targetDistances={front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null};const isGpsFix=!!gp,isHoleTargetValid=!!currentTarget.center;"
s=s.replace(round_old,round_new,1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 91',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.91\"',t,count=1);g.write_text(t)
print('Build 91 Live Course chain applied without Round startup hook crash')
