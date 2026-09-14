from pathlib import Path
import re

APP=Path('CaddieOS/App.js')
s=APP.read_text()

if "BUILD65_WIND_UI" not in s:
    s=s.replace("const BUILD64_PREMIUM=true;", "const BUILD64_PREMIUM=true;\nconst BUILD65_WIND_UI=true;")

# Put the live wind values on the Round screen, using the same state as Talking Caddie.
s=s.replace("<Round hole={hole} setHole={setHole} result={result} units={units} gps={gps} getGPS={getGPS} targetDistances={targetDistances} open={open}/>",
            "<Round hole={hole} setHole={setHole} result={result} units={units} gps={gps} getGPS={getGPS} targetDistances={targetDistances} open={open} wind={wind} windDir={windDir}/>")

s=re.sub(r"function Round\(\{hole,setHole,result,units,gps,getGPS,targetDistances,open\}\)\{.*?\}\nfunction Caddie",
'''function Round({hole,setHole,result,units,gps,getGPS,targetDistances,open,wind,windDir}){const arrow={HEAD:'↓',TAIL:'↑','L→R':'→','R→L':'←'}[windDir]||'•';const label={HEAD:'HEADWIND',TAIL:'TAILWIND','L→R':'LEFT → RIGHT','R→L':'RIGHT → LEFT'}[windDir]||windDir;const cross=windDir==='L→R'||windDir==='R→L';const hold=cross?Math.max(1,Math.round(n(wind)*.4)):0;const holdSide=windDir==='L→R'?'LEFT':'RIGHT';return <><Title kicker="PLAY" title={`Hole ${hole}`} sub="Live playing position"/><View style={s.holeStrip}><TouchableOpacity style={s.holeStep} onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}><Text style={s.holeStepText}>‹</Text></TouchableOpacity><Text style={s.holeNumber}>HOLE {hole}</Text><TouchableOpacity style={s.holeStep} onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}><Text style={s.holeStepText}>›</Text></TouchableOpacity></View><View style={s.panel}><Text style={s.panelTitle}>GREEN DISTANCES</Text><View style={s.distanceRow}><Stat a={targetDistances.front??'—'} b="FRONT"/><Stat a={targetDistances.center??'—'} b="CENTRE"/><Stat a={targetDistances.back??'—'} b="BACK"/></View><Text style={s.small}>{units==='METRES'?'metres':'yards'}</Text></View><View style={s.windCard}><View style={s.windArrowBox}><Text style={s.windArrow}>{arrow}</Text></View><View style={s.windInfo}><Text style={s.windLabel}>WIND DIRECTION</Text><Text style={s.windMain}>{label}</Text><Text style={s.windSub}>{n(wind)} {units==='METRES'?'km/h':'mph'}{cross&&n(wind)>0?` · HOLD ~${hold} ${units==='METRES'?'m':'yd'} ${holdSide}`:''}</Text></View><TouchableOpacity style={s.windEdit} onPress={()=>open('CADDIE')}><Text style={s.windEditText}>EDIT</Text></TouchableOpacity></View><View style={s.panel}><Text style={s.panelTitle}>CADDIE RECOMMENDATION</Text><View style={s.recRow}><Text style={s.bigClub}>{result.club}</Text><Text style={s.playingDistance}>PLAYING {result.y} {units==='METRES'?'m':'yd'}</Text></View></View><Btn text={gps?'REFRESH GPS':'GET GPS POSITION'} onPress={getGPS}/><Btn text="ASK CADDIE" onPress={()=>open('CADDIE')} outline/><Btn text="SCORE THIS HOLE" onPress={()=>open('SCORE')} outline/></>}
function Caddie''', s, count=1, flags=re.S)

# Make crosswind advice explicit and directional.
s=re.sub(r"function advice\(target,club,lie,w,dir,e,u\)\{.*?\}\nfunction haversine",
'''function advice(target,club,lie,w,dir,e,u){const unit=u==='METRES'?'metres':'yards';let t=`Playing ${target} ${unit}. ${club}.`;if(lie!=='Tee'&&lie!=='Fairway')t+=` Allow for ${lie.toLowerCase()}.`;if(n(w)){if(dir==='HEAD')t+=` Headwind ${w}; flight it lower and allow more club.`;else if(dir==='TAIL')t+=` Tailwind ${w}; expect extra carry.`;else if(dir==='L→R'){const h=Math.max(1,Math.round(n(w)*.4));t+=` Wind left to right ${w}; start about ${h} ${u==='METRES'?'metres':'yards'} left.`}else if(dir==='R→L'){const h=Math.max(1,Math.round(n(w)*.4));t+=` Wind right to left ${w}; start about ${h} ${u==='METRES'?'metres':'yards'} right.`}}if(n(e)>0)t+=` Uphill ${Math.abs(n(e))}%.`;if(n(e)<0)t+=` Downhill ${Math.abs(n(e))}%.`;return t+' Pick the target, picture the shot and commit.'}
function haversine''', s, count=1, flags=re.S)

# Add premium silver/blue wind card styles. Appended last so they win.
insert=""",holeStrip:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',backgroundColor:'#F7F9FA',borderWidth:1,borderColor:C.line,borderRadius:10,paddingHorizontal:8,paddingVertical:5,marginBottom:7},holeStep:{width:38,height:34,borderRadius:8,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'},holeStepText:{color:C.white,fontSize:24,fontWeight:'900',lineHeight:26},holeNumber:{color:C.navy,fontSize:15,fontWeight:'900',letterSpacing:.8},windCard:{flexDirection:'row',alignItems:'center',backgroundColor:'#F7F9FA',borderWidth:1,borderColor:C.blue,borderRadius:10,padding:8,marginBottom:7},windArrowBox:{width:54,height:54,borderRadius:27,backgroundColor:'#D8EAF5',borderWidth:1,borderColor:C.blue,alignItems:'center',justifyContent:'center'},windArrow:{fontSize:32,fontWeight:'900',color:C.navy,lineHeight:36},windInfo:{flex:1,paddingHorizontal:10},windLabel:{fontSize:8,fontWeight:'900',letterSpacing:1,color:C.blue},windMain:{fontSize:14,fontWeight:'900',color:C.navy,marginTop:1},windSub:{fontSize:10,fontWeight:'700',color:C.muted,marginTop:2},windEdit:{borderWidth:1,borderColor:C.blue,borderRadius:7,paddingHorizontal:9,paddingVertical:7,backgroundColor:'#EAF2F7'},windEditText:{fontSize:9,fontWeight:'900',color:C.navy},playingDistance:{fontSize:10,fontWeight:'900',color:C.blue}"""
idx=s.rfind('});')
if idx!=-1 and 'windArrowBox' not in s[idx-9000:]:
    s=s[:idx]+insert+s[idx:]

APP.write_text(s)

# Version Build 65.
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+', 'versionCode 65', t, count=1)
    t=re.sub(r'versionName\s+"[^"]+"', 'versionName "1.0.65"', t, count=1)
    g.write_text(t)

print('Build 65 wind UI patch applied')
