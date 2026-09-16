from pathlib import Path
import re

p=Path('CaddieOS/App.js');s=p.read_text()
if 'BUILD88_GPS_STREAM_TARGET_FIX' not in s:
    marker='const BUILD87_NEARBY_COURSE_LOCK=true;'
    if marker not in s: raise SystemExit('Build 87 marker missing')
    s=s.replace(marker,marker+'\nconst BUILD88_GPS_STREAM_TARGET_FIX=true;',1)

# Start with an immediate hardware fix, then keep streaming positions. A watch error
# must not leave the UI claiming LIVE GPS is active.
old="const startLiveGPS=async()=>{if(!await allowGPS())return;if(gpsWatch.current!==null)Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=Geolocation.watchPosition(setGPSPoint,()=>{}, {enableHighAccuracy:true,distanceFilter:2,interval:2500,fastestInterval:1200,maximumAge:1500});setGpsLive(true)};"
new="const startLiveGPS=async()=>{if(!await allowGPS())return;if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}Geolocation.getCurrentPosition(setGPSPoint,e=>{setGpsLive(false);Alert.alert('GPS','Could not get a live GPS fix. Check Location is switched on and allowed for CaddieOS.')},{enableHighAccuracy:true,timeout:15000,maximumAge:1000});gpsWatch.current=Geolocation.watchPosition(setGPSPoint,e=>{if(gpsWatch.current!==null){Geolocation.clearWatch(gpsWatch.current);gpsWatch.current=null}setGpsLive(false);Alert.alert('GPS','Live GPS tracking stopped. Check Location permission and GPS signal.')},{enableHighAccuracy:true,distanceFilter:1,interval:2000,fastestInterval:1000,maximumAge:1000});setGpsLive(true)};"
if old not in s: raise SystemExit('Build 60 live GPS engine anchor missing')
s=s.replace(old,new,1)

# Build 86 accidentally made STOP immediately restart GPS because gpsLive was an
# effect dependency. Auto-start only when the selected real course itself changes.
bad="const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse&&!gpsLive)startLiveGPS?.()},[realCourse,gpsLive]);"
good="const BUILD85_AUTOGPS=true;useEffect(()=>{if(realCourse)startLiveGPS?.()},[realCourse]);"
if bad not in s: raise SystemExit('Build 86 auto GPS anchor missing')
s=s.replace(bad,good,1)

# The OSM target loader previously required the course record itself to contain
# coordinates. Fall back to the golfer's first real GPS fix, then run once when
# GPS changes from unavailable to available. This supplies a real Hole target
# without any mock coordinates.
oldfrag="const c=realCourse?.course||realCourse||{},lat=Number(c.latitude??c.lat??c.location?.lat??c.coordinates?.lat),lon=Number(c.longitude??c.lon??c.lng??c.location?.lon??c.location?.lng??c.coordinates?.lon??c.coordinates?.lng);if(!Number.isFinite(lat)||!Number.isFinite(lon))return()=>{alive=false};"
newfrag="const c=realCourse?.course||realCourse||{},courseLat=Number(c.latitude??c.lat??c.location?.lat??c.coordinates?.lat),courseLon=Number(c.longitude??c.lon??c.lng??c.location?.lon??c.location?.lng??c.coordinates?.lon??c.coordinates?.lng),gpsLat=Number(gps?.lat),gpsLon=Number(gps?.lon),lat=Number.isFinite(courseLat)?courseLat:gpsLat,lon=Number.isFinite(courseLon)?courseLon:gpsLon;if(!Number.isFinite(lat)||!Number.isFinite(lon))return()=>{alive=false};"
if oldfrag not in s: raise SystemExit('Build 85 OSM coordinate anchor missing')
s=s.replace(oldfrag,newfrag,1)
# Only transition from no GPS to GPS retriggers this query, not every moving position.
s=s.replace("}).catch(()=>{});return()=>{alive=false}},[realCourse]);", "}).catch(()=>{});return()=>{alive=false}},[realCourse,!!gps]);",1)

p.write_text(s)
g=Path('CaddieOS/android/app/build.gradle')
if g.exists():
    t=g.read_text();t=re.sub(r'versionCode\s+\d+','versionCode 88',t,count=1);t=re.sub(r'versionName\s+\"[^\"]+\"','versionName \"1.0.88\"',t,count=1);g.write_text(t)
print('Build 88 live GPS stream + STOP control + real target fallback applied')
