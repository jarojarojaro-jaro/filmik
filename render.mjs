// node render.mjs            -> genesis.mp4 (1080p60 + audio.wav)
// node render.mjs 0.5 3 6.5  -> preview stills in shots/
import {chromium} from '/opt/node22/lib/node_modules/playwright/index.mjs';
import {spawn} from 'child_process';
import {mkdirSync} from 'fs';
const ts=process.argv.slice(2).map(Number),[W,H]=ts.length?[960,540]:[1920,1080],FPS=60,D=7;
const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:W,height:H}});
p.on('pageerror',e=>{console.error(e);process.exit(1)});
await p.goto(new URL('index.html',import.meta.url).href);
const shot=async t=>(await p.evaluate(t=>draw(t),t),p.screenshot({type:'png'}));
if(ts.length){mkdirSync('shots',{recursive:true});for(const t of ts){await p.evaluate(t=>draw(t),t);await p.screenshot({path:`shots/${t}.png`})}}
else{
 const f=spawn(process.env.FFMPEG||'ffmpeg',['-y','-loglevel','error','-framerate',`${FPS}`,'-f','image2pipe','-i','-','-i','audio.wav',
  '-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart','genesis.mp4'],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<FPS*D;i++){if(!f.stdin.write(await shot(i/FPS)))await new Promise(r=>f.stdin.once('drain',r));if(i%30==0)console.log(i)}
 f.stdin.end();await new Promise(r=>f.on('close',r));
}
await b.close();
