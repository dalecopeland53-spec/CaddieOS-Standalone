from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD79_STARTUP_FIX' not in s:
    s=s.replace('const BUILD78_REAL_COURSE_CADDIE=true;', 'const BUILD78_REAL_COURSE_CADDIE=true;\nconst BUILD79_STARTUP_FIX=true;', 1)

# Build 78 inserted a useEffect before Shell(), which calls React hooks outside a
# component and crashes immediately at runtime. Remove that injected effect and put
# the cached real-course state/effect safely inside Shell.
s=re.sub(r"useEffect\(\(\)=>\{cachedOpenGolfCourse\(\)\.then\(x=>\{if\(x\)setRealCourse\(x\)\}\)\.catch\(\(\)=>\{\}\)\},\[\]\);\n",'',s,count=1)

shell="function Shell(){const{height,width}=useWindowDimensions(),insets=useSafeAreaInsets(),compact=height<780||width<380;"
if shell not in s: raise SystemExit('Shell anchor not found')
if 'const[realCourse,setRealCourse]=useState(null);' not in s:
    s=s.replace(shell,shell+"\n const[realCourse,setRealCourse]=useState(null);",1)

first_effect=' useEffect(()=>{\n  let active=true;'
if first_effect not in s: raise SystemExit('Shell effect anchor not found')
load_effect=" useEffect(()=>{let mounted=true;cachedOpenGolfCourse().then(x=>{if(mounted&&x)setRealCourse(x)}).catch(()=>{});return()=>{mounted=false}},[]);\n"
if load_effect.strip() not in s:
    s=s.replace(first_effect,load_effect+first_effect,1)

# Keep the existing app stable: Build 79 fixes startup first. Build 78 helpers remain
# available for the real-course/caddie link and are loaded only from inside Shell.
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 79',t,count=1);t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.79"',t,count=1);g.write_text(t)
print('Build 79 startup crash fix applied')
