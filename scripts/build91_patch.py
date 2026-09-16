from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
marker='const BUILD90_GPS_TARGET_DIAGNOSTIC=true;'
if marker in s and 'BUILD91_LIVE_COURSE_CHAIN' not in s:
    s=s.replace(marker,marker+'\nconst BUILD91_LIVE_COURSE_CHAIN=true;',1)
# Harden haversine: reject incomplete coordinate objects.
s=re.sub(r"function haversine\(a,b,u\)\{if\(!a\|\|!b\)return null;", "function haversine(a,b,u){if(!a||!b||!a.lat||!a.lon||!b.lat||!b.lon)return null;", s, count=1)
# Build 86/90 actual Live Course chain includes API course targets and gp guards.
needle="targetDistances={front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null};"
if needle not in s: raise SystemExit('Build 91 real live target chain anchor missing')
replacement="targetDistances=useMemo(()=>({front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null}),[gps?.lat,gps?.lon,currentTarget?.front?.lat,currentTarget?.front?.lon,currentTarget?.center?.lat,currentTarget?.center?.lon,currentTarget?.back?.lat,currentTarget?.back?.lon,units]);const isGpsFix=!!gp,isHoleTargetValid=!!currentTarget.center;useEffect(()=>{if(targetDistances.center!==null)setDistance(String(targetDistances.center))},[targetDistances.center]);"
s=s.replace(needle,replacement,1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 91',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.91\"',t,count=1);g.write_text(t)
print('Build 91 supplied Live Course GPS chain applied')
