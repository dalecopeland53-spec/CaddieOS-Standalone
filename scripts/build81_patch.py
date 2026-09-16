from pathlib import Path
import re
p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD81_REAL_ONLY' not in s:s=s.replace('const BUILD80_REAL_COURSE_SELECT=true;','const BUILD80_REAL_COURSE_SELECT=true;\nconst BUILD81_REAL_ONLY=true;',1)
# Round must not present generated geometry as a real course. If no API course is loaded,
# replace the graphic area with an explicit Select Course state and route to COURSE.
old="<View style={s.mapWrap}>"
new="<View style={s.mapWrap}>{!realCourse?<TouchableOpacity onPress={()=>open('COURSE')} style={{flex:1,alignItems:'center',justifyContent:'center',padding:14}}><Text style={{fontSize:17,fontWeight:'900',color:C.white,textAlign:'center'}}>SELECT COURSE</Text><Text style={{fontSize:10,color:C.white,textAlign:'center',marginTop:8}}>Choose a real course before starting the round.</Text></TouchableOpacity>:null}"
if old in s and 'Choose a real course before starting the round.' not in s:s=s.replace(old,new,1)
# Hide legacy generated map children when no real course is loaded by dimming them completely.
# We retain their layout only after a course is loaded until geometry renderer is populated.
marker="{(()=>{const shapes=["
if marker in s:s=s.replace(marker,"{realCourse&&(()=>{const shapes=[",1)
# Do not show generic caddie recommendation as though it came from real course data.
s=s.replace("{realCourse?buildRealCourseAdvice({hole:i+1,realCourse,distance:targetDistances.center,playing,club,wind,windDir,units}):caddieText}","{realCourse?buildRealCourseAdvice({hole:i+1,realCourse,distance:targetDistances.center,playing,club,wind,windDir,units}):'Select a real course to activate course-aware Caddie advice.'}",1)
p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
 t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 81',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.81"',t,count=1);g.write_text(t)
print('Build 81 real-course-only state applied')
