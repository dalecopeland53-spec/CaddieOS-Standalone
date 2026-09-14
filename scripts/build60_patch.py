from pathlib import Path
import re

app=Path('CaddieOS/App.js')
text=app.read_text()

def must(old,new,label):
    global text
    if old not in text:
        raise SystemExit(f'Build 60 patch marker missing: {label}')
    text=text.replace(old,new,1)

marker='function Header({go})'
helpers="""
const Panel=({children})=><View style={s.panel}>{children}</View>;
const Label=({text})=><Text style={s.label}>{text}</Text>;
const Chip=({active,text,onPress})=><TouchableOpacity onPress={onPress} style={[s.chip,active&&{backgroundColor:C.gold}]}><Text style={[s.chipText,active&&{color:C.dark}]}>{text}</Text></TouchableOpacity>;
const Mini=({text,onPress})=><TouchableOpacity onPress={onPress} style={{width:40,height:40,borderRadius:9,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'}}><Text style={{fontSize:22,fontWeight:'900',color:C.white}}>{text}</Text></TouchableOpacity>;
"""
if 'const Panel=({children})' not in text:
    if marker not in text: raise SystemExit('Build 60: Header marker missing')
    text=text.replace(marker,helpers+'\n'+marker,1)

must("import React,{useEffect,useMemo,useState}from'react';","import React,{useEffect,useMemo,useRef,useState}from'react';",'React useRef')
must("[targets,setTargets]=useState(blankTargets()),[gps,setGps]=useState(null);","[targets,setTargets]=useState(blankTargets()),[gps,setGps]=useState(null),[gpsLive,setGpsLive]=useState(false);",'GPS state')
must("const[warmDone,setWarmDone]=useState([]),[routineSteps,setRoutineSteps]=useState(ROUTINE_DEFAULT),[routineDone,setRoutineDone]=useState([]);","const[warmDone,setWarmDone]=useState([]),[routineSteps,setRoutineSteps]=useState(ROUTINE_DEFAULT),[routineDone,setRoutineDone]=useState([]);\n const gpsWatch=useRef(null);\n const[savedCourses,setSavedCourses]=useState([]);",'saved courses state')
must("Object.entries({units:setUnits,player:setPlayer,email:setEmail,handicap:setHandicap,bag:setBag,course:setCourse,tee:setTee,targets:setTargets,scores:setScores,putts:setPutts,gir:setGir,fw:setFw,pen:setPen,notes:setNotes,roundLog:setRoundLog,practiceHistory:setPracticeHistory,routineSteps:setRoutineSteps,courseInfo:setCourseInfo})","Object.entries({units:setUnits,player:setPlayer,email:setEmail,handicap:setHandicap,bag:setBag,course:setCourse,tee:setTee,targets:setTargets,scores:setScores,putts:setPutts,gir:setGir,fw:setFw,pen:setPen,notes:setNotes,roundLog:setRoundLog,practiceHistory:setPracticeHistory,routineSteps:setRoutineSteps,courseInfo:setCourseInfo,savedCourses:setSavedCourses})",'load saved courses')
must("AsyncStorage.setItem(STORAGE,JSON.stringify({units,player,email,handicap,bag,course,tee,targets,scores,putts,gir,fw,pen,notes,roundLog,practiceHistory,routineSteps,courseInfo}))","AsyncStorage.setItem(STORAGE,JSON.stringify({units,player,email,handicap,bag,course,tee,targets,scores,putts,gir,fw,pen,notes,roundLog,practiceHistory,routineSteps,courseInfo,savedCourses}))",'persist saved courses')
must("[units,player,email,handicap,bag,course,tee,targets,scores,putts,gir,fw,pen,notes,roundLog,practiceHistory,routineSteps,courseInfo]);","[units,player,email,handicap,bag,course,tee,targets,scores,putts,gir,fw,pen,notes,roundLog,practiceHistory,routineSteps,courseInfo,savedCourses]);",'saved courses dependencies')

