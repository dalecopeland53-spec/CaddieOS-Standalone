from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD84_ACTIVE_COURSE_FIX' not in s:s=s.replace('const BUILD83_COURSE_MANAGEMENT=true;','const BUILD83_COURSE_MANAGEMENT=true;\nconst BUILD84_ACTIVE_COURSE_FIX=true;',1)
# ONE shared realCourse state: Course writes it, Round reads it.
s=re.sub(r'function Course\(\{([^}]*)\}\)',lambda m:'function Course({'+(m.group(1)+',realCourse,setRealCourse' if 'setRealCourse' not in m.group(1) else m.group(1))+'})',s,count=1)
m=re.search(r"\{page==='COURSE'&&<Course \{\.\.\.\{([^}]*)\}\}/>\}",s)
if not m:raise SystemExit('Build84 COURSE route missing')
props=m.group(1)
if 'realCourse' not in props:
 newprops=props.rstrip(',')+',realCourse,setRealCourse';s=s[:m.start()]+"{page==='COURSE'&&<Course {...{"+newprops+"}}/>}"+s[m.end():]
# Critical missing link: actual ROUND route must receive shared realCourse.
m=re.search(r"\{page==='ROUND'&&<Round\s+([^>]*?)/>\}",s,re.S)
if not m:raise SystemExit('Build84 ROUND route missing')
route=m.group(0)
if 'realCourse=' not in route:
 route=route[:-3]+' realCourse={realCourse}/>}'
 s=s[:m.start()]+route+s[m.end():]
# Visible importer creates one normalized payload, activates it immediately, and persists it.
old="const c=cr.ok?await cr.json():item,hj=hr.ok?await hr.json():[],tj=tr.ok?await tr.json():[];const name=c?.name||c?.course_name||item?.name||item?.course_name||'Golf Course';setCourse(name);"
new="const c=cr.ok?await cr.json():item,hj=hr.ok?await hr.json():[],tj=tr.ok?await tr.json():[];const hs=Array.isArray(hj)?hj:(hj?.holes||hj?.data||[]),tees=Array.isArray(tj)?tj:(tj?.tees||tj?.data||[]),real={course:c,holes:hs,tees,source:'OpenGolfAPI / OpenStreetMap contributors',savedAt:Date.now()};setRealCourse(real);AsyncStorage.setItem('caddieos.realCourse',JSON.stringify(real)).catch(()=>{});const name=c?.name||c?.course_name||item?.name||item?.course_name||'Golf Course';setCourse(name);"
if old not in s:raise SystemExit('Build84 importer missing')
s=s.replace(old,new,1)
s=s.replace("const hs=Array.isArray(hj)?hj:(hj?.holes||hj?.data||[]);if(Array.isArray(hs)&&hs.length)","if(Array.isArray(hs)&&hs.length)",1)
s=s.replace("const tees=Array.isArray(tj)?tj:(tj?.tees||tj?.data||[]);if(Array.isArray(tees)&&tees.length)","if(Array.isArray(tees)&&tees.length)",1)
# Restore saved course into the same state.
s=s.replace("const loadSaved=x=>{setCourse(x.name);","const loadSaved=x=>{setCourse(x.name);if(x.realCourse){setRealCourse(x.realCourse);AsyncStorage.setItem('caddieos.realCourse',JSON.stringify(x.realCourse)).catch(()=>{})}else{setRealCourse(null);AsyncStorage.removeItem('caddieos.realCourse').catch(()=>{})}",1)
s=s.replace("const entry={name,tee,targets,courseMetres};","const entry={name,tee,targets,courseMetres,realCourse};",1)
s=s.replace("const entry={name,tee,targets};","const entry={name,tee,targets,realCourse};",1)
# Startup restores payload and name.
needle="cachedOpenGolfCourse().then(x=>{if(mounted&&x){setRealCourse(x);const nm=x.course?.name||x.name||x.course_name;if(nm)setCourse(nm)}})"
if needle not in s:s=s.replace("cachedOpenGolfCourse().then(x=>{if(mounted&&x)setRealCourse(x)})",needle,1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 84',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.84\"',t,count=1);g.write_text(t)
print('Build 84 final Course -> shared state -> Round fix applied')
