from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
# Build 92: startup-safe release based on corrected Build 91 chain.
marker='const BUILD91_LIVE_COURSE_CHAIN=true;'
if marker in s and 'BUILD92_STARTUP_SAFE' not in s:
    s=s.replace(marker,marker+'\nconst BUILD92_STARTUP_SAFE=true;',1)
# Do not allow the Round component to call Shell-only setDistance.
# The live distance state update remains in Shell, where setDistance is defined.
# Harden GPS coordinate checks without rejecting valid zero coordinates.
s=s.replace("function haversine(a,b,u){if(!a||!b||!a.lat||!a.lon||!b.lat||!b.lon)return null;","function haversine(a,b,u){if(!a||!b||!Number.isFinite(Number(a.lat))||!Number.isFinite(Number(a.lon))||!Number.isFinite(Number(b.lat))||!Number.isFinite(Number(b.lon)))return null;",1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 92',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.92\"',t,count=1);g.write_text(t)
print('Build 92 startup-safe patch applied')
