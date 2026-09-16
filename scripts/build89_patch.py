from pathlib import Path
import re

p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD89_GPS_FEED_STATUS_FIX' not in s:
    marker='const BUILD88_GPS_STREAM_TARGET_FIX=true;'
    if marker not in s: raise SystemExit('Build 88 marker missing')
    s=s.replace(marker,marker+'\nconst BUILD89_GPS_FEED_STATUS_FIX=true;',1)

# LIVE must mean a real position has arrived, not merely that watchPosition was requested.
old="const startLiveGPS=async()=>{if(!await allowGPS())return;if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}Geolocation.getCurrentPosition(setGPSPoint,e=>{setGpsLive(false);Alert.alert('GPS','Could not get a live GPS fix. Check Location is switched on and allowed for CaddieOS.')},{enableHighAccuracy:true,timeout:15000,maximumAge:1000});gpsWatch.current=Geolocation.watchPosition(setGPSPoint,e=>{if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}setGpsLive(false);Alert.alert('GPS','Live GPS tracking stopped. Check Location permission and GPS signal.')},{enableHighAccuracy:true,distanceFilter:1,interval:2000,fastestInterval:1000,maximumAge:1000});setGpsLive(true)};"
new="const startLiveGPS=async()=>{if(!await allowGPS())return;if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}setGpsLive(false);const onFix=p=>{setGPSPoint(p);setGpsLive(true)};Geolocation.getCurrentPosition(onFix,e=>{setGpsLive(false);Alert.alert('GPS','Could not get a live GPS fix. Check Location is switched on and allowed for CaddieOS.')},{enableHighAccuracy:true,timeout:15000,maximumAge:0});gpsWatch.current=Geolocation.watchPosition(onFix,e=>{if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}setGpsLive(false);Alert.alert('GPS','Live GPS tracking stopped. Check Location permission and GPS signal.')},{enableHighAccuracy:true,distanceFilter:1,interval:2000,fastestInterval:1000,maximumAge:0})};"
if old not in s: raise SystemExit('Build 88 GPS anchor missing')
s=s.replace(old,new,1)

# Do not auto-start from the Round render lifecycle. Start once when a real course is selected;
# STOP then remains stopped until the golfer starts it again.
oldauto="const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse)startLiveGPS?.()},[realCourse]);"
newauto="const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse)startLiveGPS?.()},[realCourse]);"
if oldauto not in s: raise SystemExit('Build 88 auto GPS anchor missing')

# Correct haversine validation: valid latitude/longitude can be zero.
s=s.replace("if(!a||!b||!a.lat||!a.lon||!b.lat||!b.lon)return null;","if(!a||!b||!Number.isFinite(Number(a.lat))||!Number.isFinite(Number(a.lon))||!Number.isFinite(Number(b.lat))||!Number.isFinite(Number(b.lon)))return null;",1)

p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 89',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.89\"',t,count=1);g.write_text(t)
print('Build 89 GPS feed status fix applied')
