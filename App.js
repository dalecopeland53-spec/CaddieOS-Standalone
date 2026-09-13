import React,{useMemo,useState}from'react';
import{SafeAreaView,ScrollView,StatusBar,StyleSheet,Text,TextInput,TouchableOpacity,View}from'react-native';

const NAV=['HOME','CADDIE','BAG','COURSE','SCORE'];
const BAG0=[['Driver',230],['3W',210],['5W',195],['4i',180],['5i',170],['6i',160],['7i',150],['8i',140],['9i',130],['PW',115],['GW',100],['SW',85],['LW',70],['Putter',0]];
const LIES=['Tee','Fairway','Light Rough','Rough','Deep Rough','Fairway Bunker','Greenside Bunker'];
const TEES=['Black','Blue','White','Red','Yellow'];
const PARS=[4,5,4,3,4,4,4,5,4,4,3,4,5,4,5,3,3,4];

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
 const result=useMemo(()=>{const y=playsLike(distance,wind,elev,lie),c=nearestClub(y,bag);return{y,club:c[0],carry:c[1]}},[distance,wind,elev,lie,bag]);
 const total=scores.reduce((a,b)=>a+(Number(b)||0),0);
 const parTotal=PARS.reduce((a,b)=>a+b,0);
 const played=scores.filter(Boolean).length;
 const toPar=played?scores.reduce((a,v,i)=>a+(v?Number(v)-PARS[i]:0),0):0;
 return <SafeAreaView style={s.safe}>
  <StatusBar barStyle="dark-content" backgroundColor="#EEE9DE"/>
  <Header/>
  <ScrollView contentContainerStyle={s.body} keyboardShouldPersistTaps="handled">
   {tab==='HOME'&&<Home go={setTab} course={course} hole={hole} total={total} played={played}/>} 
   {tab==='CADDIE'&&<Caddie result={result} distance={distance} setDistance={setDistance} wind={wind} setWind={setWind} elev={elev} setElev={setElev} lie={lie} setLie={setLie} hole={hole}/>} 
   {tab==='BAG'&&<Bag bag={bag} setBag={setBag}/>} 
   {tab==='COURSE'&&<Course course={course} setCourse={setCourse} tee={tee} setTee={setTee} hole={hole} setHole={setHole}/>} 
   {tab==='SCORE'&&<Score scores={scores} setScores={setScores} total={total} parTotal={parTotal} toPar={toPar} played={played}/>} 
  </ScrollView>
  <BottomNav tab={tab} setTab={setTab}/>
 </SafeAreaView>;
}

function Header(){return <View style={s.header}><View style={s.iconButton}><Text style={s.iconBall}>●</Text><Text style={s.iconC}>C</Text></View><View style={s.brandBox}><Text style={s.brand}>Caddie<Text style={s.blue}>OS</Text></Text><Text style={s.tag}>YOUR CADDIE • YOUR GAME</Text></View></View>}

function BottomNav({tab,setTab}){return <View style={s.bottomNav}>{NAV.map(x=><TouchableOpacity key={x} onPress={()=>setTab(x)} style={s.bottomItem}><View style={[s.navGlyph,tab===x&&s.navGlyphOn]}><Text style={[s.navGlyphText,tab===x&&s.navGlyphTextOn]}>{x==='HOME'?'⌂':x==='CADDIE'?'●':x==='BAG'?'◇':x==='COURSE'?'⌖':'≡'}</Text></View><Text style={[s.bottomTxt,tab===x&&s.bottomTxtOn]}>{x==='SCORE'?'SCORE':x}</Text></TouchableOpacity>)}</View>}

