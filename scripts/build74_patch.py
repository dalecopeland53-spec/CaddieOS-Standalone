from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD74_REVIEW_FIXES' not in s:
    s=s.replace('const BUILD73_COURSE_VIEW=true;', 'const BUILD73_COURSE_VIEW=true;\nconst BUILD74_REVIEW_FIXES=true;', 1)

# Course-specific scorecard state.
old="const[bag,setBag]=useState(DEFAULT_BAG),[course,setCourse]=useState(''),[tee,setTee]=useState('White'),[hole,setHole]=useState('1'),[targets,setTargets]=useState(blankTargets()),[courseMetres,setCourseMetres]=useState(Array(18).fill('')),[gps,setGps]=useState(null),[gpsLive,setGpsLive]=useState(false);"
new="const[bag,setBag]=useState(DEFAULT_BAG),[course,setCourse]=useState(''),[tee,setTee]=useState('White'),[hole,setHole]=useState('1'),[targets,setTargets]=useState(blankTargets()),[courseMetres,setCourseMetres]=useState(Array(18).fill('')),[coursePars,setCoursePars]=useState(PARS),[courseSI,setCourseSI]=useState(STROKE_INDEX),[gps,setGps]=useState(null),[gpsLive,setGpsLive]=useState(false);"
if old not in s: raise SystemExit('Build 74 course state marker missing')
s=s.replace(old,new,1)
s=s.replace("const[distance,setDistance]=useState('150'),[wind,setWind]=useState('0'),[windDir,setWindDir]=useState('HEAD'),[elev,setElev]=useState('0'),[lie,setLie]=useState('Fairway');", "const[distance,setDistance]=useState('150'),[wind,setWind]=useState('0'),[windDir,setWindDir]=useState('HEAD'),[elev,setElev]=useState('0'),[lie,setLie]=useState('Fairway'),[pinPos,setPinPos]=useState('CENTRE');", 1)
s=s.replace('courseMetres:setCourseMetres,scores:setScores', 'courseMetres:setCourseMetres,coursePars:setCoursePars,courseSI:setCourseSI,scores:setScores', 1)
s=s.replace('targets,courseMetres,scores,putts', 'targets,courseMetres,coursePars,courseSI,scores,putts', 2)
s=s.replace('targets,courseMetres,scores,putts', 'targets,courseMetres,coursePars,courseSI,scores,putts', 2)

# Natural golf speech: "185 out", "pin at the back", and "slight rough".
old_parse="const d=m(/(?:to|target|distance|playing)\\s+(\\d{2,3})/)||m(/(\\d{2,3})\\s*(?:yards?|yds?|metres?|meters?)/);if(d)S.setDistance(d);"
new_parse="const d=m(/(?:to|target|distance|playing)\\s+(\\d{2,3})/)||m(/(\\d{2,3})\\s*(?:yards?|yds?|metres?|meters?|out|away|to go)/)||m(/^\\s*(\\d{2,3})(?:\\s|$)/);if(d)S.setDistance(d);if(/pin(?:\\s+is)?(?:\\s+at)?\\s+(?:the\\s+)?back|back\\s+pin/.test(s))S.setPinPos?.('BACK');else if(/pin(?:\\s+is)?(?:\\s+at)?\\s+(?:the\\s+)?front|front\\s+pin/.test(s))S.setPinPos?.('FRONT');else if(/pin(?:\\s+is)?(?:\\s+at)?\\s+(?:the\\s+)?cent(?:re|er)|cent(?:re|er)\\s+pin/.test(s))S.setPinPos?.('CENTRE');"
if old_parse not in s: raise SystemExit('Build 74 speech marker missing')
s=s.replace(old_parse,new_parse,1)
s=s.replace("if(/light\\s+(rough|ruff|roth|roof)/.test(s))", "if(/(?:light|slight)\\s+(rough|ruff|roth|roof)/.test(s))", 1)
s=s.replace('parseSpeech(t,{setDistance,setWind,setWindDir,setElev,setLie})', 'parseSpeech(t,{setDistance,setWind,setWindDir,setElev,setLie,setPinPos})', 1)

