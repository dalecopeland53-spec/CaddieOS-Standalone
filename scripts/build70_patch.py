from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD70_PHONE_FIT' not in s:
    s=s.replace('const BUILD69_FIELD_TEST=true;', 'const BUILD69_FIELD_TEST=true;\nconst BUILD70_PHONE_FIT=true;', 1)

# Final S24 portrait fit: preserve the complete tagline and all nine score columns.
styles=",brandSub:{fontSize:6.4,color:C.navy,letterSpacing:.62},anti:{fontSize:7.2,color:C.navy,fontWeight:'900'},antiBtn:{flexShrink:0,borderWidth:1.5,borderColor:C.blue,borderRadius:14,paddingHorizontal:7,paddingVertical:6,backgroundColor:'#F7F9FA'},scoreLabel:{width:46,height:28,paddingHorizontal:2,textAlignVertical:'center',fontSize:7.5,fontWeight:'900',color:C.navy,borderWidth:.5,borderColor:C.line},scoreCellHead:{width:29,height:28,textAlign:'center',textAlignVertical:'center',fontSize:8,fontWeight:'900',color:C.navy,borderWidth:.5,borderColor:C.line},scoreCellPar:{width:29,height:27,textAlign:'center',textAlignVertical:'center',fontSize:8,color:C.muted,borderWidth:.5,borderColor:C.line},scoreCellInput:{width:29,height:30,textAlign:'center',textAlignVertical:'center',fontSize:9,fontWeight:'900',color:C.navy,backgroundColor:C.white,borderWidth:.5,borderColor:C.line,padding:0}"
idx=s.rfind('});')
if idx<0: raise SystemExit('Build 70: styles marker missing')
s=s[:idx]+styles+s[idx:]
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 70',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.70"',t,count=1)
    g.write_text(t)
print('Build 70 final phone-fit patch applied')
