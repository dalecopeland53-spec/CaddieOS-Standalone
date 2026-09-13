import React,{useMemo,useState}from'react';
import{SafeAreaView,ScrollView,StatusBar,StyleSheet,Text,TextInput,TouchableOpacity,View}from'react-native';

const PAGES=['HOME','CADDIE','BAG','COURSE','SCORE','PRACTICE','WARMUP','ROUTINES','SETTINGS','SUMMARY'];
const NAV=['HOME','CADDIE','BAG','COURSE','SCORE'];
const BAG0=[['Driver',230],['3W',210],['5W',195],['4i',180],['5i',170],['6i',160],['7i',150],['8i',140],['9i',130],['PW',115],['GW',100],['SW',85],['LW',70],['Putter',0]];
const LIES=['Tee','Fairway','Light Rough','Rough','Deep Rough','Fairway Bunker','Greenside Bunker'];
const TEES=['Black','Blue','White','Red','Yellow'];
const PARS=[4,5,4,3,4,4,4,5,4,4,3,4,5,4,5,3,3,4];
const WARM=['Loosen Up','Short Wedges','Mid Irons','Long Club','Driver','Chipping','Putting','Ready'];
const ROUTINES=['Target','Lie','Club','Picture','Commit','Breathe','Reset','Next'];
const PRACTICE=['Wedges','Irons','Driver','Chipping','Bunker','Putting'];

function playsLike(distance,wind,elev,lie){let d=Math.max(0,Number(distance)||0);const lp={Tee:0,Fairway:0,'Light Rough':.015,Rough:.04,'Deep Rough':.07,'Fairway Bunker':.045,'Greenside Bunker':0}[lie]||0;d*=1+lp;d+=(Number(wind)||0)*.75;d*=1+(Number(elev)||0)/100;return Math.max(0,Math.round(d));}
function nearestClub(y,bag){const clubs=bag.filter(x=>x[1]>0);return clubs.reduce((a,b)=>Math.abs(b[1]-y)<Math.abs(a[1]-y)?b:a,clubs[0]);}
function advice(y,club,lie,wind){if(lie==='Greenside Bunker'&&y<=45)return`${y<=25?'LW':'SW'}. Open the face, use the bounce and commit.`;let t=`Playing ${y} yards. ${club}.`;if(lie!=='Tee'&&lie!=='Fairway')t+=` Allow for ${lie.toLowerCase()}.`;if(Number(wind)>0)t+=' Into the wind.';if(Number(wind)<0)t+=' Wind helping.';return t+' Pick the target and commit.';}

export default function App(){
 const[tab,setTab]=useState('HOME');
 const[distance,setDistance]=useState('150');
 const[wind,setWind]=useState('0');
 const[elev,setElev]=useState('0');
 const[lie,setLie]=useState('Fairway');
 const[bag,setBag]=useState(BAG0);
 const[course,setCourse]=useState('');
 const[tee,setTee]=useState('White');
 const[hole,setHole]=useState('1');
 const[scores,setScores]=useState(Array(18).fill(''));
 const[putts,setPutts]=useState(Array(18).fill(''));
 const[practice,setPractice]=useState('Wedges');
 const[shape,setShape]=useState('Straight');
 const[resultShot,setResultShot]=useState('Good');
 const[warmDone,setWarmDone]=useState([]);
 const[routineDone,setRoutineDone]=useState([]);
 const[units,setUnits]=useState('YARDS');
 const[player,setPlayer]=useState('Player');
 const[caddieName,setCaddieName]=useState('Pete');
 const result=useMemo(()=>{const y=playsLike(distance,wind,elev,lie),c=nearestClub(y,bag);return{y,club:c[0],carry:c[1]}},[distance,wind,elev,lie,bag]);
 const total=scores.reduce((a,b)=>a+(Number(b)||0),0);
 const totalPutts=putts.reduce((a,b)=>a+(Number(b)||0),0);
 const parTotal=PARS.reduce((a,b)=>a+b,0);
 const played=scores.filter(Boolean).length;
 const toPar=played?scores.reduce((a,v,i)=>a+(v?Number(v)-PARS[i]:0),0):0;
 const common={go:setTab,course,hole,total,played,toPar};
 return <SafeAreaView style={s.safe}>
  <StatusBar barStyle="dark-content" backgroundColor="#EEE9DE"/>
  <Header go={setTab}/>
  <ScrollView contentContainerStyle={s.body} keyboardShouldPersistTaps="handled">
   {tab==='HOME'&&<Home {...common}/>} 
   {tab==='CADDIE'&&<Caddie result={result} distance={distance} setDistance={setDistance} wind={wind} setWind={setWind} elev={elev} setElev={setElev} lie={lie} setLie={setLie} hole={hole} caddieName={caddieName}/>} 
   {tab==='BAG'&&<Bag bag={bag} setBag={setBag} units={units}/>} 
   {tab==='COURSE'&&<Course course={course} setCourse={setCourse} tee={tee} setTee={setTee} hole={hole} setHole={setHole}/>} 
   {tab==='SCORE'&&<Score scores={scores} setScores={setScores} putts={putts} setPutts={setPutts} total={total} parTotal={parTotal} toPar={toPar} played={played}/>} 
   {tab==='PRACTICE'&&<Practice practice={practice} setPractice={setPractice} shape={shape} setShape={setShape} resultShot={resultShot} setResultShot={setResultShot}/>} 
   {tab==='WARMUP'&&<Warmup done={warmDone} setDone={setWarmDone}/>} 
   {tab==='ROUTINES'&&<Routines done={routineDone} setDone={setRoutineDone}/>} 
   {tab==='SETTINGS'&&<Settings units={units} setUnits={setUnits} player={player} setPlayer={setPlayer} caddieName={caddieName} setCaddieName={setCaddieName}/>} 
   {tab==='SUMMARY'&&<Summary course={course} tee={tee} scores={scores} total={total} totalPutts={totalPutts} played={played} toPar={toPar}/>} 
  </ScrollView>
  <BottomNav tab={tab} setTab={setTab}/>
 </SafeAreaView>;
}

