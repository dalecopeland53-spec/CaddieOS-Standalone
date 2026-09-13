import React, {useMemo, useState} from 'react';
import {SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, TextInput, TouchableOpacity, View} from 'react-native';

const BAG=[
 ['Driver',230],['3W',210],['5W',195],['4i',180],['5i',170],['6i',160],['7i',150],['8i',140],['9i',130],['PW',115],['GW',100],['SW',85],['LW',70]
];

function playsLike(distance, windMph, elevationPct, lie){
  let d=Number(distance)||0;
  const liePct={Tee:0,Fairway:0,Rough:.04,'Deep Rough':.07,'Fairway Bunker':.045,'Greenside Bunker':0}[lie]||0;
  d*=1+liePct;
  d+=Number(windMph||0)*0.75;
  d*=1+(Number(elevationPct||0)/100);
  return Math.max(0,Math.round(d));
}
function clubFor(yards){
  return BAG.reduce((best,c)=>Math.abs(c[1]-yards)<Math.abs(best[1]-yards)?c:best,BAG[0]);
}

export default function App(){
 const [tab,setTab]=useState('CADDIE');
 const [distance,setDistance]=useState('150');
 const [wind,setWind]=useState('0');
 const [elev,setElev]=useState('0');
 const [lie,setLie]=useState('Fairway');
 const [player,setPlayer]=useState('Player');
 const [course,setCourse]=useState('');
 const [hole,setHole]=useState('1');
 const result=useMemo(()=>{const y=playsLike(distance,wind,elev,lie); const c=clubFor(y); return {y,c:c[0],carry:c[1]}},[distance,wind,elev,lie]);
 const lies=['Tee','Fairway','Rough','Deep Rough','Fairway Bunker','Greenside Bunker'];
 return <SafeAreaView style={s.safe}><StatusBar barStyle="dark-content" backgroundColor="#E9E5DC"/><View style={s.header}><Text style={s.brand}>CADDIE<Text style={s.blue}>OS</Text></Text><Text style={s.tag}>PRO TOUR SUITE • STANDALONE</Text></View>
 <View style={s.nav}>{['CADDIE','BAG','COURSE'].map(x=><TouchableOpacity key={x} onPress={()=>setTab(x)} style={[s.navBtn,tab===x&&s.navOn]}><Text style={[s.navText,tab===x&&s.navTextOn]}>{x}</Text></TouchableOpacity>)}</View>
 <ScrollView contentContainerStyle={s.body}>
 {tab==='CADDIE'&&<>
  <View style={s.card}><Text style={s.kicker}>LIVE SHOT</Text><Text style={s.big}>{result.y} yd</Text><Text style={s.reco}>{result.c}</Text><Text style={s.small}>Stock carry {result.carry} yd • {lie}</Text></View>
  <Field label="TARGET YARDS" value={distance} set={setDistance}/><Field label="HEADWIND MPH (+) / TAILWIND (-)" value={wind} set={setWind}/><Field label="ELEVATION % (+UP / -DOWN)" value={elev} set={setElev}/>
  <Text style={s.label}>LIE</Text><View style={s.wrap}>{lies.map(x=><TouchableOpacity key={x} onPress={()=>setLie(x)} style={[s.chip,lie===x&&s.chipOn]}><Text style={[s.chipText,lie===x&&s.chipTextOn]}>{x}</Text></TouchableOpacity>)}</View>
  <View style={s.answer}><Text style={s.answerTitle}>CADDIE ADVICE</Text><Text style={s.answerText}>{result.y<=45&&lie==='Greenside Bunker'?'Open the face, use the bounce and commit.':`Playing ${result.y} yards. ${result.c}. Commit to the number.`}</Text></View>
 </>}
 {tab==='BAG'&&<View style={s.card}><Text style={s.section}>ACTIVE BAG</Text>{BAG.map(([n,d])=><View style={s.row} key={n}><Text style={s.club}>{n}</Text><Text style={s.dist}>{d} yd</Text></View>)}</View>}
 {tab==='COURSE'&&<><View style={s.card}><Text style={s.section}>ROUND SETUP</Text><TextInput style={s.input} placeholder="Player name" value={player} onChangeText={setPlayer}/><TextInput style={s.input} placeholder="Course name" value={course} onChangeText={setCourse}/><TextInput style={s.input} placeholder="Hole" keyboardType="numeric" value={hole} onChangeText={setHole}/><Text style={s.small}>Current: {player} • {course||'Course not set'} • Hole {hole}</Text></View><View style={s.card}><Text style={s.section}>SYSTEM</Text><Text style={s.small}>Standalone calculation engine is active on-device. Server sync is optional.</Text></View></>}
 </ScrollView></SafeAreaView>
}
function Field({label,value,set}){return <View><Text style={s.label}>{label}</Text><TextInput value={value} onChangeText={set} keyboardType="numbers-and-punctuation" style={s.input}/></View>}
const s=StyleSheet.create({safe:{flex:1,backgroundColor:'#E9E5DC'},header:{padding:18,paddingBottom:10,alignItems:'center'},brand:{fontSize:30,fontWeight:'900',letterSpacing:2,color:'#182A45'},blue:{color:'#0B5FA5'},tag:{fontSize:11,fontWeight:'800',letterSpacing:1.2,color:'#5A6472',marginTop:2},nav:{flexDirection:'row',paddingHorizontal:12,gap:8},navBtn:{flex:1,padding:11,borderRadius:10,borderWidth:1,borderColor:'#9FA5AB',alignItems:'center',backgroundColor:'#F4F1EA'},navOn:{backgroundColor:'#17365D',borderColor:'#17365D'},navText:{fontWeight:'900',color:'#17365D'},navTextOn:{color:'#FFF'},body:{padding:12,paddingBottom:32},card:{backgroundColor:'#F7F4ED',borderRadius:14,padding:16,marginBottom:12,borderWidth:1,borderColor:'#C7C2B9'},kicker:{fontSize:12,fontWeight:'900',letterSpacing:1.5,color:'#65707D'},big:{fontSize:52,fontWeight:'900',color:'#17365D',lineHeight:58},reco:{fontSize:32,fontWeight:'900',color:'#0B5FA5'},small:{fontSize:13,color:'#5B6570',marginTop:4},label:{fontSize:11,fontWeight:'900',letterSpacing:1,color:'#34465C',marginBottom:5,marginTop:7},input:{backgroundColor:'#FFF',borderWidth:1,borderColor:'#B9B8B3',borderRadius:10,paddingHorizontal:12,paddingVertical:11,fontSize:18,fontWeight:'800',color:'#172A45',marginBottom:7},wrap:{flexDirection:'row',flexWrap:'wrap',gap:7,marginBottom:10},chip:{paddingVertical:9,paddingHorizontal:11,borderRadius:9,borderWidth:1,borderColor:'#9BA4AE',backgroundColor:'#F8F6F1'},chipOn:{backgroundColor:'#17365D'},chipText:{fontWeight:'800',color:'#17365D',fontSize:12},chipTextOn:{color:'#FFF'},answer:{backgroundColor:'#17365D',borderRadius:14,padding:16,marginTop:4},answerTitle:{color:'#AFC9E5',fontSize:11,fontWeight:'900',letterSpacing:1.2},answerText:{color:'#FFF',fontSize:19,fontWeight:'800',lineHeight:27,marginTop:6},section:{fontSize:18,fontWeight:'900',color:'#17365D',marginBottom:10},row:{flexDirection:'row',justifyContent:'space-between',paddingVertical:9,borderBottomWidth:1,borderBottomColor:'#DDD8CE'},club:{fontWeight:'900',color:'#17365D'},dist:{fontWeight:'800',color:'#4A5664'}});