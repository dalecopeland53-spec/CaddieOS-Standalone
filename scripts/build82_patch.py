from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD82_IMPORT_TO_ROUND' not in s:s=s.replace('const BUILD81_REAL_ONLY=true;','const BUILD81_REAL_ONLY=true;\nconst BUILD82_IMPORT_TO_ROUND=true;',1)
# When a directory/API course is imported, persist the full real-course payload in the
# same cache consumed by Shell/Round. This closes the import -> active course gap.
# Hook common importer success points without changing approved UI.
patterns=[
("setCourse(name);setTee(match||tee);", "setCourse(name);setTee(match||tee);if(typeof data==='object'&&data){setRealCourse&&setRealCourse(data);AsyncStorage.setItem(OPENGOLF_CACHE,JSON.stringify(data)).catch(()=>{});}"),
("setCourse(name);", "setCourse(name);if(typeof data==='object'&&data){setRealCourse&&setRealCourse(data);AsyncStorage.setItem(OPENGOLF_CACHE,JSON.stringify(data)).catch(()=>{});}")]
for a,b in patterns:
 if a in s and 'setRealCourse&&setRealCourse(data)' not in s:s=s.replace(a,b,1)
# Course component must receive real-course setters wherever importer lives.
s=re.sub(r'function Course\(\{([^}]*)\}\)',lambda m:'function Course({'+(m.group(1)+',realCourse,setRealCourse' if 'setRealCourse' not in m.group(1) else m.group(1))+'})',s,count=1)
# Remove misleading generic advice when there is no genuine centre distance.
s=s.replace("150 metres playing distance to a centre pin. 7 Iron. Favour the centre of the green. Pick the target, picture the shot and commit.","Start live GPS and select a real course for Caddie advice.")
# If realCourse is restored, sync its course name so Round and Course agree.
needle="cachedOpenGolfCourse().then(x=>{if(mounted&&x)setRealCourse(x)})"
if needle in s:s=s.replace(needle,"cachedOpenGolfCourse().then(x=>{if(mounted&&x){setRealCourse(x);const nm=x.course?.name||x.name||x.course_name;if(nm)setCourse(nm)}})",1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 82',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.82"',t,count=1);g.write_text(t)
print('Build 82 import-to-round wiring applied')