function Header({go}){return <View style={s.header}><TouchableOpacity onPress={()=>go('HOME')} style={s.iconButton}><Text style={s.iconBall}>●</Text><Text style={s.iconC}>C</Text></TouchableOpacity><View style={s.brandBox}><Text style={s.brand}>Caddie<Text style={s.blue}>OS</Text></Text><Text style={s.tag}>YOUR CADDIE • YOUR GAME</Text></View></View>}
function BottomNav({tab,setTab}){return <View style={s.bottomNav}>{NAV.map(x=><TouchableOpacity key={x} onPress={()=>setTab(x)} style={s.bottomItem}><View style={[s.navGlyph,tab===x&&s.navGlyphOn]}><Text style={[s.navGlyphText,tab===x&&s.navGlyphTextOn]}>{x==='HOME'?'⌂':x==='CADDIE'?'●':x==='BAG'?'◇':x==='COURSE'?'⌖':'≡'}</Text></View><Text style={[s.bottomTxt,tab===x&&s.bottomTxtOn]}>{x==='SCORE'?'SCORE':x}</Text></TouchableOpacity>)}</View>}
function PageHead({kicker,title,badge}){return <View style={s.pageHead}><View><Text style={s.kicker}>{kicker}</Text><Text style={s.pageTitle}>{title}</Text></View>{badge?<View style={s.holeBadge}><Text style={s.holeBadgeText}>{badge}</Text></View>:null}</View>}
function IconTile({icon,title,sub,onPress}){return <TouchableOpacity onPress={onPress} style={s.quickTile}><View style={s.tileIconBox}><Text style={s.quickIcon}>{icon}</Text></View><Text style={s.quickTitle}>{title}</Text><Text style={s.quickSub}>{sub}</Text></TouchableOpacity>}
function SelectChip({label,on,press}){return <TouchableOpacity onPress={press} style={[s.chip,on&&s.chipOn]}><Text style={[s.chipTxt,on&&s.chipTxtOn]}>{label}</Text></TouchableOpacity>}

function Home({go,course,hole,total,played,toPar}){return <>
 <View style={s.topCard}><View style={{flex:1}}><Text style={s.kicker}>CADDIEOS</Text><Text style={s.pageTitle}>{course||'Ready to play'}</Text><Text style={s.subline}>{course?`Hole ${hole} • Round ready`:'Set your course, bag and start your round.'}</Text></View><View style={s.readyPill}><Text style={s.readyDot}>●</Text><Text style={s.readyText}>READY</Text></View></View>
 <TouchableOpacity onPress={()=>go('CADDIE')} style={s.startRound}><View><Text style={s.startSmall}>YOUR ROUND</Text><Text style={s.startTitle}>START ROUND</Text></View><Text style={s.chev}>›</Text></TouchableOpacity>
 <View style={s.quickGrid}>
  <IconTile icon="●" title="CADDIE" sub="Shot advice" onPress={()=>go('CADDIE')}/><IconTile icon="◇" title="MY BAG" sub="14 clubs" onPress={()=>go('BAG')}/>
  <IconTile icon="⌖" title="COURSE" sub="Round setup" onPress={()=>go('COURSE')}/><IconTile icon="≡" title="SCORECARD" sub={played?`${played} holes • ${total}`:'18 holes'} onPress={()=>go('SCORE')}/>
  <IconTile icon="◎" title="PRACTICE" sub="Build your game" onPress={()=>go('PRACTICE')}/><IconTile icon="↗" title="WARM-UP" sub="8-step prep" onPress={()=>go('WARMUP')}/>
  <IconTile icon="✓" title="ROUTINES" sub="8-step routine" onPress={()=>go('ROUTINES')}/><IconTile icon="⚙" title="SETTINGS" sub="Player & units" onPress={()=>go('SETTINGS')}/>
  <IconTile icon="▣" title="ROUND SUMMARY" sub={played?`${toPar>0?'+':''}${toPar} after ${played}`:'Round report'} onPress={()=>go('SUMMARY')}/>
 </View>
 <View style={s.infoStrip}><View><Text style={s.infoLabel}>CURRENT HOLE</Text><Text style={s.infoValue}>{hole}</Text></View><View style={s.vline}/><View style={{flex:1}}><Text style={s.infoLabel}>COURSE</Text><Text style={s.infoText}>{course||'Not selected'}</Text></View></View>
 </>}

