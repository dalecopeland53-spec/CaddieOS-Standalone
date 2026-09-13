import React, {useMemo, useState} from 'react';
import {SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, TextInput, TouchableOpacity, View} from 'react-native';

const DEFAULT_BAG=[['Driver',230],['3W',210],['5W',195],['4i',180],['5i',170],['6i',160],['7i',150],['8i',140],['9i',130],['PW',115],['GW',100],['SW',85],['LW',70],['Putter',0]];
const LIES=['Tee','Fairway','Light Rough','Rough','Deep Rough','Fairway Bunker','Greenside Bunker'];

function playsLike(distance, wind, elevation, lie){
  let d=Math.max(0,Number(distance)||0);
  const liePct={'Tee':0,'Fairway':0,'Light Rough':.015,'Rough':.04,'Deep Rough':.07,'Fairway Bunker':.045,'Greenside Bunker':0}[lie]||0;
  d*=1+liePct;
  d+=(Number(wind)||0)*0.75;
  d*=1+(Number(elevation)||0)/100;
  return Math.max(0,Math.round(d));
}
function clubFor(yards,bag){
  if(!yards) return bag[bag.length-1];
  return bag.filter(x=>x[1]>0).reduce((best,c)=>Math.abs(c[1]-yards)<Math.abs(best[1]-yards)?c:best,bag[0]);
}
function adviceFor(yards,club,lie,wind){
  if(lie==='Greenside Bunker' && yards<=45) return `Use ${yards<=25?'LW':'SW'}. Open the face, use the bounce and commit.`;
  const windTxt=Number(wind)>0?' Into the wind.':Number(wind)<0?' Wind helping.':'';
  const lieTxt=lie==='Fairway'||lie==='Tee'?'':` Allow for ${lie.toLowerCase()}.`;
  return `Playing ${yards} yards. ${club}. ${lieTxt}${windTxt} Pick the target and commit.`.replace(/\s+/g,' ');
}

