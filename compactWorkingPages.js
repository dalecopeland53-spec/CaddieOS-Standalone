import {StyleSheet} from 'react-native';

// Compact only the working screens. Home/login/header/bottom navigation stay untouched.
const originalCreate=StyleSheet.create.bind(StyleSheet);
const compactKeys=new Set([
  'pageHead','pageTitle','pill','card','sectionLabelTop','sectionLabel','input','note','helper',
  'mapCard','mapVisual','distanceStrip','distanceMini','roundMetrics','roundMetric','metricBig','recommend','recommendClub',
  'goldButton','goldOutline','micHero','micRing','micSymbol','micHeroTitle','micHeroSub','heardBox','heardText','answerBox','answerText',
  'quickGrid','quickCard','quickValue','quickValueSmall','fieldInner','fieldInput','chip','chipRow',
  'bagPanel','bagRow','bagStep','bagStepText','bagDist','holeGrid','holeBtn','markRow','markBtn',
  'menuPanel','menuRow','menuInfo','scoreBoard','scoreHeader','scoreLine','scoreTotalLine','scoreInput','scoreFooter',
  'practiceDistance','practiceStep','practiceStepText','practiceBig','checkRow','checkBox','checkText',
  'summaryHero','summaryScore','summaryRow','courseBanner','facilityRow'
]);
const verticalProps=new Set(['height','minHeight','maxHeight','padding','paddingTop','paddingBottom','paddingVertical','margin','marginTop','marginBottom','marginVertical','rowGap','gap']);
const textProps=new Set(['fontSize','lineHeight']);

StyleSheet.create=(styles)=>{
  const next={...styles};
  for(const key of compactKeys){
    const src=next[key];
    if(!src||typeof src!=='object')continue;
    const out={...src};
    for(const prop of Object.keys(out)){
      const value=out[prop];
      if(typeof value!=='number')continue;
      if(verticalProps.has(prop))out[prop]=Math.max(prop==='gap'||prop==='rowGap'?3:1,Math.round(value*0.78));
      else if(textProps.has(prop))out[prop]=Math.max(8,Math.round(value*0.90));
    }
    next[key]=out;
  }
  return originalCreate(next);
};