function Caddie({result,distance,setDistance,wind,setWind,elev,setElev,lie,setLie,hole,caddieName}){return <>
 <PageHead kicker="CADDIE" title={`Hole ${hole}`} badge="LIVE"/>
 <View style={s.caddiePanel}><View style={s.caddieLeft}><Text style={s.metricLabel}>PLAYS LIKE</Text><Text style={s.bigDistance}>{result.y}<Text style={s.bigUnit}> yd</Text></Text><Text style={s.clubCall}>{result.club}</Text><Text style={s.carry}>Stock carry {result.carry} yd</Text></View><View style={s.clubBadge}><Text style={s.clubBadgeSmall}>CLUB</Text><Text style={s.clubBadgeBig}>{result.club}</Text></View></View>
 <View style={s.adviceBox}><Text style={s.adviceLabel}>{caddieName.toUpperCase()} SAYS</Text><Text style={s.adviceText}>{advice(result.y,result.club,lie,wind)}</Text></View>
 <TouchableOpacity style={s.micButton}><View style={s.micDisc}><Text style={s.micDot}>●</Text></View><View><Text style={s.micMain}>ASK {caddieName.toUpperCase()}</Text><Text style={s.micSub}>Tap to speak</Text></View></TouchableOpacity>
 <View style={s.compactCard}><View style={s.fieldRow}><MiniField label="TARGET" value={distance} setValue={setDistance} suffix="yd"/><MiniField label="WIND" value={wind} setValue={setWind} suffix="mph"/><MiniField label="SLOPE" value={elev} setValue={setElev} suffix="%"/></View><Text style={s.label}>LIE</Text><View style={s.chips}>{LIES.map(x=><SelectChip key={x} label={x} on={lie===x} press={()=>setLie(x)}/>)}</View></View>
 </>}

function Bag({bag,setBag,units}){const change=(i,delta)=>setBag(p=>p.map((x,n)=>n===i?[x[0],x[0]==='Putter'?0:Math.max(0,x[1]+delta)]:x));return <>
 <PageHead kicker="MY BAG" title="14 Clubs" badge={units}/>
 <View style={s.bagGrid}>{bag.map(([name,d],i)=><View key={name} style={s.bagClub}><View style={s.bagTop}><Text style={s.bagName}>{name}</Text><Text style={s.bagDist}>{d}<Text style={s.bagUnit}> yd</Text></Text></View><View style={s.bagControls}><TouchableOpacity onPress={()=>change(i,-1)} disabled={name==='Putter'} style={s.stepBtn}><Text style={s.stepTxt}>−</Text></TouchableOpacity><Text style={s.stockTxt}>{name==='Putter'?'PUTTING':'CARRY'}</Text><TouchableOpacity onPress={()=>change(i,1)} disabled={name==='Putter'} style={s.stepBtn}><Text style={s.stepTxt}>+</Text></TouchableOpacity></View></View>)}</View>
 <View style={s.notice}><Text style={s.noticeTitle}>PERSONAL CARRY</Text><Text style={s.noticeText}>Set normal carry distance, not your longest shot. CaddieOS uses these numbers for club selection.</Text></View>
 </>}

function Course({course,setCourse,tee,setTee,hole,setHole}){return <>
 <PageHead kicker="COURSE" title={course||'Round Setup'} badge="GPS"/>
 <View style={s.compactCard}><Text style={s.label}>COURSE NAME</Text><TextInput style={s.input} value={course} onChangeText={setCourse} placeholder="Enter course" placeholderTextColor="#7E858B"/>
 <Text style={s.label}>TEE COLOUR</Text><View style={s.teeRow}>{TEES.map(x=><TouchableOpacity key={x} onPress={()=>setTee(x)} style={[s.teeBtn,tee===x&&s.teeBtnOn]}><View style={[s.teeDot,{backgroundColor:x==='Black'?'#202020':x==='Blue'?'#1765A7':x==='White'?'#FFFFFF':x==='Red'?'#B73632':'#D4A91C'}]}/><Text style={[s.teeText,tee===x&&s.teeTextOn]}>{x}</Text></TouchableOpacity>)}</View>
 <Text style={s.label}>CURRENT HOLE</Text><View style={s.holeChooser}><TouchableOpacity onPress={()=>setHole(String(Math.max(1,Number(hole||1)-1)))} style={s.holeStep}><Text style={s.holeStepText}>−</Text></TouchableOpacity><View style={s.holeNumber}><Text style={s.holeNumberText}>{Math.min(18,Math.max(1,Number(hole)||1))}</Text></View><TouchableOpacity onPress={()=>setHole(String(Math.min(18,Number(hole||1)+1)))} style={s.holeStep}><Text style={s.holeStepText}>+</Text></TouchableOpacity></View></View>
 <View style={s.courseStatus}><View style={{flex:1}}><Text style={s.infoLabel}>COURSE</Text><Text style={s.statusMain}>{course||'No course selected'}</Text></View><View style={s.statusRight}><Text style={s.infoLabel}>TEE</Text><Text style={s.statusMain}>{tee}</Text></View></View>
 </>}

