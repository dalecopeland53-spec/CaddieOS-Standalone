const http=require('http');
const PORT=process.env.PORT||8080;
const bag=[['Driver',230],['3W',210],['5W',195],['4i',180],['5i',170],['6i',160],['7i',150],['8i',140],['9i',130],['PW',115],['GW',100],['SW',85],['LW',70]];
function solve(x){let d=Number(x.distance_yards)||0;const liePct={rough:.04,'deep rough':.07,'fairway bunker':.045}[String(x.lie||'').toLowerCase()]||0;d*=1+liePct;d+=(Number(x.wind_mph)||0)*.75;d*=1+(Number(x.elevation_pct)||0)/100;d=Math.max(0,Math.round(d));const club=bag.reduce((a,c)=>Math.abs(c[1]-d)<Math.abs(a[1]-d)?c:a,bag[0]);return {plays_like_yards:d,recommended_club:club[0],stock_carry_yards:club[1]}}
const server=http.createServer((req,res)=>{res.setHeader('Content-Type','application/json');if(req.url==='/health')return res.end(JSON.stringify({ok:true,service:'caddieos-api'}));if(req.url==='/v1/solve'&&req.method==='POST'){let b='';req.on('data',c=>b+=c);req.on('end',()=>{try{res.end(JSON.stringify(solve(JSON.parse(b||'{}'))))}catch(e){res.statusCode=400;res.end(JSON.stringify({error:'invalid_json'}))}});return;}res.statusCode=404;res.end(JSON.stringify({error:'not_found'}))});
server.listen(PORT,()=>console.log(`CaddieOS API on ${PORT}`));