export default function App(){
  const [tab,setTab]=useState('CADDIE');
  const [distance,setDistance]=useState('150');
  const [wind,setWind]=useState('0');
  const [elevation,setElevation]=useState('0');
  const [lie,setLie]=useState('Fairway');
  const [course,setCourse]=useState('');
  const [player,setPlayer]=useState('Player');
  const [hole,setHole]=useState('1');
  const [bag,setBag]=useState(DEFAULT_BAG);
  const [scores,setScores]=useState(Array(18).fill(''));
  const result=useMemo(()=>{const y=playsLike(distance,wind,elevation,lie);const c=clubFor(y,bag);return{yards:y,club:c[0],carry:c[1]}},[distance,wind,elevation,lie,bag]);
  const total=scores.reduce((a,b)=>a+(Number(b)||0),0);
  const setBagCarry=(i,v)=>setBag(prev=>prev.map((x,n)=>n===i?[x[0],Math.max(0,Number(v)||0)]:x));

  return <SafeAreaView style={s.safe}>
    <StatusBar barStyle="dark-content" backgroundColor="#E7E1D6"/>
    <View style={s.header}>
      <Text style={s.brand}>TALKING <Text style={s.blue}>CADDIE</Text></Text>
      <Text style={s.tag}>YOUR CADDIE • YOUR GAME</Text>
    </View>
    <View style={s.nav}>{['CADDIE','BAG','COURSE','SCORE'].map(x=><TouchableOpacity key={x} onPress={()=>setTab(x)} style={[s.navBtn,tab===x&&s.navOn]}><Text style={[s.navText,tab===x&&s.navTextOn]}>{x}</Text></TouchableOpacity>)}</View>
    <ScrollView contentContainerStyle={s.body} keyboardShouldPersistTaps="handled">
      {tab==='CADDIE'&&<>
        <View style={s.hero}><Text style={s.kicker}>CURRENT SHOT</Text><Text style={s.big}>{result.yards} yd</Text><Text style={s.clubBig}>{result.club}</Text><Text style={s.sub}>Stock carry {result.carry} yd • {lie}</Text></View>
        <View style={s.voiceBox}><Text style={s.voiceTitle}>CADDIE RESPONSE</Text><Text style={s.voiceText}>{adviceFor(result.yards,result.club,lie,wind)}</Text></View>
        <Field label="TARGET DISTANCE (YARDS)" value={distance} set={setDistance}/>
        <Field label="WIND MPH  (+ HEAD / - TAIL)" value={wind} set={setWind}/>
        <Field label="ELEVATION %  (+ UP / - DOWN)" value={elevation} set={setElevation}/>
        <Text style={s.label}>LIE</Text><View style={s.wrap}>{LIES.map(x=><TouchableOpacity key={x} onPress={()=>setLie(x)} style={[s.chip,lie===x&&s.chipOn]}><Text style={[s.chipText,lie===x&&s.chipTextOn]}>{x}</Text></TouchableOpacity>)}</View>
        <View style={s.mic}><Text style={s.micIcon}>🎙️</Text><View style={{flex:1}}><Text style={s.micTitle}>VOICE CADDIE</Text><Text style={s.micText}>Install build first. Microphone/GPS permissions are reserved for the native voice update.</Text></View></View>
      </>}
      {tab==='BAG'&&<View style={s.card}><Text style={s.section}>MY BAG • 14 CLUBS</Text>{bag.map(([n,d],i)=><View style={s.row} key={n}><Text style={s.club}>{n}</Text><TextInput style={s.carryInput} keyboardType="numeric" value={String(d)} onChangeText={v=>setBagCarry(i,v)} editable={n!=='Putter'}/><Text style={s.unit}>yd</Text></View>)}</View>}
      {tab==='COURSE'&&<><View style={s.card}><Text style={s.section}>ROUND SETUP</Text><TextInput style={s.input} placeholder="Player name" placeholderTextColor="#7C838B" value={player} onChangeText={setPlayer}/><TextInput style={s.input} placeholder="Course name" placeholderTextColor="#7C838B" value={course} onChangeText={setCourse}/><TextInput style={s.input} placeholder="Hole" placeholderTextColor="#7C838B" keyboardType="numeric" value={hole} onChangeText={setHole}/><Text style={s.summary}>{player} • {course||'Course not set'} • Hole {hole}</Text></View><View style={s.card}><Text style={s.section}>ON-DEVICE ENGINE</Text><Text style={s.copy}>Shot calculations run locally. Distance, lie, wind and elevation are combined before club selection.</Text></View></>}
      {tab==='SCORE'&&<View style={s.card}><Text style={s.section}>18-HOLE SCORECARD</Text><View style={s.scoreGrid}>{scores.map((v,i)=><View key={i} style={s.scoreCell}><Text style={s.holeNo}>{i+1}</Text><TextInput style={s.scoreInput} keyboardType="numeric" value={v} onChangeText={t=>setScores(p=>p.map((x,n)=>n===i?t:x))}/></View>)}</View><View style={s.total}><Text style={s.totalLabel}>TOTAL</Text><Text style={s.totalNo}>{total||'—'}</Text></View></View>}
    </ScrollView>
  </SafeAreaView>
}
function Field({label,value,set}){return <View><Text style={s.label}>{label}</Text><TextInput value={value} onChangeText={set} keyboardType="numbers-and-punctuation" style={s.input}/></View>}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#E7E1D6'},header:{paddingTop:14,paddingBottom:8,alignItems:'center'},brand:{fontSize:26,fontWeight:'900',letterSpacing:1.2,color:'#172A45'},blue:{color:'#0A5B9F'},tag:{fontSize:10,fontWeight:'900',letterSpacing:1.5,color:'#596574',marginTop:2},nav:{flexDirection:'row',paddingHorizontal:10,gap:6},navBtn:{flex:1,paddingVertical:10,borderRadius:9,borderWidth:1,borderColor:'#9FA5AA',alignItems:'center',backgroundColor:'#F2EEE6'},navOn:{backgroundColor:'#17365D',borderColor:'#17365D'},navText:{fontSize:11,fontWeight:'900',color:'#17365D'},navTextOn:{color:'#FFF'},body:{padding:10,paddingBottom:28},hero:{backgroundColor:'#F7F3EA',borderRadius:14,padding:14,marginBottom:9,borderWidth:1,borderColor:'#C5BFB5'},kicker:{fontSize:11,fontWeight:'900',letterSpacing:1.4,color:'#68727D'},big:{fontSize:48,fontWeight:'900',color:'#17365D',lineHeight:54},clubBig:{fontSize:30,fontWeight:'900',color:'#0A5B9F'},sub:{fontSize:13,fontWeight:'700',color:'#5D6670',marginTop:2},voiceBox:{backgroundColor:'#17365D',borderRadius:14,padding:14,marginBottom:8},voiceTitle:{color:'#B9D0E5',fontSize:11,fontWeight:'900',letterSpacing:1.2},voiceText:{color:'#FFF',fontSize:18,fontWeight:'800',lineHeight:25,marginTop:5},label:{fontSize:10,fontWeight:'900',letterSpacing:1,color:'#34465C',marginBottom:4,marginTop:5},input:{backgroundColor:'#FFFDF8',borderWidth:1,borderColor:'#B8B5AE',borderRadius:9,paddingHorizontal:11,paddingVertical:9,fontSize:16,fontWeight:'800',color:'#172A45',marginBottom:5},wrap:{flexDirection:'row',flexWrap:'wrap',gap:6,marginBottom:8},chip:{paddingVertical:8,paddingHorizontal:9,borderRadius:8,borderWidth:1,borderColor:'#9BA4AE',backgroundColor:'#F8F5EF'},chipOn:{backgroundColor:'#17365D'},chipText:{fontWeight:'800',color:'#17365D',fontSize:11},chipTextOn:{color:'#FFF'},mic:{flexDirection:'row',alignItems:'center',gap:10,backgroundColor:'#F7F3EA',borderWidth:1,borderColor:'#C5BFB5',borderRadius:12,padding:12,marginTop:4},micIcon:{fontSize:28},micTitle:{fontSize:12,fontWeight:'900',color:'#17365D'},micText:{fontSize:11,color:'#66717C',marginTop:2},card:{backgroundColor:'#F7F3EA',borderRadius:14,padding:14,marginBottom:10,borderWidth:1,borderColor:'#C5BFB5'},section:{fontSize:17,fontWeight:'900',color:'#17365D',marginBottom:9},row:{flexDirection:'row',alignItems:'center',paddingVertical:5,borderBottomWidth:1,borderBottomColor:'#DDD7CD'},club:{flex:1,fontWeight:'900',color:'#17365D'},carryInput:{width:74,textAlign:'right',backgroundColor:'#FFF',borderWidth:1,borderColor:'#C3C0BA',borderRadius:7,paddingHorizontal:8,paddingVertical:6,fontWeight:'900',color:'#17365D'},unit:{width:28,textAlign:'right',fontWeight:'800',color:'#68717B'},summary:{fontWeight:'800',color:'#17365D',marginTop:7},copy:{fontSize:14,lineHeight:20,color:'#59636F'},scoreGrid:{flexDirection:'row',flexWrap:'wrap',gap:6},scoreCell:{width:'15%',minWidth:48,alignItems:'center',backgroundColor:'#EEE8DE',borderRadius:8,padding:5},holeNo:{fontSize:10,fontWeight:'900',color:'#59636F'},scoreInput:{width:'100%',textAlign:'center',backgroundColor:'#FFF',borderRadius:6,paddingVertical:5,fontSize:16,fontWeight:'900',color:'#17365D',marginTop:3},total:{flexDirection:'row',justifyContent:'space-between',alignItems:'center',marginTop:12,paddingTop:10,borderTopWidth:2,borderTopColor:'#17365D'},totalLabel:{fontWeight:'900',color:'#17365D'},totalNo:{fontSize:26,fontWeight:'900',color:'#0A5B9F'}});