# Give complete situational advice rather than a bare distance/club answer.
advice_new="""function advice(target,club,lie,w,dir,e,u,pin='CENTRE'){const unit=u==='METRES'?'metres':'yards';let t=`${target} ${unit} playing distance to a ${String(pin).toLowerCase()} pin. ${club}.`;if(lie==='Light Rough')t+=' Expect slightly reduced spin and carry; make clean contact.';else if(lie==='Rough')t+=' Allow for a heavier strike and reduced control.';else if(lie==='Deep Rough')t+=' Prioritise getting the ball safely back in play.';else if(lie.includes('Bunker'))t+=' Take enough loft and choose the safest exit.';if(n(w)){if(dir==='HEAD')t+=` ${w} ${u==='METRES'?'kilometre-per-hour':'mile-per-hour'} headwind: use the extra club and flight it lower.`;else if(dir==='TAIL')t+=` ${w} ${u==='METRES'?'kilometre-per-hour':'mile-per-hour'} tailwind: expect extra carry and less stopping power.`;else if(dir==='L→R')t+=` Wind left to right: start safely left of centre.`;else if(dir==='R→L')t+=` Wind right to left: start safely right of centre.`}if(n(e)>0)t+=` Uphill ${Math.abs(n(e))} percent.`;if(n(e)<0)t+=` Downhill ${Math.abs(n(e))} percent.`;t+=pin==='BACK'?' Favour the centre and do not chase the back edge.':pin==='FRONT'?' Carry the front safely; long is the better miss.':' Favour the centre of the green.';return t+' Pick the target, picture the shot and commit.'}"""
s,na=re.subn(r"function advice\(.*?\nfunction haversine",advice_new+'\nfunction haversine',s,count=1,flags=re.S)
if na!=1: raise SystemExit('Build 74 advice replacement failed')
s=s.replace("advice(result.y,result.club,lie,wind,windDir,elev,units)", "advice(result.y,result.club,lie,wind,windDir,elev,units,pinPos)", 1)
s=s.replace('[result,lie,wind,windDir,elev,units]', '[result,lie,wind,windDir,elev,units,pinPos]', 1)

# Pass all reviewed round, course and scorecard state.
s=s.replace("bag={bag} tee={tee} open={open}/>", "bag={bag} tee={tee} open={open} ask={ask} listening={listening} caddieText={caddieText} scores={scores} setScores={setScores} putts={putts} setPutts={setPutts} gir={gir} setGir={setGir} fw={fw} setFw={setFw} pen={pen} setPen={setPen} coursePars={coursePars}/>", 1)
s=s.replace('result,units,ask,listening,heard,caddieText,recordAdvice', 'result,units,ask,listening,heard,caddieText,recordAdvice,pinPos,setPinPos', 1)
s=s.replace('courseMetres,setCourseMetres}}/>', 'courseMetres,setCourseMetres,coursePars,setCoursePars,courseSI,setCourseSI}}/>', 1)
s=s.replace('courseMetres,setCourseMetres,handicap}}/>', 'courseMetres,setCourseMetres,coursePars,courseSI,handicap}}/>', 1)
s=s.replace('roundLog={roundLog} setRoundLog={setRoundLog} open={open}/>', 'roundLog={roundLog} setRoundLog={setRoundLog} open={open} setHole={setHole} coursePars={coursePars}/>', 1)