function Home({go,course,hole,total,played}){return <>
 <View style={s.topCard}><View><Text style={s.kicker}>CADDIEOS</Text><Text style={s.pageTitle}>{course||'Ready to play'}</Text><Text style={s.subline}>{course?`Hole ${hole} • Round ready`:'Set your course, bag and start your round.'}</Text></View><View style={s.readyPill}><Text style={s.readyDot}>●</Text><Text style={s.readyText}>READY</Text></View></View>
 <TouchableOpacity onPress={()=>go('CADDIE')} style={s.startRound}><View><Text style={s.startSmall}>YOUR ROUND</Text><Text style={s.startTitle}>START ROUND</Text></View><Text style={s.chev}>›</Text></TouchableOpacity>
 <View style={s.quickGrid}>{[['CADDIE','CADDIE','Shot advice','●'],['BAG','MY BAG','14 clubs','◇'],['COURSE','COURSE','Round setup','⌖'],['SCORE','SCORECARD',played?`${played} holes • ${total}`:'18 holes','≡']].map(([goTo,title,sub,icon])=><TouchableOpacity key={goTo} onPress={()=>go(goTo)} style={s.quickTile}><Text style={s.quickIcon}>{icon}</Text><Text style={s.quickTitle}>{title}</Text><Text style={s.quickSub}>{sub}</Text></TouchableOpacity>)}</View>
 <View style={s.infoStrip}><View><Text style={s.infoLabel}>CURRENT HOLE</Text><Text style={s.infoValue}>{hole}</Text></View><View style={s.vline}/><View><Text style={s.infoLabel}>COURSE</Text><Text style={s.infoText}>{course||'Not selected'}</Text></View></View>
 </>}

function Caddie({result,distance,setDistance,wind,setWind,elev,setElev,lie,setLie,hole}){return <>
 <View style={s.pageHead}><View><Text style={s.kicker}>CADDIE</Text><Text style={s.pageTitle}>Hole {hole}</Text></View><View style={s.holeBadge}><Text style={s.holeBadgeText}>LIVE</Text></View></View>
 <View style={s.caddiePanel}><View style={s.caddieLeft}><Text style={s.metricLabel}>PLAYS LIKE</Text><Text style={s.bigDistance}>{result.y}<Text style={s.bigUnit}> yd</Text></Text><Text style={s.clubCall}>{result.club}</Text><Text style={s.carry}>Stock carry {result.carry} yd</Text></View><View style={s.clubBadge}><Text style={s.clubBadgeSmall}>CLUB</Text><Text style={s.clubBadgeBig}>{result.club}</Text></View></View>
 <View style={s.adviceBox}><Text style={s.adviceLabel}>CADDIE ADVICE</Text><Text style={s.adviceText}>{advice(result.y,result.club,lie,wind)}</Text></View>
 <TouchableOpacity style={s.micButton}><View style={s.micDisc}><Text style={s.micDot}>●</Text></View><View><Text style={s.micMain}>ASK CADDIE</Text><Text style={s.micSub}>Tap to speak</Text></View></TouchableOpacity>
 <View style={s.compactCard}><View style={s.fieldRow}><MiniField label="TARGET" value={distance} setValue={setDistance} suffix="yd"/><MiniField label="WIND" value={wind} setValue={setWind} suffix="mph"/><MiniField label="SLOPE" value={elev} setValue={setElev} suffix="%"/></View><Text style={s.label}>LIE</Text><View style={s.chips}>{LIES.map(x=><TouchableOpacity key={x} onPress={()=>setLie(x)} style={[s.chip,lie===x&&s.chipOn]}><Text style={[s.chipTxt,lie===x&&s.chipTxtOn]}>{x}</Text></TouchableOpacity>)}</View></View>
 </>}

function Bag({bag,setBag}){const change=(i,delta)=>setBag(p=>p.map((x,n)=>n===i?[x[0],x[0]==='Putter'?0:Math.max(0,x[1]+delta)]:x));return <>
 <View style={s.pageHead}><View><Text style={s.kicker}>MY BAG</Text><Text style={s.pageTitle}>14 Clubs</Text></View><View style={s.holeBadge}><Text style={s.holeBadgeText}>YARDS</Text></View></View>
 <View style={s.bagGrid}>{bag.map(([name,d],i)=><View key={name} style={s.bagClub}><View style={s.bagTop}><Text style={s.bagName}>{name}</Text><Text style={s.bagDist}>{d}<Text style={s.bagUnit}> yd</Text></Text></View><View style={s.bagControls}><TouchableOpacity onPress={()=>change(i,-1)} disabled={name==='Putter'} style={s.stepBtn}><Text style={s.stepTxt}>−</Text></TouchableOpacity><Text style={s.stockTxt}>{name==='Putter'?'PUTTING':'CARRY'}</Text><TouchableOpacity onPress={()=>change(i,1)} disabled={name==='Putter'} style={s.stepBtn}><Text style={s.stepTxt}>+</Text></TouchableOpacity></View></View>)}</View>
 <View style={s.notice}><Text style={s.noticeTitle}>PERSONAL CARRY</Text><Text style={s.noticeText}>Set normal carry distance, not your longest shot. CaddieOS uses these numbers for club selection.</Text></View>
 </>}

