from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD71_PLAYER_ONE' not in s:
    s=s.replace('const BUILD70_PHONE_FIT=true;', 'const BUILD70_PHONE_FIT=true;\nconst BUILD71_PLAYER_ONE=true;', 1)
old='<Text style={s.scoreLabel}>YOU</Text>'
if old not in s:
    raise SystemExit('Build 71: scorecard Player 1 marker missing')
s=s.replace(old,'<Text style={s.scoreLabel}>Player 1</Text>',2)
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 71',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.71"',t,count=1)
    g.write_text(t)
print('Build 71 Player 1 label applied')