function Score({scores,setScores,putts,setPutts,total,parTotal,toPar,played}){const setScore=(arr,setter,i,t)=>setter(arr.map((x,n)=>n===i?t.replace(/[^0-9]/g,''):x));return <>
 <PageHead kicker="GAME REPORT" title="Scorecard" badge={played?`${toPar>0?'+':''}${toPar}`:'—'}/>
 <View style={s.scoreRibbon}>{scores.map((v,i)=><View key={i} style={s.ribbonCell}><Text style={s.ribbonHole}>{i+1}</Text><Text style={s.ribbonScore}>{v||'•'}</Text></View>)}</View>
 <View style={s.scoreCard}><View style={s.scoreHeaderRow}><Text style={s.sectionTitle}>18-HOLE SCORECARD</Text><Text style={s.scoreMeta}>{played}/18 PLAYED</Text></View><View style={s.scoreGrid}>{scores.map((v,i)=><View key={i} style={s.scoreCell}><Text style={s.holeNo}>{i+1}</Text><Text style={s.parMini}>PAR {PARS[i]}</Text><TextInput style={s.scoreInput} keyboardType="numeric" maxLength={2} value={v} onChangeText={t=>setScore(scores,setScores,i,t)} placeholder="—" placeholderTextColor="#9A9A93"/><TextInput style={s.puttInput} keyboardType="numeric" maxLength={1} value={putts[i]} onChangeText={t=>setScore(putts,setPutts,i,t)} placeholder="P" placeholderTextColor="#7E858B"/></View>)}</View>
 <View style={s.totals}><View><Text style={s.totalSmall}>PAR</Text><Text style={s.totalValue}>{parTotal}</Text></View><View><Text style={s.totalSmall}>SCORE</Text><Text style={s.totalValue}>{total||'—'}</Text></View><View><Text style={s.totalSmall}>TO PAR</Text><Text style={s.totalAccent}>{played?`${toPar>0?'+':''}${toPar}`:'—'}</Text></View></View></View>
 </>}

function Practice({practice,setPractice,shape,setShape,resultShot,setResultShot}){return <>
 <PageHead kicker="PRACTICE" title="Practice Mode" badge="TRAIN"/>
 <View style={s.heroLine}><Text style={s.heroLineBig}>{practice}</Text><Text style={s.heroLineSub}>Practice with purpose. One shot, one target, one result.</Text></View>
 <View style={s.compactCard}><Text style={s.label}>AREA</Text><View style={s.chips}>{PRACTICE.map(x=><SelectChip key={x} label={x} on={practice===x} press={()=>setPractice(x)}/>)}</View><Text style={s.label}>SHOT SHAPE</Text><View style={s.threeRow}>{['Straight','Draw','Fade'].map(x=><SelectChip key={x} label={x} on={shape===x} press={()=>setShape(x)}/>)}</View><Text style={s.label}>RESULT</Text><View style={s.chips}>{['Good','Left','Right','Short','Long'].map(x=><SelectChip key={x} label={x} on={resultShot===x} press={()=>setResultShot(x)}/>)}</View></View>
 <View style={s.adviceBox}><Text style={s.adviceLabel}>SESSION NOTE</Text><Text style={s.adviceText}>{practice} • {shape} • {resultShot}. Keep the same target and repeat the routine.</Text></View>
 </>}

function Warmup({done,setDone}){const toggle=i=>setDone(done.includes(i)?done.filter(x=>x!==i):[...done,i]);return <>
 <PageHead kicker="WARM-UP" title="Ready to Play" badge={`${done.length}/8`}/>
 <View style={s.notice}><Text style={s.noticeTitle}>ADVICE ONLY</Text><Text style={s.noticeText}>Use the full warm-up when time allows. If not, work through the steps mentally before the first tee.</Text></View>
 <View style={s.stepList}>{WARM.map((x,i)=><TouchableOpacity key={x} onPress={()=>toggle(i)} style={[s.stepCard,done.includes(i)&&s.stepCardOn]}><View style={[s.stepIndex,done.includes(i)&&s.stepIndexOn]}><Text style={[s.stepIndexText,done.includes(i)&&s.stepIndexTextOn]}>{done.includes(i)?'✓':i+1}</Text></View><View style={{flex:1}}><Text style={s.stepTitle}>{x}</Text><Text style={s.stepSub}>{i===0?'Easy movement and tempo':i===1?'Find strike and distance':i===2?'Build rhythm':i===3?'Controlled full swings':i===4?'Finish with targets':i===5?'Land spots and rollout':i===6?'Speed then line':'Commit to your game'}</Text></View></TouchableOpacity>)}</View>
 </>}

