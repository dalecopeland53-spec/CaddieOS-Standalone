import React, { useEffect, useMemo, useState } from 'react';
import {
  Alert,
  PermissionsAndroid,
  Platform,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  useWindowDimensions
} from 'react-native';
import { SafeAreaProvider, SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import Voice from '@react-native-voice/voice';
import Tts from 'react-native-tts';
import Geolocation from '@react-native-community/geolocation';
import AsyncStorage from '@react-native-async-storage/async-storage';

const C = {
  bg: '#071E2D', bg2: '#0A2A3E', panel: '#F2ECDD', panel2: '#E7DECA',
  navy: '#0A2A43', blue: '#0B7FC0', gold: '#D5AE52', gold2: '#F0CE77',
  text: '#0C2940', muted: '#667581', line: '#CDBE9E', dark: '#04131E',
  white: '#FFFDF7', green: '#DCE7D5'
};

const NAV = ['HOME', 'CADDIE', 'BAG', 'COURSE', 'MORE'];
const PARS = [4, 5, 4, 3, 4, 4, 4, 5, 4, 4, 3, 4, 5, 4, 5, 3, 3, 4]; // Fixed missing data
const LIES = ['Tee', 'Fairway', 'Light Rough', 'Rough', 'Deep Rough', 'Fairway Bunker', 'Greenside Bunker'];
const TEES = ['Black', 'Blue', 'White', 'Red', 'Yellow'];
const WIND = ['HEAD', 'TAIL', 'L→R', 'R→L'];

const CLUB_LIBRARY = [
  'Driver', '2 Wood', '3 Wood', '4 Wood', '5 Wood', '7 Wood', '9 Wood',
  '2 Hybrid', '3 Hybrid', '4 Hybrid', '5 Hybrid', '6 Hybrid', '2 Iron',
  '3 Iron', '4 Iron', '5 Iron', '6 Iron', '7 Iron', '8 Iron', '9 Iron',
  'Pitching Wedge', 'Approach Wedge', 'Gap Wedge', 'Sand Wedge', 'Lob Wedge', 'Putter'
];

const DEFAULT_BAG = [
  ['Driver', 230], ['3 Wood', 210], ['5 Wood', 195], ['4 Iron', 180],
  ['5 Iron', 170], ['6 Iron', 160], ['7 Iron', 150], ['8 Iron', 140],
  ['9 Iron', 130], ['Pitching Wedge', 115], ['Gap Wedge', 100],
  ['Sand Wedge', 85], ['Lob Wedge', 70], ['Putter', 0]
];

const WARM = [
  ['Glute Activator', '10 bodyweight squats, using a club for balance.'],
  ['Torso Twist', 'Club across shoulders, rotate smoothly for 60 seconds.'],
  ['Hip Opener', '10 forward/back and 10 side-to-side leg swings each side.'],
  ['Heavy Swing', 'Two wedges together, 5 slow continuous swings.'],
  ['Half-Wedge Drill', '5 hip-to-hip wedge shots, concentrating on contact.'],
  ['Ladder Climber', '2–3 balls each: Wedge → 8 Iron → 5 Iron/Hybrid → Driver.'],
  ['Fringe Roll', 'Two long putts to the fringe to learn today’s green speed.'],
  ['3-Foot Circle', 'Three short putts from about one putter length.']
];

const ROUTINE_DEFAULT = ['Target', 'Lie', 'Club', 'Picture', 'Commit', 'Breathe', 'Reset', 'Next'];
const STORAGE = 'CADDIEOS_WORLDCLASS_V1';

const n = v => Number(String(v ?? '').replace(/[^0-9.-]/g, '')) || 0;
const yd = (m, u) => u === 'METRES' ? Math.round(m) : Math.round(m * 1.09361);
const blankTargets = () => Array.from({ length: 18 }, () => ({ front: null, center: null, back: null }));
const blankResults = () => Array.from({ length: 18 }, () => ({ situation: '', advice: '', club: '', result: '' }));

function windAdj(w, u) {
  w = Math.abs(n(w));
  return u === 'METRES' ? (w / 1.609344) * .75 * .9144 : w * .75;
}

function playsLike(d, w, e, lie, dir, u) {
  let x = Math.max(0, n(d));
  x *= 1 + ({ 'Light Rough': .015, Rough: .04, 'Deep Rough': .07, 'Fairway Bunker': .045 }[lie] || 0);
  const a = windAdj(w, u);
  if (dir === 'HEAD') x += a;
  if (dir === 'TAIL') x -= a;
  x *= 1 + n(e) / 100;
  return Math.max(0, Math.round(x));
}

// Fixed data-unwrap crash: Map structural arrays appropriately 
function nearestClub(target, bag, u) {
  const validClubs = bag
    .filter(club => club[1] > 0)
    .map(club => ({ name: club[0], distance: yd(club[1], u) }));
    
  if (!validClubs.length) return ['—', 0];
  
  return validClubs.reduce((prev, curr) => 
    Math.abs(curr.distance - target) < Math.abs(prev.distance - target) ? curr : prev
  );
}

function advice(target, clubName, lie, w, dir, e, u) {
  const unit = u === 'METRES' ? 'metres' : 'yards';
  let t = `Playing ${target} ${unit}. ${clubName}.`;
  if (lie !== 'Tee' && lie !== 'Fairway') t += ` Allow for ${lie.toLowerCase()}.`;
  if (n(w)) {
    if (dir === 'HEAD') t += ` Headwind ${w}; flight it lower and allow more club.`;
    else if (dir === 'TAIL') t += ` Tailwind ${w}; expect extra carry.`;
    else t += ` Crosswind ${w}; start it into the wind.`;
  }
  if (n(e) > 0) t += ` Uphill ${Math.abs(n(e))}%.`;
  if (n(e) < 0) t += ` Downhill ${Math.abs(n(e))}%.`;
  return t + ' Pick the target, picture the shot and commit.';
}

function haversine(a, b, u) {
  if (!a || !b) return null;
  const r = x => x * Math.PI / 180, R = 6371000,
    dLat = r(b.lat - a.lat), dLon = r(b.lon - a.lon),
    la1 = r(a.lat), la2 = r(b.lat),
    h = Math.sin(dLat / 2) ** 2 + Math.cos(la1) * Math.cos(la2) * Math.sin(dLon / 2) ** 2,
    m = 2 * R * Math.asin(Math.min(1, Math.sqrt(h)));
  return Math.round(u === 'METRES' ? m : m * 1.09361);
}

// Fixed text selection crash
function parseSpeech(text, S) {
  const s = text.toLowerCase();
  const m = rx => { const a = s.match(rx); return a ? a[1] : null; };
  
  const d = m(/(?:to|target|distance|playing)\s+(\d{2,3})/) || m(/(\d{2,3})\s*(?:yards?|yds?|metres?|meters?)/);
  if (d) S.setDistance(d);
  
  const w = m(/(?:wind|headwind|tailwind)\s*(?:is|at)?\s*(\d{1,2})/) || m(/(\d{1,2})\s*(?:mph|kph|km\/h)/);
  if (w) S.setWind(w);
  
  if (/headwind|into the wind/.test(s)) S.setWindDir('HEAD');
  else if (/tailwind|helping wind/.test(s)) S.setWindDir('TAIL');
  else if (/left to right|left-to-right/.test(s)) S.setWindDir('L→R');
  else if (/right to left|right-to-left/.test(s)) S.setWindDir('R→L');
  
  const sl = m(/(?:slope|uphill|downhill)\s*(?:is|at)?\s*(\d{1,2})/);
  if (sl) S.setElev(/downhill/.test(s) ? `-${sl}` : sl);
  
  for (const l of [...LIES].reverse()) {
    if (s.includes(l.toLowerCase())) {
      S.setLie(l);
      break;
    }
  }
}

export default function App() {
  return (
    <SafeAreaProvider>
      <Shell />
    </SafeAreaProvider>
  );
}

function Shell() {
  const { height, width } = useWindowDimensions();
  const insets = useSafeAreaInsets();

  const [entered, setEntered] = useState(false);
  const [tab, setTab] = useState('CADDIE'); // Placed directly on Caddie view for easy voice debugging
  const [units, setUnits] = useState('METRES');
  const [player, setPlayer] = useState('Player');
  const [email, setEmail] = useState('');
  const [handicap, setHandicap] = useState('');
  const [bag, setBag] = useState(DEFAULT_BAG);
  const [course, setCourse] = useState('');
  const [tee, setTee] = useState('White');
  const [hole, setHole] = useState('1');
  const [targets, setTargets] = useState(blankTargets());
  const [gps, setGps] = useState(null);

  const [scores, setScores] = useState(Array(18).fill(''));
  const [putts, setPutts] = useState(Array(18).fill(''));
  const [gir, setGir] = useState(Array(18).fill(false));
  const [fw, setFw] = useState(Array(18).fill(false));
  const [pen, setPen] = useState(Array(18).fill(''));
  const [notes, setNotes] = useState(Array(18).fill(''));
  const [roundLog, setRoundLog] = useState(blankResults());

  const [distance, setDistance] = useState('150');
  const [wind, setWind] = useState('0');
  const [windDir, setWindDir] = useState('HEAD');
  const [elev, setElev] = useState('0');
  const [lie, setLie] = useState('Fairway');

  const [heard, setHeard] = useState('Tap the microphone and ask your caddie.');
  const [listening, setListening] = useState(false);

  const total = scores.reduce((a, b) => a + n(b), 0);
  const played = scores.filter(Boolean).length;
  const idx = Math.min(17, Math.max(0, n(hole) - 1));
  const toPar = scores.reduce((a, v, i) => a + (v ? n(v) - PARS[i] : 0), 0);

  const result = useMemo(() => {
    const adjustedYardage = playsLike(distance, wind, elev, lie, windDir, units);
    const matchedClub = nearestClub(adjustedYardage, bag, units);
    return { y: adjustedYardage, club: matchedClub.name };
  }, [distance, wind, elev, lie, windDir, units, bag]);

  const caddieText = useMemo(() => 
    advice(result.y, result.club, lie, wind, windDir, elev, units), 
    [result, lie, wind, windDir, elev, units]
  );

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const raw = await AsyncStorage.getItem(STORAGE);
        if (active && raw) {
          const x = JSON.parse(raw);
          if (x.units) setUnits(x.units);
          if (x.player) setPlayer(x.player);
          if (x.bag) setBag(x.bag);
          if (x.course) setCourse(x.course);
        }
      } catch {}
    })();

    Tts.setDefaultLanguage('en-AU').catch(() => {});

    Voice.onSpeechStart = () => setListening(true);
    Voice.onSpeechEnd = () => setListening(false);
    Voice.onSpeechError = () => setListening(false);
    Voice.onSpeechResults = (e) => {
      if (e.value && e.value.length > 0) {
        const spokenText = e.value[0];
        setHeard(spokenText);
        parseSpeech(spokenText, { setDistance, setWind, setWindDir, setElev, setLie });
      }
    };

    return () => {
      active = false;
      Voice.destroy().then(Voice.removeAllListeners).catch(() => {});
    };
  }, []);

  const toggleListening = async () => {
    if (listening) {
      try { await Voice.stop(); } catch {}
    } else {
      try {
        setHeard('Listening...');
        await Voice.start('en-AU');
      } catch {
        setListening(false);
      }
    }
  };

  const speakAdvice = () => {
    Tts.stop();
    Tts.speak(caddieText);
  };

  return (
    <SafeAreaView style={[styles.container, { paddingTop: insets.top }]}>
      <StatusBar barStyle="light-content" backgroundColor={C.bg} />
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.title}>CADDIE<Text style={{ color: C.gold }}>OS</Text></Text>

        <View style={styles.panel}>
          <Text style={styles.label}>HOLE {hole} — PAR {PARS[idx]}</Text>
          <Text style={styles.largeText}>Plays Like: {result.y} {units.toLowerCase()}</Text>
