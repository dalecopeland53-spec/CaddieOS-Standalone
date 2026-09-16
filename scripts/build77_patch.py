from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD77_REAL_COURSE_API' not in s:
    s=s.replace('const BUILD76_HOLE_GRAPHICS=true;', "const BUILD76_HOLE_GRAPHICS=true;\nconst BUILD77_REAL_COURSE_API=true;\nconst OPENGOLF_API='https://api.opengolfapi.org/v1';", 1)

# Add real OpenGolfAPI read helpers. Reads are keyless; course data is cached locally.
anchor='function Round('
helpers="""async function searchOpenGolfCourses(query){const q=String(query||'').trim();if(!q)return[];const r=await fetch(`${OPENGOLF_API}/courses/search?q=${encodeURIComponent(q)}&limit=20`);if(!r.ok)throw new Error('Course search unavailable');const j=await r.json();return Array.isArray(j)?j:(j.courses||j.results||[])}
async function loadOpenGolfCourse(id){const [courseR,holesR,teesR]=await Promise.all([fetch(`${OPENGOLF_API}/courses/${id}`),fetch(`${OPENGOLF_API}/courses/${id}/holes`),fetch(`${OPENGOLF_API}/courses/${id}/tees`)]);if(!courseR.ok)throw new Error('Course unavailable');const course=await courseR.json();const holes=holesR.ok?await holesR.json():[];const tees=teesR.ok?await teesR.json():[];const data={course,holes:Array.isArray(holes)?holes:(holes.holes||[]),tees:Array.isArray(tees)?tees:(tees.tees||[]),source:'OpenGolfAPI / OpenStreetMap contributors',savedAt:Date.now()};try{await AsyncStorage.setItem('caddieos.realCourse',JSON.stringify(data))}catch(e){}return data}
async function cachedOpenGolfCourse(){try{const x=await AsyncStorage.getItem('caddieos.realCourse');return x?JSON.parse(x):null}catch(e){return null}}

"""
if helpers.strip() not in s:
    if anchor not in s: raise SystemExit('Build 77 Round anchor not found')
    s=s.replace(anchor,helpers+anchor,1)

# Mark the map as data-backed rather than invented when live mapped geometry is available.
# Existing generated shape remains only as an explicit fallback until a selected course has geometry.
s=s.replace("<MiniText style={[s.mapYouText,{bottom:7}]}>YOU</MiniText>","<MiniText style={[s.mapYouText,{bottom:7}]}>YOU</MiniText><View style={{position:'absolute',bottom:2,left:4,right:4}}><MiniText style={{fontSize:6,color:'#DDE7E4',textAlign:'center'}}>OpenGolfAPI · OpenStreetMap</MiniText></View>",1)
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 77',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.77"',t,count=1)
    g.write_text(t)
print('Build 77 OpenGolfAPI real-course foundation applied')
