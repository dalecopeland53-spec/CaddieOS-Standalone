from pathlib import Path
import re

APP=Path('CaddieOS/App.js')
s=APP.read_text()

if 'BUILD66_LOGIN' not in s:
    anchor='const BUILD65_WIND_UI=true;'
    if anchor in s:
        s=s.replace(anchor,anchor+'\nconst BUILD66_LOGIN=true;',1)
    else:
        s="const BUILD66_LOGIN=true;\n"+s

# Remove the obsolete email/social-auth login and replace it with the compact
# CaddieOS player entry used for the on-device build.
s=s.replace('<Welcome player={player} setPlayer={setPlayer} email={email} setEmail={setEmail} enter={()=>setEntered(true)}/>','<Welcome player={player} setPlayer={setPlayer} enter={()=>setEntered(true)}/>',1)

s=re.sub(r'function Welcome\([^)]*\)\{return .*?\}\nfunction Home', '''function Welcome({player,setPlayer,enter}){return <ScrollView contentContainerStyle={s.loginBody} keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}><View style={s.loginHero}><Text style={s.loginEyebrow}>YOUR CADDIE · YOUR GAME</Text><Text style={s.loginMark}>CADDIE<Text style={s.brandGold}>OS</Text></Text><View style={s.loginRule}/><Text style={s.loginTitle}>Welcome</Text><Text style={s.loginSub}>Tour-level decisions. Personal numbers. One simple system.</Text></View><View style={s.loginCard}><Text style={s.loginCardTitle}>PLAYER PROFILE</Text><Text style={s.loginCardSub}>Enter your name to continue</Text><Field label="PLAYER NAME" value={player} onChangeText={setPlayer}/><Btn text="ENTER CADDIEOS" onPress={enter}/><Text style={s.loginPrivacy}>No email required · Your golf data stays with your profile</Text></View><View style={s.loginFeatureRow}><View style={s.loginFeature}><Text style={s.loginFeatureBig}>GPS</Text><Text style={s.loginFeatureSmall}>LIVE DISTANCE</Text></View><View style={s.loginFeature}><Text style={s.loginFeatureBig}>VOICE</Text><Text style={s.loginFeatureSmall}>CADDIE</Text></View><View style={s.loginFeature}><Text style={s.loginFeatureBig}>18</Text><Text style={s.loginFeatureSmall}>HOLE SCORING</Text></View></View><Text style={s.loginFoot}>CADDIEOS · BUILT FOR THE COURSE</Text></ScrollView>}\nfunction Home''',s,count=1,flags=re.S)

# Premium compact silver/champagne login additions. These append after existing
# styles so the approved login treatment wins without disturbing other screens.
insert=",loginHero:{alignItems:'center',paddingTop:16,paddingBottom:14},loginEyebrow:{fontSize:9,fontWeight:'900',letterSpacing:2,color:C.blue,marginBottom:6},loginRule:{width:52,height:3,borderRadius:2,backgroundColor:C.gold,marginTop:8,marginBottom:12},loginCardTitle:{fontSize:12,fontWeight:'900',letterSpacing:1.5,color:C.navy,marginBottom:2},loginCardSub:{fontSize:10,fontWeight:'700',color:C.muted,marginBottom:12},loginPrivacy:{fontSize:9,fontWeight:'700',color:C.muted,textAlign:'center',marginTop:10},loginFeatureRow:{flexDirection:'row',gap:7,marginTop:10},loginFeature:{flex:1,alignItems:'center',justifyContent:'center',minHeight:58,borderRadius:10,borderWidth:1,borderColor:C.line,backgroundColor:'#F7F9FA'},loginFeatureBig:{fontSize:14,fontWeight:'900',color:C.navy},loginFeatureSmall:{fontSize:7,fontWeight:'900',letterSpacing:.7,color:C.blue,marginTop:2}"
idx=s.rfind('});')
if idx!=-1 and 'loginFeatureRow' not in s[idx-7000:]:
    s=s[:idx]+insert+s[idx:]

APP.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 66',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.66"',t,count=1)
    g.write_text(t)

print('Build 66 approved login patch applied')