function Routines({done,setDone}){const toggle=i=>setDone(done.includes(i)?done.filter(x=>x!==i):[...done,i]);return <>
 <PageHead kicker="ROUTINES" title="Pre-Shot Routine" badge={`${done.length}/8`}/>
 <View style={s.stepList}>{ROUTINES.map((x,i)=><TouchableOpacity key={x} onPress={()=>toggle(i)} style={[s.stepCard,done.includes(i)&&s.stepCardOn]}><View style={[s.stepIndex,done.includes(i)&&s.stepIndexOn]}><Text style={[s.stepIndexText,done.includes(i)&&s.stepIndexTextOn]}>{done.includes(i)?'✓':i+1}</Text></View><View style={{flex:1}}><Text style={s.stepTitle}>{x}</Text><Text style={s.stepSub}>{['Pick one precise target','Read the ground and conditions','Choose it and stop second guessing','See the shot before you hit it','Make the decision final','Slow breath, soft hands','Accept the result immediately','Move fully to the next shot'][i]}</Text></View></TouchableOpacity>)}</View>
 </>}

function Settings({units,setUnits,player,setPlayer,caddieName,setCaddieName}){return <>
 <PageHead kicker="SETTINGS" title="CaddieOS Setup" badge="SYSTEM"/>
 <View style={s.compactCard}><Text style={s.label}>PLAYER NAME</Text><TextInput style={s.input} value={player} onChangeText={setPlayer}/><Text style={s.label}>CADDIE NAME</Text><TextInput style={s.input} value={caddieName} onChangeText={setCaddieName}/><Text style={s.label}>UNITS</Text><View style={s.twoRow}>{['YARDS','METRES'].map(x=><TouchableOpacity key={x} onPress={()=>setUnits(x)} style={[s.wideChoice,units===x&&s.wideChoiceOn]}><Text style={[s.wideChoiceText,units===x&&s.wideChoiceTextOn]}>{x}</Text></TouchableOpacity>)}</View></View>
 <View style={s.settingsBlock}><SettingRow title="Outdoor display" value="ANTI-GLARE"/><SettingRow title="Caddie response" value="READY"/><SettingRow title="Screen layout" value="COMPACT"/><SettingRow title="Pages" value={`${PAGES.length}`}/></View>
 </>}
function SettingRow({title,value}){return <View style={s.settingRow}><Text style={s.settingTitle}>{title}</Text><Text style={s.settingValue}>{value}</Text></View>}

function Summary({course,tee,scores,total,totalPutts,played,toPar}){return <>
 <PageHead kicker="ROUND SUMMARY" title={course||'Your Round'} badge={played?`${played}/18`:'READY'}/>
 <View style={s.summaryHero}><View><Text style={s.summaryLabel}>TOTAL SCORE</Text><Text style={s.summaryBig}>{total||'—'}</Text></View><View style={s.summaryDivider}/><View><Text style={s.summaryLabel}>TO PAR</Text><Text style={s.summaryBig}>{played?`${toPar>0?'+':''}${toPar}`:'—'}</Text></View><View style={s.summaryDivider}/><View><Text style={s.summaryLabel}>PUTTS</Text><Text style={s.summaryBig}>{totalPutts||'—'}</Text></View></View>
 <View style={s.courseStatus}><View style={{flex:1}}><Text style={s.infoLabel}>COURSE</Text><Text style={s.statusMain}>{course||'Not selected'}</Text></View><View style={s.statusRight}><Text style={s.infoLabel}>TEE</Text><Text style={s.statusMain}>{tee}</Text></View></View>
 <View style={s.summaryList}>{scores.map((v,i)=>v?<View key={i} style={s.summaryRow}><View style={s.summaryHole}><Text style={s.summaryHoleNo}>{i+1}</Text></View><Text style={s.summaryPar}>PAR {PARS[i]}</Text><Text style={s.summaryScore}>{v}</Text><Text style={s.summaryDelta}>{Number(v)-PARS[i]===0?'E':Number(v)-PARS[i]>0?`+${Number(v)-PARS[i]}`:Number(v)-PARS[i]}</Text></View>:null)}</View>
 {!played&&<View style={s.notice}><Text style={s.noticeTitle}>NO SCORES YET</Text><Text style={s.noticeText}>Enter scores during the round and your full round report will build here automatically.</Text></View>}
 </>}

function MiniField({label,value,setValue,suffix}){return <View style={s.miniField}><Text style={s.miniLabel}>{label}</Text><View style={s.miniInputWrap}><TextInput style={s.miniInput} value={value} onChangeText={setValue} keyboardType="numbers-and-punctuation"/><Text style={s.miniSuffix}>{suffix}</Text></View></View>}

