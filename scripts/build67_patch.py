from pathlib import Path
import re

APP=Path('CaddieOS/App.js')
s=APP.read_text()

# Build 67 is a functional completion pass only. Preserve the approved
# Build 66 / compact S24 UI instead of replacing screen components/styles.
if 'BUILD67_RESPONSIVE' not in s:
    anchor='const BUILD66_LOGIN=true;'
    if anchor in s:
        s=s.replace(anchor,anchor+'\nconst BUILD67_RESPONSIVE=true;',1)
    else:
        s='const BUILD67_RESPONSIVE=true;\n'+s

# Keep anti-glare preference across launches without changing its approved UI.
needle=" const[antiGlare,setAntiGlare]=useState(true);"
if needle in s and "AsyncStorage.getItem('CADDIEOS_ANTIGLARE_V1')" not in s:
    s=s.replace(needle,needle+"\n useEffect(()=>{AsyncStorage.getItem('CADDIEOS_ANTIGLARE_V1').then(v=>{if(v!==null)setAntiGlare(v==='true')}).catch(()=>{})},[]);\n useEffect(()=>{AsyncStorage.setItem('CADDIEOS_ANTIGLARE_V1',String(antiGlare)).catch(()=>{})},[antiGlare]);",1)

# Do NOT replace Settings, Bag, Scorecard, header, body, or navigation here.
# Those Build 67 replacements caused the visible sizing/layout regression.
# Wind direction, GPS, microphone/TTS, 4-player scorecard and the approved
# login are supplied by the earlier verified build patches.

APP.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 68',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.68"',t,count=1)
    g.write_text(t)

print('Build 68 regression fix applied: approved compact UI preserved')