# Exact reviewed Round structure: tall map left, compact Caddie stack right, scoring below.
round_new="""function Round({hole,setHole,units,gps,gpsLive,startLiveGPS,stopLiveGPS,targetDistances,wind,windDir,bag,tee,open,ask,listening,caddieText,scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,coursePars}){const i=Math.max(0,Math.min(17,n(hole)-1)),par=coursePars[i]||PARS[i],arrow=windDir==='HEAD'?'↓':windDir==='TAIL'?'↑':windDir==='L→R'?'→':'←',valid=targetDistances.center!==null&&targetDistances.center!==undefined,playing=valid?playsLike(targetDistances.center,wind,0,'Fairway',windDir,units):null,club=valid?nearestClub(playing,bag,units)[0]:'—',setA=(setter,a,v)=>setter(a.map((x,k)=>k===i?v:x)),step=(setter,a,d)=>setA(setter,a,String(Math.max(0,n(a[i])+d))),next=()=>setHole(String(Math.min(18,i+2)));return <><View style={{flexDirection:'row',gap:7,height:505}}><View style={{width:'44%'}}><View style={[s.holeMap,{height:'100%',backgroundColor:'#12382F'}]}><View style={{position:'absolute',top:58,width:105,height:360,backgroundColor:'#4C9461',borderRadius:52,transform:[{rotate:'3deg'}]}}/><View style={[s.mapGreen,{top:20,width:100,height:54}]}/><View style={[s.mapLine,{top:48,height:365}]}/><Text style={[s.mapFlag,{top:35}]}>⚑</Text><View style={[s.mapYou,{bottom:35,width:24,height:24,borderRadius:12}]}/><Text style={[s.mapYouText,{bottom:13}]}>YOU</Text><View style={{position:'absolute',top:90,left:7,backgroundColor:'rgba(4,19,30,.82)',borderRadius:7,padding:5}}><Text style={{color:C.white,fontWeight:'900',fontSize:11}}>{targetDistances.center??'—'} {units==='METRES'?'m':'yd'}</Text></View></View></View><View style={{flex:1,gap:6}}><View style={[s.panel,{marginBottom:0,padding:8}]}><View style={{flexDirection:'row',alignItems:'center',justifyContent:'space-between'}}><TouchableOpacity style={[s.holeStep,{width:31,height:31}]} onPress={()=>setHole(String(Math.max(1,i)))}><Text style={s.holeStepText}>‹</Text></TouchableOpacity><View style={s.center}><Text style={s.cardTitle}>Hole {i+1}</Text><Text style={s.small}>Par {par} · S.I. {courseSI?.[i]||STROKE_INDEX[i]}</Text></View><TouchableOpacity style={[s.holeStep,{width:31,height:31}]} onPress={next}><Text style={s.holeStepText}>›</Text></TouchableOpacity></View></View><View style={[s.panel,{marginBottom:0,padding:8}]}><Text style={s.panelTitle}>TO CENTRE</Text><Text style={{fontSize:25,fontWeight:'900',color:C.navy}}>{targetDistances.center??'—'} {units==='METRES'?'m':'yd'}</Text><Text style={s.small}>Front {targetDistances.front??'—'} · Back {targetDistances.back??'—'}</Text></View><View style={[s.panel,{marginBottom:0,padding:8,flex:1}]}><Text style={s.panelTitle}>VOICE CADDIE</Text><TouchableOpacity style={[s.mic,{padding:8,minWidth:0,marginBottom:5}]} onPress={ask}><Text style={{fontSize:22}}>🎙</Text><Text style={s.micTitle}>{listening?'LISTENING…':'ASK CADDIE'}</Text></TouchableOpacity><Text numberOfLines={5} style={[s.answer,{fontSize:10,lineHeight:14}]}>{caddieText}</Text></View><View style={[s.panel,{marginBottom:0,padding:8}]}><Text style={s.panelTitle}>RECOMMENDED CLUB</Text><Text style={s.bigClub}>{club}</Text><Text style={s.small}>{valid?`Playing ${playing} ${units==='METRES'?'m':'yd'}`:'Start live GPS'}</Text></View><View style={[s.panel,{marginBottom:0,padding:8}]}><Text style={s.panelTitle}>LAST SHOT</Text><Text style={s.small}>No shot recorded</Text></View></View></View><View style={{flexDirection:'row',marginTop:7}}>{[['SCORE',scores,setScores],['PUTTS',putts,setPutts]].map(([label,a,setter])=><View key={label} style={[s.panel,{flex:1,marginRight:5,padding:6,marginBottom:5}]}><Text style={[s.panelTitle,{textAlign:'center'}]}>{label}</Text><View style={{flexDirection:'row',alignItems:'center',justifyContent:'space-around'}}><TouchableOpacity onPress={()=>step(setter,a,-1)}><Text style={s.bigClub}>−</Text></TouchableOpacity><Text style={s.bigClub}>{a[i]||0}</Text><TouchableOpacity onPress={()=>step(setter,a,1)}><Text style={s.bigClub}>+</Text></TouchableOpacity></View></View>)}{[['GIR',gir,setGir],['FW',fw,setFw],['PEN',pen,setPen]].map(([label,a,setter])=><TouchableOpacity key={label} style={[s.panel,{flex:.7,padding:6,marginRight:5,marginBottom:5,alignItems:'center',justifyContent:'center'},Boolean(a[i])&&s.toggleOn]} onPress={()=>label==='PEN'?setA(setter,a,n(a[i])?'':'1'):setA(setter,a,!a[i])}><Text style={s.panelTitle}>{label}</Text><Text style={s.bigClub}>{Boolean(a[i])?'✓':'○'}</Text></TouchableOpacity>)}</View><View style={{flexDirection:'row',gap:6}}><View style={s.flex}><Btn text="NEXT HOLE" onPress={next}/></View><View style={s.flex}><Btn text="VIEW SCORECARD" onPress={()=>open('SCORE')} outline/></View></View><Btn text={gpsLive?'STOP LIVE GPS':'START LIVE GPS'} onPress={gpsLive?stopLiveGPS:startLiveGPS} outline/></>}"""
s,nr=re.subn(r"function Round\(.*?\nfunction Caddie",round_new+'\nfunction Caddie',s,count=1,flags=re.S)
if nr!=1: raise SystemExit('Build 74 round replacement failed')
s=s.replace("coursePars={coursePars}/>", "coursePars={coursePars} courseSI={courseSI}/>", 1)
s=s.replace(",coursePars}){const i=", ",coursePars,courseSI}){const i=", 1)

