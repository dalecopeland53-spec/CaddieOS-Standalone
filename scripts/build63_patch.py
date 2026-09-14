from pathlib import Path
import re

app = Path('CaddieOS/App.js')
text = app.read_text()

# Ask for GPS permission once after the user enters the app, rather than waiting
# until a GPS button is pressed. The GPS buttons still re-check permission.
marker = " const gpsWatch=useRef(null);"
if marker not in text:
    raise SystemExit('Build 63: gpsWatch marker missing')
text = text.replace(marker, marker + "\n const gpsPermissionAsked=useRef(false);", 1)

persist_rx = r"( useEffect\(\(\)=>\{AsyncStorage\.setItem\(STORAGE,JSON\.stringify\(\{.*?\}\)\)\.catch\(\(\)=>\{\}\)\},\[.*?\]\);)"
m = re.search(persist_rx, text)
if not m:
    raise SystemExit('Build 63: persistence effect marker missing')
gps_effect = """
 useEffect(()=>{
  if(!entered||Platform.OS!=='android'||gpsPermissionAsked.current)return;
  gpsPermissionAsked.current=true;
  PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION).then(ok=>{
   if(ok!==PermissionsAndroid.RESULTS.GRANTED)Alert.alert('Location permission','CaddieOS needs location access for live GPS, hole mapping and course distances. You can allow it later from a GPS button.');
  }).catch(()=>{});
 },[entered]);"""
text = text[:m.end()] + gps_effect + text[m.end():]

# Keep bottom navigation strictly inside CaddieOS and make each tab a larger,
# reliable touch target. ROUND is also allowed because START ROUND uses go().
old_go = " const go=x=>{setScreen(null);setTab(x)},open=x=>setScreen(x),page=screen||tab;"
new_go = " const go=x=>{if(![...NAV,'ROUND'].includes(x))return;setScreen(null);setTab(x)},open=x=>setScreen(x),page=screen||tab;"
if old_go not in text:
    raise SystemExit('Build 63: navigation marker missing')
text = text.replace(old_go, new_go, 1)

old_nav = "function BottomNav({tab,go,bottom}){return <View style={[s.nav,{paddingBottom:Math.max(8,bottom)}]}>{NAV.map(x=><TouchableOpacity key={x} onPress={()=>go(x)} style={s.navItem}><Text style={[s.navText,tab===x&&s.navOn]}>{x}</Text></TouchableOpacity>)}</View>}"
new_nav = "function BottomNav({tab,go,bottom}){return <View style={[s.nav,{paddingBottom:Math.max(8,bottom)}]}>{NAV.map(x=><TouchableOpacity key={x} activeOpacity={.65} hitSlop={{top:6,bottom:6,left:2,right:2}} onPress={()=>go(x)} style={s.navItem}><Text style={[s.navText,tab===x&&s.navOn]}>{x}</Text></TouchableOpacity>)}</View>}"
if old_nav not in text:
    raise SystemExit('Build 63: BottomNav marker missing')
text = text.replace(old_nav, new_nav, 1)

app.write_text(text)

# Build 63 identity.
gradle = Path('CaddieOS/android/app/build.gradle')
g = gradle.read_text()
g = re.sub(r'versionCode\s+\d+', 'versionCode 63', g)
g = re.sub(r'versionName\s+"[^"]+"', 'versionName "1.0.63"', g)
gradle.write_text(g)

# Guarantee every native permission independently. Previous builds added the
# location permissions conditionally with the microphone permission.
manifest = Path('CaddieOS/android/app/src/main/AndroidManifest.xml')
m = manifest.read_text()
required = [
    'android.permission.RECORD_AUDIO',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.ACCESS_COARSE_LOCATION',
    'android.permission.INTERNET',
]
for perm in required:
    tag = f'<uses-permission android:name="{perm}" />'
    if perm not in m:
        m = m.replace('<application', tag + '\n    <application', 1)
manifest.write_text(m)

print('Build 63 GPS and navigation patch applied')
