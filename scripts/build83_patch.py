from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD83_COURSE_MANAGEMENT' not in s:s=s.replace('const BUILD82_IMPORT_TO_ROUND=true;','const BUILD82_IMPORT_TO_ROUND=true;\nconst BUILD83_COURSE_MANAGEMENT=true;',1)
# Ensure Course receives the active real-course state.
s=re.sub(r'function Course\(\{([^}]*)\}\)',lambda m:'function Course({'+(m.group(1)+',realCourse,setRealCourse' if 'setRealCourse' not in m.group(1) else m.group(1))+'})',s,count=1)
# Any loaded OpenGolf course becomes active immediately and is cached for Round/startup.
choose_old="setRealCourse(d);setCourse(d.course?.name||x.name||q);setRows([])"
choose_new="setRealCourse(d);setCourse(d.course?.name||x.name||q);AsyncStorage.setItem(OPENGOLF_CACHE,JSON.stringify(d)).catch(()=>{});setRows([])"
if choose_old in s:s=s.replace(choose_old,choose_new,1)
# Add a single helper used by saved-course delete controls. Active course deletion also clears Round cache.
anchor='function RealCoursePicker('
helper="function deleteSavedCourse83(x,savedCourses,setSavedCourses,course,setCourse,realCourse,setRealCourse){const name=String(x?.name||'');const next=(savedCourses||[]).filter(z=>z!==x&&String(z?.name||'')!==name);setSavedCourses(next);if(String(course||'')===name||String(realCourse?.course?.name||realCourse?.name||'')===name){setCourse('');setRealCourse&&setRealCourse(null);AsyncStorage.removeItem(OPENGOLF_CACHE).catch(()=>{})}return next}\n\n"
if anchor in s and 'function deleteSavedCourse83' not in s:s=s.replace(anchor,helper+anchor,1)
# Replace common saved-course row press-only render with SELECT + DELETE when recognizable.
pat=r"\{savedCourses\.map\(\(x,i\)=>\s*<TouchableOpacity([^>]*?)onPress=\{\(\)=>loadSaved\(x\)\}([^>]*)>(.*?)</TouchableOpacity>\)\}"
m=re.search(pat,s,re.S)
if m:
 body=m.group(3)
 repl="{savedCourses.map((x,i)=><View key={String(x?.name||i)} style={{flexDirection:'row',alignItems:'center',gap:6}}><TouchableOpacity style={{flex:1}} onPress={()=>loadSaved(x)}>"+body+"</TouchableOpacity><TouchableOpacity onPress={()=>deleteSavedCourse83(x,savedCourses,setSavedCourses,course,setCourse,realCourse,setRealCourse)} style={{padding:9}}><Text style={{fontWeight:'900',color:'#8B1E1E'}}>DELETE</Text></TouchableOpacity></View>)}"
 s=s[:m.start()]+repl+s[m.end():]
# Pass state into Course route if omitted.
s=s.replace('courseMetres,setCourseMetres,coursePars,setCoursePars,courseSI,setCourseSI}}/>','courseMetres,setCourseMetres,coursePars,setCoursePars,courseSI,setCourseSI,realCourse,setRealCourse}}/>',1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 83',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.83"',t,count=1);g.write_text(t)
print('Build 83 course activation and deletion applied')
