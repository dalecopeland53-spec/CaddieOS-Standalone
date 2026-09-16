from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD84_ACTIVE_COURSE_FIX' not in s:s=s.replace('const BUILD83_COURSE_MANAGEMENT=true;','const BUILD83_COURSE_MANAGEMENT=true;\nconst BUILD84_ACTIVE_COURSE_FIX=true;',1)
# The visible Course screen uses its own selectCourse importer (from Build 61), not RealCoursePicker.
# Wire THAT importer to the same realCourse state consumed by Round.
s=re.sub(r'function Course\(\{([^}]*)\}\)',lambda m:'function Course({'+(m.group(1)+',realCourse,setRealCourse' if 'setRealCourse' not in m.group(1) else m.group(1))+'})',s,count=1)
old="const c=cr.ok?await cr.json():item,hj=hr.ok?await hr.json():[],tj=tr.ok?await tr.json():[];const name=c?.name||c?.course_name||item?.name||item?.course_name||'Golf Course';setCourse(name);"
new="const c=cr.ok?await cr.json():item,hj=hr.ok?await hr.json():[],tj=tr.ok?await tr.json():[];const hs=Array.isArray(hj)?hj:(hj?.holes||hj?.data||[]),tees=Array.isArray(tj)?tj:(tj?.tees||tj?.data||[]),real={course:c,holes:hs,tees,source:'OpenGolfAPI / OpenStreetMap contributors',savedAt:Date.now()};setRealCourse&&setRealCourse(real);AsyncStorage.setItem('caddieos.realCourse',JSON.stringify(real)).catch(()=>{});const name=c?.name||c?.course_name||item?.name||item?.course_name||'Golf Course';setCourse(name);"
if old not in s: raise SystemExit('Build84 visible selectCourse importer marker missing')
s=s.replace(old,new,1)
# Reuse hs/tees already normalised above.
s=s.replace("const hs=Array.isArray(hj)?hj:(hj?.holes||hj?.data||[]);if(Array.isArray(hs)&&hs.length)","if(Array.isArray(hs)&&hs.length)",1)
s=s.replace("const tees=Array.isArray(tj)?tj:(tj?.tees||tj?.data||[]);if(Array.isArray(tees)&&tees.length)","if(Array.isArray(tees)&&tees.length)",1)
# Saved course selection must restore its linked real payload when present.
s=s.replace("const loadSaved=x=>{setCourse(x.name);", "const loadSaved=x=>{setCourse(x.name);if(x.realCourse){setRealCourse&&setRealCourse(x.realCourse);AsyncStorage.setItem('caddieos.realCourse',JSON.stringify(x.realCourse)).catch(()=>{})}else{setRealCourse&&setRealCourse(null);AsyncStorage.removeItem('caddieos.realCourse').catch(()=>{})}",1)
# Save the active real payload with the course entry.
s=s.replace("const entry={name,tee,targets,courseMetres};", "const entry={name,tee,targets,courseMetres,realCourse:realCourse||null};",1)
s=s.replace("const entry={name,tee,targets};", "const entry={name,tee,targets,realCourse:realCourse||null};",1)
# Manual course deliberately clears API course state.
s=s.replace("setManual(true);setSource('manual');setCourse('');setTargets(blankTargets())", "setManual(true);setSource('manual');setCourse('');setRealCourse&&setRealCourse(null);AsyncStorage.removeItem('caddieos.realCourse').catch(()=>{});setTargets(blankTargets())",1)
# Add a real delete action to the actual saved-course chips.
oldchip="<TouchableOpacity key={`${norm(x.name)}-${i}`} onPress={()=>loadSaved(x)}"
if oldchip in s:
 s=s.replace(oldchip,"<View key={`${norm(x.name)}-${i}`} style={{flexDirection:'row',alignItems:'center'}}><TouchableOpacity onPress={()=>loadSaved(x)}",1)
 end="<Text numberOfLines={1} style={{fontSize:11,fontWeight:'900',color:C.text,maxWidth:118}}>{x.name}</Text></TouchableOpacity>"
 if end not in s:end="<Text numberOfLines={1} style={{fontSize:11,fontWeight:'900',color:C.text,maxWidth:145}}>{x.name}</Text></TouchableOpacity>"
 if end in s:
  repl=end+"<TouchableOpacity onPress={()=>{setSavedCourses(a=>a.filter((_,k)=>k!==i));if(norm(course)===norm(x.name)){setCourse('');setRealCourse&&setRealCourse(null);AsyncStorage.removeItem('caddieos.realCourse').catch(()=>{})}}} style={{padding:7}}><Text style={{fontSize:9,fontWeight:'900',color:'#8B1E1E'}}>DELETE</Text></TouchableOpacity></View>"
  s=s.replace(end,repl,1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 84',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.84"',t,count=1);g.write_text(t)
print('Build 84 actual importer -> active realCourse wiring applied')