const C={bg:'#EEE9DE',panel:'#F7F4EC',panel2:'#E5E0D5',line:'#B9B7AF',navy:'#143E68',blue:'#0879BE',muted:'#66727E',gold:'#C99A34',dark:'#06192B',white:'#FFFFFF',green:'#2D7059'};
const s=StyleSheet.create({
 safe:{flex:1,backgroundColor:C.bg},header:{height:78,flexDirection:'row',alignItems:'center',justifyContent:'center',paddingTop:4,paddingHorizontal:14,borderBottomWidth:1,borderBottomColor:'#D0CBC0'},
 iconButton:{width:52,height:52,borderRadius:16,backgroundColor:C.dark,borderWidth:2,borderColor:C.blue,alignItems:'center',justifyContent:'center',shadowColor:'#000',shadowOpacity:.16,shadowRadius:5,elevation:4},iconBall:{position:'absolute',top:5,right:8,color:C.gold,fontSize:10},iconC:{color:C.gold,fontSize:30,fontWeight:'900'},brandBox:{marginLeft:10},brand:{fontSize:29,fontWeight:'900',color:C.navy,letterSpacing:.2},blue:{color:C.blue},tag:{fontSize:9,fontWeight:'900',letterSpacing:1.8,color:C.muted,marginTop:1},
 body:{paddingHorizontal:12,paddingTop:8,paddingBottom:92},bottomNav:{height:74,position:'absolute',bottom:0,left:0,right:0,backgroundColor:C.dark,flexDirection:'row',alignItems:'center',justifyContent:'space-around',borderTopWidth:1,borderTopColor:'#214763'},bottomItem:{width:'20%',alignItems:'center',justifyContent:'center'},navGlyph:{width:30,height:30,borderRadius:10,alignItems:'center',justifyContent:'center',backgroundColor:'#102A40'},navGlyphOn:{backgroundColor:C.gold},navGlyphText:{color:'#D7E0E8',fontWeight:'900',fontSize:16},navGlyphTextOn:{color:C.dark},bottomTxt:{fontSize:9,fontWeight:'800',color:'#AEBCC8',marginTop:3},bottomTxtOn:{color:C.white},
 topCard:{backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:18,padding:15,flexDirection:'row',alignItems:'center'},kicker:{fontSize:10,fontWeight:'900',letterSpacing:1.8,color:C.blue},pageTitle:{fontSize:24,fontWeight:'900',color:C.navy,marginTop:2},subline:{fontSize:12,color:C.muted,marginTop:4,maxWidth:250},readyPill:{flexDirection:'row',alignItems:'center',backgroundColor:'#DDEAE4',borderRadius:20,paddingHorizontal:10,paddingVertical:7,marginLeft:8},readyDot:{color:C.green,fontSize:10,marginRight:5},readyText:{fontSize:10,fontWeight:'900',color:C.green},
 startRound:{marginTop:10,backgroundColor:C.navy,borderRadius:18,paddingHorizontal:17,paddingVertical:15,flexDirection:'row',alignItems:'center',justifyContent:'space-between'},startSmall:{fontSize:9,fontWeight:'900',color:'#ADC7DD',letterSpacing:1.5},startTitle:{fontSize:20,fontWeight:'900',color:C.white,marginTop:2},chev:{fontSize:36,color:C.gold,fontWeight:'300'},quickGrid:{flexDirection:'row',flexWrap:'wrap',justifyContent:'space-between',marginTop:10},quickTile:{width:'48.5%',backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:16,padding:12,marginBottom:9,minHeight:112},tileIconBox:{width:35,height:35,borderRadius:11,backgroundColor:C.dark,alignItems:'center',justifyContent:'center',marginBottom:8},quickIcon:{fontSize:18,color:C.gold,fontWeight:'900'},quickTitle:{fontSize:13,fontWeight:'900',color:C.navy},quickSub:{fontSize:11,color:C.muted,marginTop:3},infoStrip:{backgroundColor:C.panel2,borderRadius:15,padding:13,flexDirection:'row',alignItems:'center',borderWidth:1,borderColor:C.line},infoLabel:{fontSize:8,fontWeight:'900',letterSpacing:1.2,color:C.muted},infoValue:{fontSize:23,fontWeight:'900',color:C.navy},infoText:{fontSize:13,fontWeight:'800',color:C.navy,marginTop:3},vline:{width:1,height:34,backgroundColor:C.line,marginHorizontal:16},
 pageHead:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',paddingVertical:6,marginBottom:8},holeBadge:{backgroundColor:C.navy,borderRadius:12,paddingHorizontal:10,paddingVertical:7},holeBadgeText:{fontSize:10,fontWeight:'900',color:C.gold,letterSpacing:1},caddiePanel:{backgroundColor:C.dark,borderRadius:20,padding:17,flexDirection:'row',justifyContent:'space-between',alignItems:'center'},caddieLeft:{flex:1},metricLabel:{fontSize:9,color:'#9FB3C3',fontWeight:'900',letterSpacing:1.4},bigDistance:{fontSize:38,fontWeight:'900',color:C.white,marginTop:1},bigUnit:{fontSize:15,color:'#B8C8D4'},clubCall:{fontSize:20,fontWeight:'900',color:C.gold},carry:{fontSize:10,color:'#AFC0CD',marginTop:2},clubBadge:{width:82,height:82,borderRadius:18,borderWidth:1,borderColor:'#34556F',backgroundColor:'#102A40',alignItems:'center',justifyContent:'center'},clubBadgeSmall:{fontSize:8,fontWeight:'900',color:'#9DB0BF'},clubBadgeBig:{fontSize:24,fontWeight:'900',color:C.gold},
 adviceBox:{backgroundColor:C.panel,borderLeftWidth:4,borderLeftColor:C.gold,borderRadius:14,padding:13,marginTop:9,borderWidth:1,borderColor:C.line},adviceLabel:{fontSize:9,fontWeight:'900',letterSpacing:1.4,color:C.blue},adviceText:{fontSize:14,lineHeight:20,color:C.dark,fontWeight:'650',marginTop:4},micButton:{backgroundColor:C.blue,borderRadius:16,padding:12,marginTop:9,flexDirection:'row',alignItems:'center'},micDisc:{width:40,height:40,borderRadius:20,backgroundColor:C.white,alignItems:'center',justifyContent:'center',marginRight:11},micDot:{fontSize:17,color:C.blue},micMain:{fontSize:15,fontWeight:'900',color:C.white},micSub:{fontSize:10,color:'#D8EEF9',marginTop:1},
 compactCard:{backgroundColor:C.panel,borderRadius:17,borderWidth:1,borderColor:C.line,padding:13,marginTop:9},fieldRow:{flexDirection:'row',justifyContent:'space-between'},miniField:{width:'31.5%'},miniLabel:{fontSize:8,fontWeight:'900',color:C.muted,letterSpacing:1},miniInputWrap:{marginTop:4,borderWidth:1,borderColor:C.line,borderRadius:10,backgroundColor:C.white,height:44,flexDirection:'row',alignItems:'center',paddingHorizontal:7},miniInput:{flex:1,fontSize:17,fontWeight:'900',color:C.navy,padding:0},miniSuffix:{fontSize:9,fontWeight:'800',color:C.muted},label:{fontSize:9,fontWeight:'900',letterSpacing:1.2,color:C.muted,marginTop:13,marginBottom:6},chips:{flexDirection:'row',flexWrap:'wrap'},chip:{borderWidth:1,borderColor:C.line,backgroundColor:'#F2EFE7',borderRadius:13,paddingHorizontal:10,paddingVertical:8,marginRight:6,marginBottom:6},chipOn:{backgroundColor:C.navy,borderColor:C.navy},chipTxt:{fontSize:10,fontWeight:'800',color:C.navy},chipTxtOn:{color:C.white},
 bagGrid:{flexDirection:'row',flexWrap:'wrap',justifyContent:'space-between'},bagClub:{width:'48.5%',backgroundColor:C.panel,borderRadius:14,borderWidth:1,borderColor:C.line,padding:11,marginBottom:8},bagTop:{flexDirection:'row',justifyContent:'space-between',alignItems:'baseline'},bagName:{fontSize:14,fontWeight:'900',color:C.navy},bagDist:{fontSize:17,fontWeight:'900',color:C.dark},bagUnit:{fontSize:8,color:C.muted},bagControls:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',marginTop:8},stepBtn:{width:31,height:31,borderRadius:10,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'},stepTxt:{fontSize:19,fontWeight:'900',color:C.gold},stockTxt:{fontSize:8,fontWeight:'900',letterSpacing:1,color:C.muted},notice:{backgroundColor:'#E8E1D3',borderRadius:14,padding:12,borderWidth:1,borderColor:'#CFC4B2',marginTop:4},noticeTitle:{fontSize:9,fontWeight:'900',letterSpacing:1.2,color:C.navy},noticeText:{fontSize:11,lineHeight:16,color:C.muted,marginTop:3},
 input:{height:46,borderRadius:11,borderWidth:1,borderColor:C.line,backgroundColor:C.white,paddingHorizontal:11,fontSize:15,fontWeight:'800',color:C.navy},teeRow:{flexDirection:'row',flexWrap:'wrap'},teeBtn:{flexDirection:'row',alignItems:'center',borderWidth:1,borderColor:C.line,borderRadius:12,paddingHorizontal:9,paddingVertical:8,marginRight:5,marginBottom:6},teeBtnOn:{backgroundColor:C.navy,borderColor:C.navy},teeDot:{width:11,height:11,borderRadius:6,borderWidth:1,borderColor:'#777',marginRight:5},teeText:{fontSize:9,fontWeight:'800',color:C.navy},teeTextOn:{color:C.white},holeChooser:{flexDirection:'row',alignItems:'center',justifyContent:'center'},holeStep:{width:46,height:42,borderRadius:12,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'},holeStepText:{fontSize:24,color:C.gold,fontWeight:'900'},holeNumber:{width:76,height:48,alignItems:'center',justifyContent:'center',marginHorizontal:10,borderRadius:12,backgroundColor:C.white,borderWidth:1,borderColor:C.line},holeNumberText:{fontSize:24,fontWeight:'900',color:C.navy},courseStatus:{backgroundColor:C.panel2,borderRadius:15,borderWidth:1,borderColor:C.line,padding:13,flexDirection:'row',marginTop:9},statusRight:{minWidth:70,alignItems:'flex-end'},statusMain:{fontSize:13,fontWeight:'900',color:C.navy,marginTop:3},
 scoreRibbon:{flexDirection:'row',flexWrap:'wrap',backgroundColor:C.dark,borderRadius:15,padding:7,marginBottom:8},ribbonCell:{width:'11.11%',alignItems:'center',paddingVertical:4},ribbonHole:{fontSize:7,color:'#8EA5B6'},ribbonScore:{fontSize:11,fontWeight:'900',color:C.white},scoreCard:{backgroundColor:C.panel,borderRadius:16,borderWidth:1,borderColor:C.line,padding:10},scoreHeaderRow:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:7},sectionTitle:{fontSize:10,fontWeight:'900',color:C.navy,letterSpacing:1},scoreMeta:{fontSize:8,fontWeight:'900',color:C.muted},scoreGrid:{flexDirection:'row',flexWrap:'wrap',justifyContent:'space-between'},scoreCell:{width:'15.8%',backgroundColor:'#F0ECE3',borderRadius:10,padding:5,alignItems:'center',marginBottom:6,borderWidth:1,borderColor:'#D5D0C5'},holeNo:{fontSize:9,fontWeight:'900',color:C.navy},parMini:{fontSize:6,fontWeight:'800',color:C.muted,marginTop:1},scoreInput:{width:'100%',height:30,textAlign:'center',fontSize:16,fontWeight:'900',color:C.dark,padding:0},puttInput:{width:'100%',height:24,textAlign:'center',fontSize:10,fontWeight:'900',color:C.blue,padding:0,borderTopWidth:1,borderTopColor:'#D6D0C4'},totals:{flexDirection:'row',justifyContent:'space-around',borderTopWidth:1,borderTopColor:C.line,paddingTop:10,marginTop:3},totalSmall:{fontSize:8,fontWeight:'900',color:C.muted,textAlign:'center'},totalValue:{fontSize:21,fontWeight:'900',color:C.navy,textAlign:'center'},totalAccent:{fontSize:21,fontWeight:'900',color:C.blue,textAlign:'center'},
 heroLine:{backgroundColor:C.dark,borderRadius:17,padding:16},heroLineBig:{fontSize:25,fontWeight:'900',color:C.gold},heroLineSub:{fontSize:11,lineHeight:16,color:'#B9C7D1',marginTop:4},threeRow:{flexDirection:'row'},twoRow:{flexDirection:'row',justifyContent:'space-between'},wideChoice:{width:'48.5%',borderWidth:1,borderColor:C.line,borderRadius:12,paddingVertical:12,alignItems:'center',backgroundColor:'#F0ECE3'},wideChoiceOn:{backgroundColor:C.navy,borderColor:C.navy},wideChoiceText:{fontSize:11,fontWeight:'900',color:C.navy},wideChoiceTextOn:{color:C.white},
 stepList:{marginTop:2},stepCard:{backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:14,padding:10,marginBottom:7,flexDirection:'row',alignItems:'center'},stepCardOn:{borderColor:C.green,backgroundColor:'#E8F0EC'},stepIndex:{width:36,height:36,borderRadius:11,backgroundColor:C.dark,alignItems:'center',justifyContent:'center',marginRight:10},stepIndexOn:{backgroundColor:C.green},stepIndexText:{fontSize:14,fontWeight:'900',color:C.gold},stepIndexTextOn:{color:C.white},stepTitle:{fontSize:13,fontWeight:'900',color:C.navy},stepSub:{fontSize:10,color:C.muted,marginTop:2},
 settingsBlock:{backgroundColor:C.panel,borderRadius:15,borderWidth:1,borderColor:C.line,marginTop:9,overflow:'hidden'},settingRow:{minHeight:49,paddingHorizontal:12,flexDirection:'row',alignItems:'center',justifyContent:'space-between',borderBottomWidth:1,borderBottomColor:'#D8D3C9'},settingTitle:{fontSize:12,fontWeight:'800',color:C.navy},settingValue:{fontSize:10,fontWeight:'900',color:C.blue},summaryHero:{backgroundColor:C.dark,borderRadius:17,padding:14,flexDirection:'row',justifyContent:'space-around',alignItems:'center'},summaryLabel:{fontSize:7,fontWeight:'900',letterSpacing:1,color:'#94AABB',textAlign:'center'},summaryBig:{fontSize:24,fontWeight:'900',color:C.gold,textAlign:'center',marginTop:2},summaryDivider:{width:1,height:36,backgroundColor:'#36536A'},summaryList:{marginTop:8},summaryRow:{height:45,backgroundColor:C.panel,borderRadius:11,borderWidth:1,borderColor:C.line,flexDirection:'row',alignItems:'center',paddingHorizontal:9,marginBottom:5},summaryHole:{width:30,height:30,borderRadius:9,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'},summaryHoleNo:{fontSize:11,fontWeight:'900',color:C.gold},summaryPar:{fontSize:9,fontWeight:'800',color:C.muted,marginLeft:10,flex:1},summaryScore:{fontSize:16,fontWeight:'900',color:C.navy,width:35,textAlign:'center'},summaryDelta:{fontSize:12,fontWeight:'900',color:C.blue,width:30,textAlign:'right'}
});
