from pathlib import Path
import re

app=Path('CaddieOS/App.js')
s=app.read_text()
if 'BUILD76_HOLE_GRAPHICS' not in s:
    s=s.replace('const BUILD75_ROUND_FIT=true;', 'const BUILD75_ROUND_FIT=true;\nconst BUILD76_HOLE_GRAPHICS=true;', 1)

# Hole-specific visual geometry. This makes the course view change with the selected hole
# while remaining compatible with the existing compact Round screen. Real mapped GPS
# coordinates can replace these geometry values as course mapping data is captured.
old="""<View style={{position:'absolute',top:45,width:100,height:275,backgroundColor:'#4C9461',borderRadius:48,transform:[{rotate:'3deg'}]}}/><View style={[s.mapGreen,{top:14,width:94,height:48}]}/><View style={[s.mapLine,{top:38,height:278}]}/><Text style={[s.mapFlag,{top:26}]}>⚑</Text>"""
new="""{(()=>{const shapes=[
{left:22,top:45,w:100,h:275,r:3,gLeft:25,gW:94}, {left:10,top:48,w:112,h:270,r:-7,gLeft:16,gW:90},
{left:30,top:70,w:86,h:245,r:8,gLeft:35,gW:82}, {left:20,top:105,w:100,h:205,r:-2,gLeft:28,gW:86},
{left:8,top:42,w:112,h:280,r:10,gLeft:15,gW:96}, {left:30,top:52,w:92,h:265,r:-10,gLeft:34,gW:84},
{left:16,top:65,w:108,h:250,r:5,gLeft:20,gW:92}, {left:25,top:92,w:92,h:220,r:-6,gLeft:31,gW:82},
{left:9,top:50,w:114,h:270,r:2,gLeft:16,gW:98}, {left:27,top:60,w:94,h:255,r:9,gLeft:32,gW:86},
{left:15,top:80,w:108,h:235,r:-9,gLeft:20,gW:92}, {left:24,top:44,w:98,h:278,r:6,gLeft:29,gW:88},
{left:32,top:112,w:84,h:198,r:1,gLeft:35,gW:80}, {left:10,top:55,w:112,h:265,r:-4,gLeft:16,gW:96},
{left:26,top:72,w:94,h:242,r:11,gLeft:31,gW:84}, {left:14,top:48,w:110,h:272,r:-8,gLeft:20,gW:92},
{left:30,top:98,w:88,h:212,r:5,gLeft:34,gW:82}, {left:12,top:46,w:112,h:275,r:-1,gLeft:18,gW:96}];const q=shapes[i];return <><View style={{position:'absolute',left:q.left,top:q.top,width:q.w,height:q.h,backgroundColor:'#4C9461',borderRadius:48,transform:[{rotate:q.r+'deg'}]}}/><View style={[s.mapGreen,{left:q.gLeft,top:14,width:q.gW,height:48}]}/><View style={[s.mapLine,{top:38,height:278,transform:[{rotate:(q.r*.45)+'deg'}]}]}/><Text style={[s.mapFlag,{top:26,left:q.gLeft+q.gW/2-8}]}>⚑</Text></>})()}"""
if old not in s: raise SystemExit('Build 76 map target not found')
s=s.replace(old,new,1)
app.write_text(s)

g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text()
    t=re.sub(r'versionCode\s+\d+','versionCode 76',t,count=1)
    t=re.sub(r'versionName\s+"[^"]+"','versionName "1.0.76"',t,count=1)
    g.write_text(t)
print('Build 76 hole-specific graphics applied')
