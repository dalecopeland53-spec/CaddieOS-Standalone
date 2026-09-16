from pathlib import Path
import re

p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD90_GPS_TARGET_DIAGNOSTIC' not in s:
    marker='const BUILD89_GPS_FEED_STATUS_FIX=true;'
    if marker not in s: raise SystemExit('Build 89 marker missing')
    s=s.replace(marker,marker+'\nconst BUILD90_GPS_TARGET_DIAGNOSTIC=true;',1)

# Show the two inputs that must exist before a distance can be calculated.
# This does not use fake coordinates and does not change course/map selection.
needle="targetDistances={front:gp&&currentTarget.front?haversine(gp,currentTarget.front,units):null,center:gp&&currentTarget.center?haversine(gp,currentTarget.center,units):null,back:gp&&currentTarget.back?haversine(gp,currentTarget.back,units):null};"
replacement=needle+"const build90GpsOk=!!gp,build90TargetOk=!!currentTarget.center,build90Diagnostic=`GPS FIX ${build90GpsOk?'✓':'✗'} · HOLE TARGET ${build90TargetOk?'✓':'✗'}`;"
if needle not in s: raise SystemExit('Build 86 target-distance anchor missing')
s=s.replace(needle,replacement,1)

# Put the diagnostic into the existing Round header subtitle; no layout redesign.
old="sub={gpsLive?`LIVE GPS${gps?.acc?` · ±${gps.acc} m`:''}`:'GPS ready when you are'}"
new="sub={`${build90Diagnostic}${gps?.acc?` · ±${gps.acc} m`:''}`}"
if old not in s: raise SystemExit('Round GPS subtitle anchor missing')
s=s.replace(old,new,1)

# Replace misleading fallback wording where present. The diagnostic above tells us
# whether GPS or real hole coordinates are the missing half.
s=s.replace("'Start live GPS'","(!build90GpsOk?'Waiting for GPS signal':!build90TargetOk?'Loading hole coordinates':'Live GPS ready')")
s=s.replace('"Start live GPS"',"(!build90GpsOk?'Waiting for GPS signal':!build90TargetOk?'Loading hole coordinates':'Live GPS ready')")

p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 90',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.90\"',t,count=1);g.write_text(t)
print('Build 90 GPS + hole target diagnostic applied')
