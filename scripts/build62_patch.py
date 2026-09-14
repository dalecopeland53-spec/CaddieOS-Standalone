from pathlib import Path
import re
p=Path('CaddieOS/App.js'); t=p.read_text()
# Build 62 compatibility patch. Every operation is intentionally idempotent so
# later release workflows can safely run it against an already-upgraded App.js.
t=re.sub(r'<Label text="EMAIL"/><TextInput[^>]*?/>','',t,count=1)

# Only upgrade the legacy Current Hole block when it is actually present.
old='''<Panel><View style={s.holeTop}><View><Text style={s.holeLabel}>CURRENT HOLE</Text><Text style={s.holeBig}>{hole}</Text></View><View style={s.holeBtns}><Mini text="−" onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}/><Mini text="+" onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}/></View></View><TouchableOpacity style={s.gps} onPress={getGPS}><Text style={s.gpsText}>⌖  GET MAPPING GPS</Text></TouchableOpacity>{gps&&<Text style={s.gpsLine}>{gps.lat}, {gps.lon} · ±{gps.acc} m</Text>}<View style={s.divider}/><Text style={s.subTitle}>MAP GREEN · HOLE {hole}</Text><Text style={s.smallGrey}>Mapping GPS only: stand at Front, Centre and Back, then save each point.</Text><View style={s.targetGrid}>'''
new='''<Panel><View style={{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:8}}><Text style={[s.holeLabel,{fontSize:18,color:C.navy}]}>CURRENT HOLE</Text><View style={{borderWidth:1,borderColor:C.gold,borderRadius:10,backgroundColor:C.navy,paddingHorizontal:10,paddingVertical:5}}><Text style={{color:C.gold2,fontWeight:'900',fontSize:10}}>Hole {hole} of 18</Text></View></View><View style={{flexDirection:'row',gap:9,alignItems:'stretch'}}><View style={{width:116,minHeight:126,borderRadius:15,backgroundColor:C.navy,borderWidth:2,borderColor:C.gold,alignItems:'center',justifyContent:'center'}}><Text style={{color:C.white,fontWeight:'900',fontSize:13}}>HOLE</Text><Text style={{color:C.white,fontWeight:'900',fontSize:64,lineHeight:70}}>{hole}</Text></View><View style={{width:54,gap:8}}><Mini text="+" onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}/><Mini text="−" onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}/></View><View style={{flex:1,gap:7}}><TouchableOpacity style={[s.gps,{marginTop:0,flex:1,justifyContent:'center'}]} onPress={getGPS}><Text style={s.gpsText}>⌖  GET MAPPING GPS</Text></TouchableOpacity><Text style={[s.smallGrey,{fontSize:10}]}>Stand at Front, Centre and Back, then save each point.</Text>{gps&&<Text style={[s.gpsLine,{fontSize:9}]}>{gps.lat}, {gps.lon} · ±{gps.acc} m</Text>}</View></View><View style={s.divider}/><Text style={s.subTitle}>MAP GREEN · HOLE {hole}</Text><View style={s.targetGrid}>'''
if old in t:
    t=t.replace(old,new,1)

# Cosmetic tightening is safe whether or not an earlier build already applied it.
t=t.replace("maxWidth:145","maxWidth:118",1)
t=t.replace("savedCourses.slice(0,8)","savedCourses.slice(0,5)",1)

# Add the dedicated Round wind meter only when the known insertion marker exists.
marker='<View style={s.panel}><Text style={s.panelTitle}>GREEN DISTANCES</Text>'
windbox='''<View style={[s.panel,{padding:10}]}><View style={{flexDirection:'row',alignItems:'center',justifyContent:'space-between'}}><View><Text style={s.panelTitle}>LIVE WIND</Text><Text style={{fontSize:12,fontWeight:'900',color:C.muted}}>{windType}</Text></View><View style={{width:58,height:58,borderRadius:29,backgroundColor:C.navy,borderWidth:2,borderColor:C.gold,alignItems:'center',justifyContent:'center'}}><Text style={{fontSize:32,lineHeight:34,fontWeight:'900',color:C.gold2}}>{arrow}</Text></View><View style={{alignItems:'flex-end'}}><Text style={{fontSize:28,fontWeight:'900',color:C.navy}}>{wind||0}</Text><Text style={{fontSize:11,fontWeight:'900',color:C.muted}}>{units==='METRES'?'km/h':'mph'}</Text></View></View></View>'''
if 'LIVE WIND' not in t and marker in t:
    t=t.replace(marker,windbox+marker,1)

# Voice label repair when legacy wording remains.
t=t.replace('text="CADDIE" onPress={listen}','text={listening?"LISTENING…":"TAP TO TALK"} onPress={listen}')

# Ensure Android speech permission without making the compatibility patch fatal.
manifest=Path('CaddieOS/android/app/src/main/AndroidManifest.xml')
if manifest.exists():
    m=manifest.read_text()
    if 'android.permission.RECORD_AUDIO' not in m:
        pos=m.find('>')
        if pos!=-1:
            m=m[:pos+1]+'\n    <uses-permission android:name="android.permission.RECORD_AUDIO" />'+m[pos+1:]
    manifest.write_text(m)

p.write_text(t)
print('Build 62 compatibility patch complete')