function Course({course,setCourse,tee,setTee,hole,setHole}){return <>
 <View style={s.pageHead}><View><Text style={s.kicker}>COURSE</Text><Text style={s.pageTitle}>{course||'Round Setup'}</Text></View><View style={s.holeBadge}><Text style={s.holeBadgeText}>GPS</Text></View></View>
 <View style={s.compactCard}><Text style={s.label}>COURSE NAME</Text><TextInput style={s.input} value={course} onChangeText={setCourse} placeholder="Enter course" placeholderTextColor="#7E858B"/>
 <Text style={s.label}>TEE COLOUR</Text><View style={s.teeRow}>{TEES.map(x=><TouchableOpacity key={x} onPress={()=>setTee(x)} style={[s.teeBtn,tee===x&&s.teeBtnOn]}><View style={[s.teeDot,x==='Black'&&{backgroundColor:'#202020'},x==='Blue'&&{backgroundColor:'#1765A7'},x==='White'&&{backgroundColor:'#FFFFFF'},x==='Red'&&{backgroundColor:'#B73632'},x==='Yellow'&&{backgroundColor:'#D4A91C'}]}/><Text style={[s.teeText,tee===x&&s.teeTextOn]}>{x}</Text></TouchableOpacity>)}</View>
 <Text style={s.label}>CURRENT HOLE</Text><View style={s.holeChooser}><TouchableOpacity onPress={()=>setHole(String(Math.max(1,Number(hole||1)-1)))} style={s.holeStep}><Text style={s.holeStepText}>−</Text></TouchableOpacity><View style={s.holeNumber}><Text style={s.holeNumberText}>{Math.min(18,Math.max(1,Number(hole)||1))}</Text></View><TouchableOpacity onPress={()=>setHole(String(Math.min(18,Number(hole||1)+1)))} style={s.holeStep}><Text style={s.holeStepText}>+</Text></TouchableOpacity></View></View>
 <View style={s.courseStatus}><View><Text style={s.infoLabel}>COURSE</Text><Text style={s.statusMain}>{course||'No course selected'}</Text></View><View style={s.statusRight}><Text style={s.infoLabel}>TEE</Text><Text style={s.statusMain}>{tee}</Text></View></View>
 </>}

function Score({scores,setScores,total,parTotal,toPar,played}){const setScore=(i,t)=>setScores(p=>p.map((x,n)=>n===i?t.replace(/[^0-9]/g,''):x));return <>
 <View style={s.pageHead}><View><Text style={s.kicker}>GAME REPORT</Text><Text style={s.pageTitle}>Scorecard</Text></View><View style={s.scoreSummary}><Text style={s.scoreSummaryLabel}>SCORE</Text><Text style={s.scoreSummaryValue}>{played?`${toPar>0?'+':''}${toPar}`:'—'}</Text></View></View>
 <View style={s.scoreRibbon}>{scores.map((v,i)=><View key={i} style={s.ribbonCell}><Text style={s.ribbonHole}>{i+1}</Text><Text style={s.ribbonScore}>{v||'•'}</Text></View>)}</View>
 <View style={s.scoreCard}><View style={s.scoreHeaderRow}><Text style={s.sectionTitle}>18-HOLE SCORECARD</Text><Text style={s.scoreMeta}>{played}/18 PLAYED</Text></View><View style={s.scoreGrid}>{scores.map((v,i)=><View key={i} style={s.scoreCell}><Text style={s.holeNo}>{i+1}</Text><Text style={s.parMini}>PAR {PARS[i]}</Text><TextInput style={s.scoreInput} keyboardType="numeric" maxLength={2} value={v} onChangeText={t=>setScore(i,t)} placeholder="—" placeholderTextColor="#9A9A93"/></View>)}</View>
 <View style={s.totals}><View><Text style={s.totalSmall}>PAR</Text><Text style={s.totalValue}>{parTotal}</Text></View><View><Text style={s.totalSmall}>SCORE</Text><Text style={s.totalValue}>{total||'—'}</Text></View><View><Text style={s.totalSmall}>TO PAR</Text><Text style={s.totalAccent}>{played?`${toPar>0?'+':''}${toPar}`:'—'}</Text></View></View></View>
 </>}

