from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD72_EMPTY_ROUTINE' not in s:
    s=s.replace('const BUILD71_PLAYER_ONE=true;', 'const BUILD71_PLAYER_ONE=true;\nconst BUILD72_EMPTY_ROUTINE=true;', 1)

old="const ROUTINE_DEFAULT=['Target','Lie','Club','Picture','Commit','Breathe','Reset','Next'];"
new="const ROUTINE_LEGACY=['Target','Lie','Club','Picture','Commit','Breathe','Reset','Next'];\nconst ROUTINE_DEFAULT=Array(8).fill('');"
if old not in s:
    raise SystemExit('Build 72: routine default marker missing')
s=s.replace(old,new,1)

# Existing installations carrying the former sample routine migrate to blanks;
# genuinely personalised routines remain untouched.
old_load='routineSteps:setRoutineSteps,courseInfo:setCourseInfo,savedCourses:setSavedCourses'
new_load="routineSteps:v=>setRoutineSteps(JSON.stringify(v)===JSON.stringify(ROUTINE_LEGACY)?ROUTINE_DEFAULT:v),courseInfo:setCourseInfo,savedCourses:setSavedCourses"
if old_load not in s:
    raise SystemExit('Build 72: routine load marker missing')
s=s.replace(old_load,new_load,1)

# Pass Course Info state into the course importer.
s=s.replace("open,setTargets}}/>", "open,setTargets,courseInfo,setCourseInfo}}/>", 1)
s=s.replace("function Course({course,setCourse,tee,setTee,hole,setHole,gps,getGPS,open,markTarget,currentTarget,targets,setTargets,savedCourses,setSavedCourses})", "function Course({course,setCourse,tee,setTee,hole,setHole,gps,getGPS,open,markTarget,currentTarget,targets,setTargets,savedCourses,setSavedCourses,courseInfo,setCourseInfo})", 1)

# Auto-fill practical course details from directory data when supplied.
needle="setCourse(name);setSource('directory');"
autofill="""setCourse(name);setCourseInfo(prev=>({...prev,phone:String(c?.phone??c?.phone_number??c?.telephone??prev.phone??''),email:String(c?.email??c?.contact_email??prev.email??''),membership:String(c?.membership??c?.access??c?.visitor_policy??prev.membership??''),cart:String(c?.cart_available??c?.carts??prev.cart??''),hire:String(c?.club_hire??c?.rental_clubs??prev.hire??''),proshop:String(c?.pro_shop??c?.proshop??prev.proshop??''),pro:String(c?.golf_pro??c?.professional??prev.pro??''),overview:String(c?.description??c?.overview??c?.notes??prev.overview??'')}));setSource('directory');"""
if needle not in s:
    raise SystemExit('Build 72: course import marker missing')
s=s.replace(needle,autofill,1)
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 72',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.72"',t,count=1)
    g.write_text(t)
print('Build 72 empty custom routine applied')