# Pin selector on the Caddie screen.
s=s.replace('function Caddie({distance,setDistance,wind,setWind,windDir,setWindDir,elev,setElev,lie,setLie,result,units,ask,listening,heard,caddieText,recordAdvice})', 'function Caddie({distance,setDistance,wind,setWind,windDir,setWindDir,elev,setElev,lie,setLie,result,units,ask,listening,heard,caddieText,recordAdvice,pinPos,setPinPos})', 1)
s=s.replace('<Seg items={LIES} value={lie} setValue={setLie}/><Field label={`WIND', '<Seg items={LIES} value={lie} setValue={setLie}/><Text style={s.label}>PIN POSITION</Text><Seg items={[\'FRONT\',\'CENTRE\',\'BACK\']} value={pinPos} setValue={setPinPos}/><Field label={`WIND', 1)

# Course importer: preserve the chosen tee and import real par/S.I. values.
s=s.replace("if(Array.isArray(hs)&&hs.length){const mapped=Array.from({length:18},(_,i)=>holeTarget(hs[i]||{}));if(mapped.some(x=>x.front||x.center||x.back))setTargets(mapped)}", "if(Array.isArray(hs)&&hs.length){const mapped=Array.from({length:18},(_,i)=>holeTarget(hs[i]||{}));if(mapped.some(x=>x.front||x.center||x.back))setTargets(mapped);setCoursePars(Array.from({length:18},(_,i)=>n(hs[i]?.par)||PARS[i]));setCourseSI(Array.from({length:18},(_,i)=>n(hs[i]?.stroke_index??hs[i]?.strokeIndex??hs[i]?.handicap??hs[i]?.si)||STROKE_INDEX[i]))}", 1)
s=s.replace('if(match)setTee(match)', '/* Keep the golfer\'s selected tee; never silently switch to the first directory tee. */', 1)
s=s.replace("savedCourses,setSavedCourses,courseInfo,setCourseInfo,courseMetres,setCourseMetres})", "savedCourses,setSavedCourses,courseInfo,setCourseInfo,courseMetres,setCourseMetres,coursePars,setCoursePars,courseSI,setCourseSI})", 1)
s=s.replace("setCourseMetres(Array.isArray(x.courseMetres)&&x.courseMetres.length===18?x.courseMetres:Array(18).fill(''));setHole('1')", "setCourseMetres(Array.isArray(x.courseMetres)&&x.courseMetres.length===18?x.courseMetres:Array(18).fill(''));setCoursePars(Array.isArray(x.coursePars)&&x.coursePars.length===18?x.coursePars:PARS);setCourseSI(Array.isArray(x.courseSI)&&x.courseSI.length===18?x.courseSI:STROKE_INDEX);setHole('1')", 1)
s=s.replace('const entry={name,tee,targets,courseMetres};', 'const entry={name,tee,targets,courseMetres,coursePars,courseSI};', 1)
s=s.replace("const cleanCourses=a=>{", "const cleanCourses=a=>{", 1)

