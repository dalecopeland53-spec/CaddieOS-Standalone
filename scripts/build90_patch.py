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

# Round subtitle changed in later patches. Replace whichever live-GPS subtitle is present.
patterns=[
    r"sub=\{gpsLive\?`LIVE GPS\$\{gps\?\.acc\?` · ±\$\{gps\.acc\} m`:''\}`:'GPS ready when you are'\}",
    r"sub=\{[^\n}]*LIVE GPS[^\n]*\}",
]
new="sub={`${build90Diagnostic}${gps?.acc?` · ±${gps.acc} m`:''}`}"
changed=False
for pattern in patterns:
    s2,n=re.subn(pattern,new,s,count=1)
    if n:
        s=s2;changed=True;break
# Do not fail the APK build just because cosmetic subtitle text changed.
if not changed:
    print('Build 90: Round subtitle anchor changed; diagnostic calculation installed without subtitle replacement')

# Replace misleading fallback wording where present.
s=s.replace("'Start live GPS'","(!build90GpsOk?'Waiting for GPS signal':!build90TargetOk?'Loading hole coordinates':'Live GPS ready')")
s=s.replace('"Start live GPS"',"(!build90GpsOk?'Waiting for GPS signal':!build90TargetOk?'Loading hole coordinates':'Live GPS ready')")

p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 90',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.90\"',t,count=1);g.write_text(t)
print('Build 90 GPS + hole target diagnostic applied')