function MiniField({label,value,setValue,suffix}){return <View style={s.miniField}><Text style={s.miniLabel}>{label}</Text><View style={s.miniInputWrap}><TextInput style={s.miniInput} value={value} onChangeText={setValue} keyboardType="numbers-and-punctuation"/><Text style={s.miniSuffix}>{suffix}</Text></View></View>}

const C={bg:'#EEE9DE',panel:'#F7F4EC',panel2:'#E5E0D5',line:'#B9B7AF',navy:'#143E68',blue:'#0879BE',muted:'#66727E',gold:'#C99A34',dark:'#06192B',white:'#FFFFFF'};
const s=StyleSheet.create({
 safe:{flex:1,backgroundColor:C.bg},
 header:{height:82,flexDirection:'row',alignItems:'center',justifyContent:'center',paddingTop:6,paddingHorizontal:14},
 iconButton:{width:54,height:54,borderRadius:17,backgroundColor:C.dark,borderWidth:2,borderColor:C.blue,alignItems:'center',justifyContent:'center',shadowColor:'#000',shadowOpacity:.16,shadowRadius:5,elevation:4},
 iconBall:{position:'absolute',top:5,right:8,color:C.gold,fontSize:10},iconC:{color:C.gold,fontSize:31,fontWeight:'900'},
 brandBox:{marginLeft:10},brand:{fontSize:30,fontWeight:'900',color:C.navy,letterSpacing:.2},blue:{color:C.blue},tag:{fontSize:9,fontWeight:'900',letterSpacing:2,color:C.muted,marginTop:1},
 body:{paddingHorizontal:12,paddingTop:8,paddingBottom:18},
 pageHead:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:9,paddingHorizontal:2},kicker:{fontSize:10,fontWeight:'900',letterSpacing:1.8,color:C.muted},pageTitle:{fontSize:23,fontWeight:'900',color:C.navy,marginTop:1},subline:{fontSize:11,fontWeight:'700',color:C.muted,marginTop:3},
 holeBadge:{paddingHorizontal:12,paddingVertical:7,borderRadius:10,backgroundColor:C.navy},holeBadgeText:{fontSize:10,fontWeight:'900',letterSpacing:1,color:C.white},
 topCard:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:16,padding:14,marginBottom:9},readyPill:{flexDirection:'row',alignItems:'center',gap:5,backgroundColor:'#DCE8E1',borderRadius:12,paddingHorizontal:9,paddingVertical:6},readyDot:{color:'#2E7D56',fontSize:9},readyText:{fontSize:9,fontWeight:'900',color:'#2E6A4D'},
 startRound:{minHeight:92,backgroundColor:C.blue,borderRadius:16,paddingHorizontal:18,paddingVertical:15,flexDirection:'row',alignItems:'center',justifyContent:'space-between',marginBottom:9},startSmall:{fontSize:10,fontWeight:'900',letterSpacing:1.5,color:'#CAE3F3'},startTitle:{fontSize:25,fontWeight:'900',color:C.white,marginTop:2},chev:{fontSize:42,color:C.white,fontWeight:'300'},
 quickGrid:{flexDirection:'row',flexWrap:'wrap',gap:8},quickTile:{width:'48.8%',minHeight:104,backgroundColor:C.navy,borderRadius:14,padding:13,justifyContent:'center'},quickIcon:{fontSize:25,fontWeight:'900',color:'#66B8E6',marginBottom:5},quickTitle:{fontSize:14,fontWeight:'900',color:C.white},quickSub:{fontSize:10,fontWeight:'700',color:'#C8D7E5',marginTop:2},
 infoStrip:{marginTop:9,backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:14,padding:12,flexDirection:'row',alignItems:'center'},vline:{width:1,height:38,backgroundColor:'#D0CCC3',marginHorizontal:15},infoLabel:{fontSize:8,fontWeight:'900',letterSpacing:1,color:C.muted},infoValue:{fontSize:22,fontWeight:'900',color:C.navy},infoText:{fontSize:13,fontWeight:'800',color:C.navy,marginTop:3},
 caddiePanel:{backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:16,padding:14,flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:8},caddieLeft:{flex:1},metricLabel:{fontSize:9,fontWeight:'900',letterSpacing:1.4,color:C.muted},bigDistance:{fontSize:47,fontWeight:'900',color:C.navy,lineHeight:52},bigUnit:{fontSize:16,color:C.blue},clubCall:{fontSize:25,fontWeight:'900',color:C.blue},carry:{fontSize:10,fontWeight:'700',color:C.muted,marginTop:1},clubBadge:{width:88,height:88,borderRadius:18,backgroundColor:C.dark,borderWidth:2,borderColor:C.gold,alignItems:'center',justifyContent:'center'},clubBadgeSmall:{fontSize:8,fontWeight:'900',letterSpacing:1,color:'#D6C08E'},clubBadgeBig:{fontSize:20,fontWeight:'900',color:C.gold,marginTop:3},
 adviceBox:{backgroundColor:C.navy,borderRadius:15,padding:14,marginBottom:8},adviceLabel:{fontSize:9,fontWeight:'900',letterSpacing:1.4,color:'#BFD6E8'},adviceText:{fontSize:16,fontWeight:'800',lineHeight:22,color:C.white,marginTop:5},
 micButton:{backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:14,padding:10,flexDirection:'row',alignItems:'center',justifyContent:'center',gap:11,marginBottom:8},micDisc:{width:44,height:44,borderRadius:22,backgroundColor:C.blue,alignItems:'center',justifyContent:'center'},micDot:{fontSize:22,color:C.white},micMain:{fontSize:15,fontWeight:'900',color:C.navy},micSub:{fontSize:9,fontWeight:'700',color:C.muted,marginTop:1},
 compactCard:{backgroundColor:C.panel,borderWidth:1,borderColor:C.line,borderRadius:15,padding:11,marginBottom:8},fieldRow:{flexDirection:'row',gap:6},miniField:{flex:1},miniLabel:{fontSize:8,fontWeight:'900',letterSpacing:.7,color:C.muted,marginBottom:4},miniInputWrap:{flexDirection:'row',alignItems:'center',backgroundColor:C.white,borderWidth:1,borderColor:'#C8C5BC',borderRadius:9,paddingHorizontal:7},miniInput:{flex:1,paddingVertical:7,fontSize:15,fontWeight:'900',color:C.navy,textAlign:'center'},miniSuffix:{fontSize:8,fontWeight:'900',color:C.muted},
 label:{fontSize:8,fontWeight:'900',letterSpacing:1.1,color:C.muted,marginTop:9,marginBottom:5},chips:{flexDirection:'row',flexWrap:'wrap',gap:5},chip:{paddingVertical:7,paddingHorizontal:8,borderRadius:8,borderWidth:1,borderColor:'#B6B8B5',backgroundColor:'#F5F2EA'},chipOn:{backgroundColor:C.navy,borderColor:C.navy},chipTxt:{fontSize:9,fontWeight:'800',color:C.navy},chipTxtOn:{color:C.white},
 bagGrid:{flexDirection:'row',flexWrap:'wrap',gap:7},bagClub:{width:'48.9%',backgroundColor:C.panel,borderRadius:12,borderWidth:1,borderColor:C.line,padding:9},bagTop:{flexDirection:'row',justifyContent:'space-between',alignItems:'baseline'},bagName:{fontSize:12,fontWeight:'900',color:C.navy},bagDist:{fontSize:18,fontWeight:'900',color:C.navy},bagUnit:{fontSize:8,color:C.muted},bagControls:{flexDirection:'row',alignItems:'center',justifyContent:'space-between',marginTop:7},stepBtn:{width:28,height:26,borderRadius:8,borderWidth:1,borderColor:'#B7B4AA',alignItems:'center',justifyContent:'center',backgroundColor:'#ECE8DE'},stepTxt:{fontSize:17,fontWeight:'900',color:C.navy},stockTxt:{fontSize:7,fontWeight:'900',letterSpacing:.8,color:C.muted},notice:{marginTop:8,backgroundColor:C.panel2,borderRadius:12,padding:11,borderWidth:1,borderColor:'#C5C1B7'},noticeTitle:{fontSize:9,fontWeight:'900',letterSpacing:1,color:C.navy},noticeText:{fontSize:10,fontWeight:'700',lineHeight:15,color:C.muted,marginTop:3},
 input:{backgroundColor:C.white,borderRadius:9,borderWidth:1,borderColor:'#BAB8B0',paddingHorizontal:10,paddingVertical:9,fontSize:14,fontWeight:'800',color:C.navy},teeRow:{flexDirection:'row',gap:5},teeBtn:{flex:1,alignItems:'center',borderWidth:1,borderColor:'#B8B6AF',borderRadius:8,paddingVertical:7,backgroundColor:'#F4F1E9'},teeBtnOn:{backgroundColor:C.navy,borderColor:C.navy},teeDot:{width:11,height:11,borderRadius:6,borderWidth:1,borderColor:'#8A8A85',marginBottom:3},teeText:{fontSize:7,fontWeight:'900',color:C.navy},teeTextOn:{color:C.white},holeChooser:{flexDirection:'row',justifyContent:'center',alignItems:'center',gap:10},holeStep:{width:46,height:38,borderRadius:9,backgroundColor:C.navy,alignItems:'center',justifyContent:'center'},holeStepText:{fontSize:22,fontWeight:'900',color:C.white},holeNumber:{width:86,height:46,borderRadius:10,borderWidth:1,borderColor:C.line,backgroundColor:C.white,alignItems:'center',justifyContent:'center'},holeNumberText:{fontSize:26,fontWeight:'900',color:C.navy},courseStatus:{backgroundColor:C.panel,borderRadius:14,borderWidth:1,borderColor:C.line,padding:12,flexDirection:'row',justifyContent:'space-between'},statusMain:{fontSize:13,fontWeight:'900',color:C.navy,marginTop:3},statusRight:{alignItems:'flex-end'},
 scoreSummary:{backgroundColor:C.navy,borderRadius:11,minWidth:72,paddingHorizontal:11,paddingVertical:7,alignItems:'center'},scoreSummaryLabel:{fontSize:7,fontWeight:'900',letterSpacing:1,color:'#BFD4E6'},scoreSummaryValue:{fontSize:18,fontWeight:'900',color:C.white},scoreRibbon:{flexDirection:'row',backgroundColor:C.panel,borderRadius:12,borderWidth:1,borderColor:C.line,padding:5,marginBottom:8},ribbonCell:{flex:1,alignItems:'center'},ribbonHole:{fontSize:6,fontWeight:'900',color:C.muted},ribbonScore:{fontSize:8,fontWeight:'900',color:C.navy,marginTop:1},scoreCard:{backgroundColor:C.panel,borderRadius:15,borderWidth:1,borderColor:C.line,padding:10},scoreHeaderRow:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginBottom:7},sectionTitle:{fontSize:12,fontWeight:'900',letterSpacing:.8,color:C.navy},scoreMeta:{fontSize:8,fontWeight:'900',color:C.muted},scoreGrid:{flexDirection:'row',flexWrap:'wrap',gap:5},scoreCell:{width:'15.4%',backgroundColor:'#E5E1D8',borderRadius:8,borderWidth:1,borderColor:'#C8C4BA',padding:4,alignItems:'center'},holeNo:{fontSize:9,fontWeight:'900',color:C.navy},parMini:{fontSize:6,fontWeight:'800',color:C.muted,marginTop:1},scoreInput:{width:'100%',height:31,backgroundColor:C.white,borderRadius:6,textAlign:'center',fontSize:15,fontWeight:'900',color:C.navy,marginTop:3,paddingVertical:2},totals:{flexDirection:'row',justifyContent:'space-around',borderTopWidth:1,borderTopColor:'#CFCCC3',marginTop:10,paddingTop:9},totalSmall:{fontSize:7,fontWeight:'900',letterSpacing:1,color:C.muted,textAlign:'center'},totalValue:{fontSize:21,fontWeight:'900',color:C.navy,textAlign:'center'},totalAccent:{fontSize:21,fontWeight:'900',color:C.blue,textAlign:'center'},
 bottomNav:{height:64,backgroundColor:'#F6F3EC',borderTopWidth:1,borderTopColor:'#C8C4BA',flexDirection:'row',paddingHorizontal:8,paddingTop:6},bottomItem:{flex:1,alignItems:'center'},navGlyph:{width:30,height:25,borderRadius:9,alignItems:'center',justifyContent:'center'},navGlyphOn:{backgroundColor:C.navy},navGlyphText:{fontSize:14,fontWeight:'900',color:'#6E7880'},navGlyphTextOn:{color:C.white},bottomTxt:{fontSize:7,fontWeight:'900',color:'#6D757C',marginTop:2},bottomTxtOn:{color:C.navy}
});