# Hole scoring refinements.
hole_new="""function HoleScore({hole,scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,roundLog,setRoundLog,open,setHole,coursePars}){const i=Math.max(0,Math.min(17,n(hole)-1)),par=coursePars[i]||PARS[i],setA=(setter,a,v)=>setter(a.map((x,k)=>k===i?v:x)),step=(setter,a,d)=>setA(setter,a,String(Math.max(0,n(a[i])+d))),save=()=>{if(i<17){setHole(String(i+2));open('HOLESCORE')}else open('SCORE')};return <><Title kicker="SCORE THIS HOLE" title={`Hole ${hole}`} sub={`Par ${par}`}/><View style={s.holeScoreCard}><Text style={s.holeScoreLabel}>STROKES</Text><View style={s.scoreStepper}><TouchableOpacity style={s.scoreStep} onPress={()=>step(setScores,scores,-1)}><Text style={s.scoreStepText}>−</Text></TouchableOpacity><Text style={s.scoreValue}>{scores[i]||0}</Text><TouchableOpacity style={s.scoreStep} onPress={()=>step(setScores,scores,1)}><Text style={s.scoreStepText}>+</Text></TouchableOpacity></View><Text style={s.holeScoreLabel}>PUTTS</Text><View style={s.scoreStepper}><TouchableOpacity style={s.scoreStep} onPress={()=>step(setPutts,putts,-1)}><Text style={s.scoreStepText}>−</Text></TouchableOpacity><Text style={s.scoreValue}>{putts[i]||0}</Text><TouchableOpacity style={s.scoreStep} onPress={()=>step(setPutts,putts,1)}><Text style={s.scoreStepText}>+</Text></TouchableOpacity></View><View style={s.scoreFlags}><TouchableOpacity style={[s.scoreFlag,gir[i]&&s.toggleOn]} onPress={()=>setA(setGir,gir,!gir[i])}><Text style={s.cardTitle}>GIR</Text></TouchableOpacity><TouchableOpacity disabled={par===3} style={[s.scoreFlag,fw[i]&&s.toggleOn,par===3&&{opacity:.35}]} onPress={()=>setA(setFw,fw,!fw[i])}><Text style={s.cardTitle}>{par===3?'NO FW':'FAIRWAY'}</Text></TouchableOpacity><TouchableOpacity style={[s.scoreFlag,n(pen[i])>0&&s.penaltyOn]} onPress={()=>setA(setPen,pen,n(pen[i])>0?'':'1')}><Text style={s.cardTitle}>PENALTY</Text></TouchableOpacity></View><Field label="RESULT / NOTE" value={roundLog[i]?.result||''} onChangeText={v=>setRoundLog(roundLog.map((x,k)=>k===i?{...x,result:v}:x))}/></View><Btn text={i<17?'SAVE & NEXT HOLE':'SAVE ROUND'} onPress={save}/></>}"""
s,nh=re.subn(r"function HoleScore\(.*?\nfunction Score",hole_new+'\nfunction Score',s,count=1,flags=re.S)
if nh!=1: raise SystemExit('Build 74 hole score replacement failed')

# Scorecard uses imported par and stroke index, and METRES stays on one line.
s=s.replace('function Score({scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,total,toPar,played,open,tee,courseMetres,setCourseMetres,handicap})', 'function Score({scores,setScores,putts,setPutts,gir,setGir,fw,setFw,pen,setPen,total,toPar,played,open,tee,courseMetres,setCourseMetres,coursePars,courseSI,handicap})', 1)
s=s.replace('>METRES</Text>', '>M</Text>', 1)
s=s.replace('{PARS[i]}</Text>', '{coursePars[i]||PARS[i]}</Text>', 1)
s=s.replace('{STROKE_INDEX[i]}</Text>', '{courseSI[i]||STROKE_INDEX[i]}</Text>', 1)
s=s.replace('q+PARS[i]', 'q+(coursePars[i]||PARS[i])', 1)
s=s.replace('<Text key={i} style={s.scoreCellPar}>{STROKE_INDEX[i]}</Text>', '<Text key={i} style={s.scoreCellPar}>{courseSI[i]||STROKE_INDEX[i]}</Text>', 1)
s=s.replace('PAR {PARS.reduce((a,b)=>a+b,0)}', 'PAR {coursePars.reduce((a,b)=>a+n(b),0)}', 1)

# Settings and routine review fixes.
s=s.replace('<Field label="EMAIL" value={email} onChangeText={setEmail}/>', '', 1)
s=s.replace('sub={`${done.length}/9 complete`}', 'sub="Create your personal routine"', 1)
s=s.replace('<Text style={s.repeatNo}>9</Text>', '', 1)

app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 74',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.74"',t,count=1)
    g.write_text(t)
print('Build 74 final review corrections applied')
