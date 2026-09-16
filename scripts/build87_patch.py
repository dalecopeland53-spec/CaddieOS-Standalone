from pathlib import Path
import re

app=Path('CaddieOS/App.js');s=app.read_text()
if 'BUILD87_NEARBY_COURSE_LOCK' not in s:
    marker='const BUILD86_LIVE_TARGET_FIX=true;'
    if marker not in s: raise SystemExit('Build 86 marker missing')
    s=s.replace(marker,marker+'\nconst BUILD87_NEARBY_COURSE_LOCK=true;',1)

# OpenGolfAPI v3.6.1 supports server-side lat/lng/radius_mi search: do not download/filter the world on-device.
anchor='async function searchOpenGolfCourses(query)'
nearby="""async function searchNearbyOpenGolfCourses(gps,radiusKm=50,limit=5){
  const lat=Number(gps?.lat),lng=Number(gps?.lon??gps?.lng);
  if(!Number.isFinite(lat)||!Number.isFinite(lng))throw new Error('Valid GPS position required');
  const radiusMi=Math.max(1,Number(radiusKm)||50)*0.621371;
  const r=await fetch(`${OPENGOLF_API}/courses/search?lat=${encodeURIComponent(lat)}&lng=${encodeURIComponent(lng)}&radius_mi=${encodeURIComponent(radiusMi.toFixed(2))}&limit=${Math.max(1,Math.min(10,Number(limit)||5))}`);
  if(!r.ok)throw new Error('Nearby course search unavailable');
  const j=await r.json();
  const rows=Array.isArray(j)?j:(j.courses||j.results||[]);
  return rows.slice().sort((a,b)=>Number(a.distance_mi??Infinity)-Number(b.distance_mi??Infinity));
}

"""
if 'async function searchNearbyOpenGolfCourses' not in s:
    if anchor not in s: raise SystemExit('OpenGolf search anchor missing')
    s=s.replace(anchor,nearby+anchor,1)

# Replace picker with GPS-first nearby search, while retaining manual text search as fallback.
start=s.find('function RealCoursePicker(')
end=s.find('\nfunction Round(',start)
if start<0 or end<0: raise SystemExit('RealCoursePicker/Round anchor missing')
ui="""function RealCoursePicker({course,setCourse,realCourse,setRealCourse,gps,getGPS}){
 const[q,setQ]=useState(course||''),[rows,setRows]=useState([]),[busy,setBusy]=useState(false),[err,setErr]=useState(''),[radius,setRadius]=useState(50);
 const search=async()=>{setBusy(true);setErr('');try{setRows(await searchOpenGolfCourses(q))}catch(e){setErr('Course search unavailable. Check internet and try again.')}finally{setBusy(false)}};
 const nearby=async km=>{setBusy(true);setErr('');setRadius(km);try{let p=gps;if(!p||!Number.isFinite(Number(p.lat))||!Number.isFinite(Number(p.lon))){await getGPS?.();setErr('GPS acquired. Tap NEARBY again to search around your position.');setRows([]);return}const found=await searchNearbyOpenGolfCourses(p,km,5);setRows(found);if(!found.length)setErr(`No courses found within ${km} km.`)}catch(e){setErr('Could not search nearby courses. Check GPS and internet.')}finally{setBusy(false)}};
 const choose=async x=>{const id=x.id??x.course_id??x.osm_id;if(id==null)return;setBusy(true);setErr('');try{const d=await loadOpenGolfCourse(id);const selected=d?.course??d;if(!selected?.id)throw new Error('Course did not resolve to one ID');const locked={...d,course:{...selected,id:selected.id}};setRealCourse(locked);setCourse(selected.course_name||selected.name||x.course_name||x.name||q);setRows([])}catch(e){setErr('Could not load that course.')}finally{setBusy(false)}};
 const selected=realCourse?.course??realCourse;
 return <View style={{marginTop:10}}><Text style={{fontWeight:'900',color:C.navy,fontSize:14}}>REAL COURSE DATABASE</Text><View style={{flexDirection:'row',gap:7,marginTop:7}}><TouchableOpacity onPress={()=>nearby(50)} style={{backgroundColor:C.blue,borderRadius:10,paddingHorizontal:12,paddingVertical:9}}><Text style={{color:C.white,fontWeight:'900'}}>NEARBY 50 KM</Text></TouchableOpacity><TouchableOpacity onPress={()=>nearby(200)} style={{borderWidth:1,borderColor:C.blue,borderRadius:10,paddingHorizontal:12,paddingVertical:9}}><Text style={{color:C.blue,fontWeight:'900'}}>200 KM</Text></TouchableOpacity></View><View style={{flexDirection:'row',gap:8,marginTop:7}}><TextInput value={q} onChangeText={setQ} placeholder="Or search course name" placeholderTextColor={C.muted} style={{flex:1,borderWidth:1,borderColor:C.line,borderRadius:10,paddingHorizontal:10,paddingVertical:8,color:C.text,backgroundColor:C.white}}/><TouchableOpacity onPress={search} style={{backgroundColor:C.blue,borderRadius:10,paddingHorizontal:15,justifyContent:'center'}}><Text style={{color:C.white,fontWeight:'900'}}>SEARCH</Text></TouchableOpacity></View>{busy&&<Text style={{marginTop:6,color:C.muted}}>Loading real course data…</Text>}{!!err&&<Text style={{marginTop:6,color:'#8B1E1E'}}>{err}</Text>}{rows.slice(0,5).map((x,k)=><TouchableOpacity key={String(x.id??x.course_id??k)} onPress={()=>choose(x)} style={{paddingVertical:9,borderBottomWidth:1,borderBottomColor:C.line}}><Text style={{fontWeight:'800',color:C.text}}>{x.course_name||x.name||'Golf course'}</Text><Text style={{fontSize:11,color:C.muted}}>{[x.city,x.state,x.country,Number.isFinite(Number(x.distance_mi))?`${(Number(x.distance_mi)*1.60934).toFixed(1)} km`:null].filter(Boolean).join(' · ')}</Text></TouchableOpacity>)}{!!selected?.id&&<Text style={{marginTop:7,color:C.text,fontWeight:'800'}}>LOCKED: {selected.course_name||selected.name||course} · {(realCourse?.holes||selected?.holes||[]).length} holes</Text>}<Text style={{marginTop:5,fontSize:9,color:C.muted}}>Course data: OpenGolfAPI · OpenStreetMap contributors</Text></View>}
"""
s=s[:start]+ui+s[end:]

# Give picker access to the app's existing GPS getter/state.
s=s.replace('<RealCoursePicker course={course} setCourse={setCourse} realCourse={realCourse} setRealCourse={setRealCourse}/>','<RealCoursePicker course={course} setCourse={setCourse} realCourse={realCourse} setRealCourse={setRealCourse} gps={gps} getGPS={getGPS}/>',1)

# Defensive Round data shape: only use hole API data after one explicit course ID has resolved.
old='apiHole=openGolfHoleContext(realCourse,idx+1)'
new="selectedCourse=realCourse?.course??realCourse,courseResolved=!!selectedCourse?.id,apiHole=courseResolved?openGolfHoleContext(realCourse,idx+1):null"
if old not in s: raise SystemExit('Build 86 apiHole anchor missing')
s=s.replace(old,new,1)
s=s.replace('rawHole=apiHole?.raw||{}','rawHole=apiHole?.raw||apiHole||{}',1)

app.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 87',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.87"',t,count=1);g.write_text(t)
print('Build 87 GPS nearby course selection and selected-course lock applied')
