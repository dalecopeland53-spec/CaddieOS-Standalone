from pathlib import Path
import re

app=Path('CaddieOS/App.js');s=app.read_text()
if 'BUILD80_REAL_COURSE_SELECT' not in s:s=s.replace('const BUILD79_STARTUP_FIX=true;','const BUILD79_STARTUP_FIX=true;\nconst BUILD80_REAL_COURSE_SELECT=true;',1)

# Real course search/selection UI. Selection downloads holes/tees, caches them and updates app course name.
anchor='function Round('
ui="""function RealCoursePicker({course,setCourse,realCourse,setRealCourse}){const[q,setQ]=useState(course||''),[rows,setRows]=useState([]),[busy,setBusy]=useState(false),[err,setErr]=useState('');const search=async()=>{setBusy(true);setErr('');try{setRows(await searchOpenGolfCourses(q))}catch(e){setErr('Course search unavailable. Check internet and try again.')}finally{setBusy(false)}};const choose=async x=>{const id=x.id??x.course_id??x.osm_id;if(id==null)return;setBusy(true);setErr('');try{const d=await loadOpenGolfCourse(id);setRealCourse(d);setCourse(d.course?.name||x.name||q);setRows([])}catch(e){setErr('Could not load that course.')}finally{setBusy(false)}};return <View style={{marginTop:10}}><Text style={{fontWeight:'900',color:C.navy,fontSize:14}}>REAL COURSE DATABASE</Text><View style={{flexDirection:'row',gap:8,marginTop:7}}><TextInput value={q} onChangeText={setQ} placeholder="Search golf course" placeholderTextColor={C.muted} style={{flex:1,borderWidth:1,borderColor:C.line,borderRadius:10,paddingHorizontal:10,paddingVertical:8,color:C.text,backgroundColor:C.white}}/><TouchableOpacity onPress={search} style={{backgroundColor:C.blue,borderRadius:10,paddingHorizontal:15,justifyContent:'center'}}><Text style={{color:C.white,fontWeight:'900'}}>SEARCH</Text></TouchableOpacity></View>{busy&&<Text style={{marginTop:6,color:C.muted}}>Loading real course data…</Text>}{!!err&&<Text style={{marginTop:6,color:'#8B1E1E'}}>{err}</Text>}{rows.slice(0,8).map((x,k)=><TouchableOpacity key={String(x.id??x.course_id??k)} onPress={()=>choose(x)} style={{paddingVertical:9,borderBottomWidth:1,borderBottomColor:C.line}}><Text style={{fontWeight:'800',color:C.text}}>{x.name||x.course_name||'Golf course'}</Text><Text style={{fontSize:11,color:C.muted}}>{[x.city,x.state,x.country].filter(Boolean).join(' · ')}</Text></TouchableOpacity>)}{realCourse&&<Text style={{marginTop:7,color:C.text,fontWeight:'800'}}>Loaded: {realCourse.course?.name||course} · {(realCourse.holes||[]).length} holes</Text>}<Text style={{marginTop:5,fontSize:9,color:C.muted}}>Course data: OpenGolfAPI · OpenStreetMap contributors</Text></View>}

"""
if 'function RealCoursePicker' not in s:
    if anchor not in s:raise SystemExit('Round anchor missing')
    s=s.replace(anchor,ui+anchor,1)

# Pass real-course state into Course screen.
s=s.replace("{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open,setTargets}}/>}","{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open,setTargets,realCourse,setRealCourse}}/>}",1)

# Inject picker into Course component without redesigning the approved page.
s=re.sub(r'function Course\(\{([^}]*)\}\)',lambda m:'function Course({'+(m.group(1)+',realCourse,setRealCourse' if 'realCourse' not in m.group(1) else m.group(1))+'})',s,count=1)
# Place picker immediately before the Course component's final closing Scroll/Page area by using its COURSE INFO heading when available.
needle='<Text style={s.h2}>COURSE INFO</Text>'
if needle in s and 'RealCoursePicker course={course}' not in s:
    s=s.replace(needle,'<RealCoursePicker course={course} setCourse={setCourse} realCourse={realCourse} setRealCourse={setRealCourse}/>'+needle,1)

# Feed real mapped front/centre/back coordinates into GPS distance calculation when API provides coordinates.
old="const idx=Math.min(17,Math.max(0,n(hole)-1)),currentTarget=targets[idx],gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null,targetDistances={front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)};"
new="const idx=Math.min(17,Math.max(0,n(hole)-1)),apiHole=openGolfHoleContext(realCourse,idx+1),coord=v=>{if(!v)return null;const lat=Number(v.lat??v.latitude),lon=Number(v.lon??v.lng??v.longitude);return Number.isFinite(lat)&&Number.isFinite(lon)?{lat,lon}:null},rawHole=apiHole.raw||{},apiTarget={front:coord(rawHole.front||rawHole.green_front||rawHole.front_coordinate),center:coord(rawHole.center||rawHole.green_center||rawHole.center_coordinate||rawHole.green),back:coord(rawHole.back||rawHole.green_back||rawHole.back_coordinate)},currentTarget={...targets[idx],front:apiTarget.front||targets[idx]?.front,center:apiTarget.center||targets[idx]?.center,back:apiTarget.back||targets[idx]?.back},gp=gps?{lat:Number(gps.lat),lon:Number(gps.lon)}:null,targetDistances={front:haversine(gp,currentTarget?.front,units),center:haversine(gp,currentTarget?.center,units),back:haversine(gp,currentTarget?.back,units)};"
if old in s:s=s.replace(old,new,1)

app.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 80',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.80"',t,count=1);g.write_text(t)
print('Build 80 real course selection and GPS caddie wiring applied')