oldgps="const getGPS=async()=>{if(Platform.OS==='android'){const ok=await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION);if(ok!==PermissionsAndroid.RESULTS.GRANTED)return Alert.alert('Location permission','Allow location access so CaddieOS can use GPS.')}Geolocation.getCurrentPosition(p=>setGps({lat:p.coords.latitude.toFixed(6),lon:p.coords.longitude.toFixed(6),acc:Math.round(p.coords.accuracy)}),()=>Alert.alert('GPS','Could not get your current position.'),{enableHighAccuracy:true,timeout:15000,maximumAge:3000})};"
newgps="""const allowGPS=async()=>{if(Platform.OS!=='android')return true;const ok=await PermissionsAndroid.request(PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION);if(ok!==PermissionsAndroid.RESULTS.GRANTED){Alert.alert('Location permission','Allow location access so CaddieOS can use GPS.');return false}return true};
 const setGPSPoint=p=>setGps({lat:p.coords.latitude.toFixed(6),lon:p.coords.longitude.toFixed(6),acc:Math.round(p.coords.accuracy)});
 const getGPS=async()=>{if(!await allowGPS())return;Geolocation.getCurrentPosition(setGPSPoint,()=>Alert.alert('GPS','Could not get your current position.'),{enableHighAccuracy:true,timeout:15000,maximumAge:3000})};
 const startLiveGPS=async()=>{if(!await allowGPS())return;if(gpsWatch.current!==null)Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=Geolocation.watchPosition(setGPSPoint,()=>{}, {enableHighAccuracy:true,distanceFilter:2,interval:2500,fastestInterval:1200,maximumAge:1500});setGpsLive(true)};
 const stopLiveGPS=()=>{if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}setGpsLive(false)};"""
must(oldgps,newgps,'live GPS engine')
must("return()=>{active=false;Voice.destroy().then(Voice.removeAllListeners).catch(()=>{})};","return()=>{active=false;if(gpsWatch.current!==null)Geolocation.clearWatch(gpsWatch.current);Voice.destroy().then(Voice.removeAllListeners).catch(()=>{})};",'GPS cleanup')
must("{page==='ROUND'&&<Round hole={hole} setHole={setHole} result={result} units={units} gps={gps} getGPS={getGPS} targetDistances={targetDistances} open={open}/>} ","{page==='ROUND'&&<Round hole={hole} setHole={setHole} result={result} units={units} gps={gps} gpsLive={gpsLive} startLiveGPS={startLiveGPS} stopLiveGPS={stopLiveGPS} targetDistances={targetDistances} open={open}/>} ",'Round props')
must("{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open,setTargets}}/>}","{page==='COURSE'&&<Course {...{course,setCourse,tee,setTee,hole,setHole,gps,getGPS,markTarget,currentTarget,open,targets,setTargets,savedCourses,setSavedCourses}}/>}",'Course props')

round_rx=r"function Round\(\{hole,setHole,result,units,gps,getGPS,targetDistances,open\}\)\{.*?\nfunction Caddie"
round_new="""function Round({hole,setHole,result,units,gps,gpsLive,startLiveGPS,stopLiveGPS,targetDistances,open}){const holes=Array.from({length:18},(_,i)=>String(i+1));return <><Title kicker=\"ROUND\" title={`Hole ${hole}`} sub={gpsLive?`LIVE GPS${gps?.acc?` · ±${gps.acc} m`:''}`:'GPS ready when you are'}/><View style={{flexDirection:'row',flexWrap:'wrap',gap:5,marginBottom:9}}>{holes.map(x=><TouchableOpacity key={x} onPress={()=>setHole(x)} style={{width:'15.2%',minHeight:34,borderRadius:8,alignItems:'center',justifyContent:'center',backgroundColor:String(hole)===x?C.gold:'#153348',borderWidth:1,borderColor:String(hole)===x?C.gold:'#315064'}}><Text style={{fontSize:10,fontWeight:'900',color:String(hole)===x?C.dark:C.white}}>{x}</Text></TouchableOpacity>)}</View><View style={s.panel}><Text style={s.panelTitle}>GREEN DISTANCES</Text><View style={s.distanceRow}><Stat a={targetDistances.front??'—'} b=\"FRONT\"/><Stat a={targetDistances.center??'—'} b=\"CENTRE\"/><Stat a={targetDistances.back??'—'} b=\"BACK\"/></View><Text style={s.small}>{units==='METRES'?'metres':'yards'} · {gps?`${gps.lat}, ${gps.lon}`:'No position yet'}</Text></View><View style={s.panel}><Text style={s.panelTitle}>CADDIE RECOMMENDATION</Text><Text style={s.bigClub}>{result.club}</Text><Text style={s.cardSub}>Playing {result.y} {units==='METRES'?'m':'yd'}</Text></View><Btn text={gpsLive?'STOP LIVE GPS':'START LIVE GPS'} onPress={gpsLive?stopLiveGPS:startLiveGPS}/><Btn text=\"OPEN CADDIE\" onPress={()=>open('CADDIE')} outline/><Btn text=\"SCORE THIS HOLE\" onPress={()=>open('SCORE')} outline/></>}
function Caddie"""
text,count=re.subn(round_rx,round_new,text,count=1,flags=re.S)
if count!=1: raise SystemExit('Build 60 patch marker missing: Round function')

