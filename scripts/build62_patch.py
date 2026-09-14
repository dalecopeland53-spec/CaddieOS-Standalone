from pathlib import Path
import re
p=Path('CaddieOS/App.js'); t=p.read_text()
# Settings: remove email field to keep player settings compact.
t=re.sub(r'<Label text="EMAIL"/><TextInput[^>]*?/>','',t,count=1)
# Header: preserve full tagline at compact readable size.
t=t.replace('TOUR-LEVEL DECISIONS · YOUR GAME</Text>','TOUR-LEVEL DECISIONS · YOUR GAME</Text>')
# Current Hole: replace legacy vertical mapping block with approved boxed layout.
old='''<Panel><View style={s.holeTop}><View><Text style={s.holeLabel}>CURRENT HOLE</Text><Text style={s.holeBig}>{hole}</Text></View><View style={s.holeBtns}><Mini text="−" onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}/><Mini text="+" onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}/></View></View><TouchableOpacity style={s.gps} onPress={getGPS}><Text style={s.gpsText}>⌖  GET MAPPING GPS</Text></TouchableOpacity>{gps&&<Text style={s.gpsLine}>{gps.lat}, {gps.lon} · ±{gps.acc} m</Text>}<View style={s.divider}/><Text style={s.subTitle}>MAP GREEN · HOLE {hole}</Text><Text style={s.smallGrey}>Mapping GPS only: stand at Front, Centre and Back, then save each point.</Text><View style={s.targetGrid}>'''
new='''<Panel><View style={{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:8}}><Text style={[s.holeLabel,{fontSize:18,color:C.navy}]}>CURRENT HOLE</Text><View style={{borderWidth:1,borderColor:C.gold,borderRadius:10,backgroundColor:C.navy,paddingHorizontal:10,paddingVertical:5}}><Text style={{color:C.gold2,fontWeight:'900',fontSize:10}}>Hole {hole} of 18</Text></View></View><View style={{flexDirection:'row',gap:9,alignItems:'stretch'}}><View style={{width:116,minHeight:126,borderRadius:15,backgroundColor:C.navy,borderWidth:2,borderColor:C.gold,alignItems:'center',justifyContent:'center'}}><Text style={{color:C.white,fontWeight:'900',fontSize:13}}>HOLE</Text><Text style={{color:C.white,fontWeight:'900',fontSize:64,lineHeight:70}}>{hole}</Text></View><View style={{width:54,gap:8}}><Mini text="+" onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}/><Mini text="−" onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}/></View><View style={{flex:1,gap:7}}><TouchableOpacity style={[s.gps,{marginTop:0,flex:1,justifyContent:'center'}]} onPress={getGPS}><Text style={s.gpsText}>⌖  GET MAPPING GPS</Text></TouchableOpacity><Text style={[s.smallGrey,{fontSize:10}]}>Stand at Front, Centre and Back, then save each point.</Text>{gps&&<Text style={[s.gpsLine,{fontSize:9}]}>{gps.lat}, {gps.lon} · ±{gps.acc} m</Text>}</View></View><View style={s.divider}/><Text style={s.subTitle}>MAP GREEN · HOLE {hole}</Text><View style={s.targetGrid}>'''
if old not in t: raise SystemExit('Build 62 current-hole marker missing')
t=t.replace(old,new,1)
# Tighten course cards/search/saved row without reducing tap targets.
t=t.replace("maxWidth:145","maxWidth:118",1)
t=t.replace("savedCourses.slice(0,8)","savedCourses.slice(0,5)",1)
# Version/build identity and native mic label repair.
t=t.replace('versionCode 61','versionCode 62')
# Voice button wording: tapping should clearly start recognition, not just say Caddie.
t=t.replace('text="CADDIE" onPress={listen}','text={listening?"LISTENING…":"TAP TO TALK"} onPress={listen}')
# Ensure Android speech recognition is requested by native app.
manifest=Path('CaddieOS/android/app/src/main/AndroidManifest.xml')
if manifest.exists():
 m=manifest.read_text()
 if 'android.permission.RECORD_AUDIO' not in m: m=m.replace('<manifest','<manifest',1).replace('>','>\n    <uses-permission android:name="android.permission.RECORD_AUDIO" />',1)
 manifest.write_text(m)
p.write_text(t)
print('Build 62 patch applied')
