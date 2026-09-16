from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD78_REAL_COURSE_CADDIE' not in s:
    s=s.replace('const BUILD77_REAL_COURSE_API=true;', 'const BUILD77_REAL_COURSE_API=true;\nconst BUILD78_REAL_COURSE_CADDIE=true;', 1)

# Normalize OpenGolf hole data into a compact context the existing caddie can use.
anchor='function Round('
helpers="""function openGolfHoleContext(realCourse,holeNo){try{const list=realCourse?.holes||[];const h=list.find(x=>Number(x.hole??x.number)===Number(holeNo))||list[Number(holeNo)-1]||{};const hazards=h.hazards||h.features||[];const names=hazards.map(x=>x.type||x.kind||x.name).filter(Boolean).slice(0,4);return {par:Number(h.par||0)||null,strokeIndex:Number(h.handicap||h.stroke_index||h.si||0)||null,front:h.front_distance??h.green_front??null,center:h.center_distance??h.green_center??null,back:h.back_distance??h.green_back??null,hazards:names,raw:h}}catch(e){return {hazards:[]}}}
function buildRealCourseAdvice({hole,realCourse,distance,playing,club,wind,windDir,units,lie='Fairway'}){const h=openGolfHoleContext(realCourse,hole);const u=units==='METRES'?'metres':'yards';const parts=[];if(distance!=null)parts.push(`${distance} ${u} to centre`);if(playing!=null&&Number(playing)!==Number(distance))parts.push(`playing ${playing} ${u}`);if(wind>0)parts.push(`${wind} wind ${windDir||''}`.trim());if(h.hazards.length)parts.push(`hazards: ${h.hazards.join(', ')}`);if(lie&&lie!=='Fairway')parts.push(`${lie} lie`);if(club&&club!=='—')parts.push(`${club}`);parts.push('Pick the safest target, picture the shot and commit.');return parts.join('. ')}

"""
if 'function buildRealCourseAdvice' not in s:
    if anchor not in s: raise SystemExit('Build 78 Round anchor not found')
    s=s.replace(anchor,helpers+anchor,1)

# Round now accepts cached real-course data and uses it in the visible advice whenever available.
s=s.replace('function Round({hole,setHole,units,gps,gpsLive,startLiveGPS,stopLiveGPS,targetDistances,wind,windDir,bag,tee,open,ask,listening,caddieText,scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,coursePars,courseSI})',
'''function Round({hole,setHole,units,gps,gpsLive,startLiveGPS,stopLiveGPS,targetDistances,wind,windDir,bag,tee,open,ask,listening,caddieText,scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,coursePars,courseSI,realCourse})''',1)
old="""<MiniText numberOfLines={3} style={{fontSize:8.5,lineHeight:11,color:C.text,fontWeight:'700'}}>{caddieText}</MiniText>"""
new="""<MiniText numberOfLines={3} style={{fontSize:8.5,lineHeight:11,color:C.text,fontWeight:'700'}}>{realCourse?buildRealCourseAdvice({hole:i+1,realCourse,distance:targetDistances.center,playing,club,wind,windDir,units}):caddieText}</MiniText>"""
if old in s:s=s.replace(old,new,1)

# Load the locally cached OpenGolf course at app start, then pass it into Round.
# Keep this defensive so older state/layout remains intact.
state_anchor="const [screen,setScreen]"
if state_anchor in s and 'setRealCourse' not in s:
    s=s.replace(state_anchor,"const [realCourse,setRealCourse]=useState(null);\n"+state_anchor,1)
    # Add a mount effect near the first existing effect if possible.
    effect_pos=s.find('useEffect(')
    if effect_pos!=-1:
        s=s[:effect_pos]+"useEffect(()=>{cachedOpenGolfCourse().then(x=>{if(x)setRealCourse(x)}).catch(()=>{})},[]);\n"+s[effect_pos:]

# Pass realCourse into any Round component invocation.
s=re.sub(r'<Round\s+([^>]*?)\s*/>',lambda m: m.group(0) if 'realCourse=' in m.group(0) else '<Round '+m.group(1)+' realCourse={realCourse}/>',s,count=1,flags=re.S)
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 78',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.78"',t,count=1);g.write_text(t)
print('Build 78 real-course caddie advice link applied')