must("function Course({course,setCourse,tee,setTee,hole,setHole,gps,getGPS,open,markTarget,currentTarget,setTargets}){","function Course({course,setCourse,tee,setTee,hole,setHole,gps,getGPS,open,markTarget,currentTarget,targets,setTargets,savedCourses,setSavedCourses}){",'Course signature')
course_state="const[q,setQ]=useState(''),[results,setResults]=useState([]),[searching,setSearching]=useState(false),[importing,setImporting]=useState(false);"
course_state_new=course_state+"\n useEffect(()=>{if(!course.trim())return;setSavedCourses(prev=>{const entry={name:course.trim(),tee,targets};const i=prev.findIndex(x=>x.name.toLowerCase()===entry.name.toLowerCase());const next=i>=0?prev.map((x,k)=>k===i?entry:x):[entry,...prev].slice(0,50);return JSON.stringify(next)===JSON.stringify(prev)?prev:next})},[course,tee,targets]);\n const loadSaved=x=>{setCourse(x.name);setTee(x.tee||'White');setTargets(Array.isArray(x.targets)&&x.targets.length===18?x.targets:blankTargets());setHole('1');Alert.alert('Course loaded',`${x.name} loaded from your CaddieOS library.`)};"
must(course_state,course_state_new,'local course library')
must("Search OpenGolfAPI, then save the selected course locally. Manual mapping remains available.","Search online or load a saved course. Tap a search result to import it.",'directory helper')
must("Contains data from OpenGolfAPI (opengolfapi.org).","OpenGolfAPI course directory.",'directory credit')
must("</Panel>\n <Panel><Label text=\"COURSE NAME\"/>","{savedCourses.length?<View style={{marginTop:6}}><Text style={s.panelTitle}>SAVED COURSES · {savedCourses.length}</Text><View style={s.chips}>{savedCourses.slice(0,6).map(x=><Chip key={x.name} active={x.name===course} text={x.name} onPress={()=>loadSaved(x)}/>)}</View></View>:null}</Panel>\n <Panel><Label text=\"COURSE NAME\"/>",'saved course panel')
must("⌖  GET GPS POSITION","⌖  GET MAPPING GPS",'mapping GPS label')
must("Stand at each point and save its GPS coordinate. Imported courses can still be corrected here.","Mapping GPS only: stand at Front, Centre and Back, then save each point.",'mapping helper')

app.write_text(text)

props=Path('CaddieOS/android/gradle.properties')
ptxt=props.read_text().replace('newArchEnabled=true','newArchEnabled=false')
if 'newArchEnabled=false' not in ptxt: ptxt+='\nnewArchEnabled=false\n'
props.write_text(ptxt)

gradle=Path('CaddieOS/android/app/build.gradle')
g=gradle.read_text()
g=re.sub(r'versionCode\s+\d+','versionCode 60',g)
g=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.60"',g)
gradle.write_text(g)

manifest=Path('CaddieOS/android/app/src/main/AndroidManifest.xml')
m=manifest.read_text()
perms='<uses-permission android:name="android.permission.RECORD_AUDIO" />\n    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />\n    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />\n    <uses-permission android:name="android.permission.INTERNET" />'
if 'android.permission.RECORD_AUDIO' not in m:
    m=m.replace('<application',perms+'\n    <application',1)
elif 'android.permission.INTERNET' not in m:
    m=m.replace('<application','<uses-permission android:name="android.permission.INTERNET" />\n    <application',1)
manifest.write_text(m)
