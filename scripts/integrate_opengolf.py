from pathlib import Path

p = Path('App.js')
t = p.read_text()

old_call = "{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open}}/>}"
new_call = "{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open,setTargets}}/>}"
if old_call in t:
    t = t.replace(old_call, new_call, 1)
elif new_call not in t:
    raise SystemExit('Course render call not found')

course = r'''function Course({course,setCourse,tee,setTee,hole,setHole,gps,getGPS,open,markTarget,currentTarget,setTargets}){
 const[q,setQ]=useState(''),[results,setResults]=useState([]),[searching,setSearching]=useState(false),[importing,setImporting]=useState(false);
 const searchCourses=async()=>{const term=q.trim();if(term.length<2)return Alert.alert('Course search','Type at least two letters of the course name.');setSearching(true);try{const r=await fetch(`https://api.opengolfapi.org/v1/courses/search?q=${encodeURIComponent(term)}&limit=12`);if(!r.ok)throw new Error(`HTTP ${r.status}`);const j=await r.json();const a=Array.isArray(j)?j:(j?.courses||j?.results||j?.data||[]);setResults(Array.isArray(a)?a:[]);if(!a?.length)Alert.alert('Course search','No matching course found. You can still enter and map it manually.')}catch(e){Alert.alert('Course search','The online course directory is unavailable right now. Manual setup still works.')}finally{setSearching(false)}};
 const point=v=>{if(!v||typeof v!=='object')return null;const lat=Number(v.lat??v.latitude??v.y),lon=Number(v.lon??v.lng??v.longitude??v.x);return Number.isFinite(lat)&&Number.isFinite(lon)?{lat,lon}:null};
 const holeTarget=h=>{const g=h?.green||h?.coordinates||h?.gps||{};return{front:point(h?.front||h?.green_front||h?.greenFront||g?.front),center:point(h?.center||h?.green_center||h?.greenCenter||h?.pin||g?.center||g?.green),back:point(h?.back||h?.green_back||h?.greenBack||g?.back)}};
 const selectCourse=async item=>{const id=item?.id??item?.course_id??item?.courseId;if(id===undefined||id===null)return Alert.alert('Course import','This course record has no usable ID.');setImporting(true);try{const [cr,hr,tr]=await Promise.all([fetch(`https://api.opengolfapi.org/v1/courses/${id}`),fetch(`https://api.opengolfapi.org/v1/courses/${id}/holes`),fetch(`https://api.opengolfapi.org/v1/courses/${id}/tees`)]);const c=cr.ok?await cr.json():item,hj=hr.ok?await hr.json():[],tj=tr.ok?await tr.json():[];const name=c?.name||c?.course_name||item?.name||item?.course_name||'Golf Course';setCourse(name);const hs=Array.isArray(hj)?hj:(hj?.holes||hj?.data||[]);if(Array.isArray(hs)&&hs.length){const mapped=Array.from({length:18},(_,i)=>holeTarget(hs[i]||{}));if(mapped.some(x=>x.front||x.center||x.back))setTargets(mapped)}const tees=Array.isArray(tj)?tj:(tj?.tees||tj?.data||[]);if(Array.isArray(tees)&&tees.length){const preferred=tees.find(x=>String(x?.color||x?.name||'').toLowerCase()===String(tee).toLowerCase())||tees[0];const raw=String(preferred?.color||preferred?.name||'');const match=TEES.find(x=>x.toLowerCase()===raw.toLowerCase());if(match)setTee(match)}setResults([]);setQ('');Alert.alert('Course loaded',`${name} is now stored with your local CaddieOS data. Any missing green points can still be mapped manually.`)}catch(e){Alert.alert('Course import','Could not import this course. Manual course setup is still available.')}finally{setImporting(false)}};
 return <><Title kicker="MAP & PLAY" title="Course"/>
 <Panel><Label text="COURSE DIRECTORY"/><View style={{flexDirection:'row',gap:7}}><TextInput value={q} onChangeText={setQ} onSubmitEditing={searchCourses} placeholder="Search course name" placeholderTextColor="#8A8F91" style={[s.input,{flex:1,marginBottom:0}]}/><TouchableOpacity onPress={searchCourses} disabled={searching} style={{backgroundColor:C.gold,borderRadius:10,paddingHorizontal:13,justifyContent:'center',opacity:searching?.65:1}}><Text style={{fontWeight:'900',color:C.text,fontSize:12}}>{searching?'SEARCHING':'SEARCH'}</Text></TouchableOpacity></View><Text style={[s.smallGrey,{marginTop:7}]}>Search OpenGolfAPI, then save the selected course locally. Manual mapping remains available.</Text>{results.map((x,i)=>{const name=x?.name||x?.course_name||'Golf Course',place=[x?.city,x?.state,x?.country].filter(Boolean).join(', ');return <TouchableOpacity key={String(x?.id??x?.course_id??i)} onPress={()=>selectCourse(x)} style={{paddingVertical:10,borderTopWidth:1,borderTopColor:C.line}}><Text style={{color:C.text,fontWeight:'900'}}>{name}</Text>{place?<Text style={s.smallGrey}>{place}</Text>:null}</TouchableOpacity>})}{importing?<Text style={{color:C.gold,fontWeight:'900',marginTop:8}}>IMPORTING COURSE…</Text>:null}<Text style={[s.smallGrey,{marginTop:8}]}>Contains data from OpenGolfAPI (opengolfapi.org).</Text></Panel>
 <Panel><Label text="COURSE NAME"/><TextInput value={course} onChangeText={setCourse} placeholder="Enter course" placeholderTextColor="#8A8F91" style={s.input}/><Label text="TEE"/><View style={s.chips}>{TEES.map(x=><Chip key={x} active={tee===x} text={x} onPress={()=>setTee(x)}/>)}</View></Panel>
 <Panel><View style={s.holeTop}><View><Text style={s.holeLabel}>CURRENT HOLE</Text><Text style={s.holeBig}>{hole}</Text></View><View style={s.holeBtns}><Mini text="−" onPress={()=>setHole(String(Math.max(1,n(hole)-1)))}/><Mini text="+" onPress={()=>setHole(String(Math.min(18,n(hole)+1)))}/></View></View><TouchableOpacity style={s.gps} onPress={getGPS}><Text style={s.gpsText}>⌖  GET GPS POSITION</Text></TouchableOpacity>{gps&&<Text style={s.gpsLine}>{gps.lat}, {gps.lon} · ±{gps.acc} m</Text>}<View style={s.divider}/><Text style={s.subTitle}>MAP GREEN — HOLE {hole}</Text><Text style={s.smallGrey}>Stand at each point and save its GPS coordinate. Imported courses can still be corrected here.</Text><View style={s.mapBtns}>{['front','center','back'].map(k=><TouchableOpacity key={k} style={[s.mapBtn,currentTarget?.[k]&&s.mapBtnDone]} onPress={()=>markTarget(k)}><Text style={s.mapBtnTxt}>{k.toUpperCase()}</Text></TouchableOpacity>)}</View></Panel>
 <TouchableOpacity style={s.infoBtn} onPress={()=>open('COURSEINFO')}><Text style={s.infoBtnText}>COURSE INFORMATION</Text></TouchableOpacity></>}
'''

start = t.find('function Course(')
end = t.find('\nfunction More', start)
if start < 0 or end < 0:
    raise SystemExit('Course component boundaries not found')
t = t[:start] + course + t[end:]

for needle in ['api.opengolfapi.org/v1/courses/search','Contains data from OpenGolfAPI','setTargets']:
    if needle not in t:
        raise SystemExit(f'Integration verification failed: {needle}')
p.write_text(t)
print('OpenGolfAPI integration applied to App.js')
