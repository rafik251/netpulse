from flask import Flask, render_template_string, jsonify, request
import requests
import time

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head><meta name="google-site-verification" content="Vbct_9UjwRQFwXfyKxhGdIt6UfqLD50XKrEjfN65wdo">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NETPULSE</title>

<style>
*{box-sizing:border-box}

body{
margin:0;
min-height:100vh;
font-family:Arial,sans-serif;
color:#fff;
background:
radial-gradient(circle at 50% 0%,#12365b,#07111f 40%,#02050a 80%);
}

.container{
max-width:760px;
margin:auto;
padding:25px 15px 45px;
}

.header{
text-align:center;
margin-bottom:22px;
}

.welcome{
color:#94a3b8;
font-size:13px;
letter-spacing:3px;
}

.logo{
margin-top:8px;
font-size:42px;
font-weight:900;
color:#38bdf8;
text-shadow:0 0 12px #38bdf8,0 0 35px #38bdf855;
}

.subtitle{
color:#64748b;
margin-top:7px;
}

.card{
background:#081120ee;
border:1px solid #ffffff12;
border-radius:25px;
padding:22px;
margin-bottom:17px;
box-shadow:0 20px 70px #00000073;
}

.info{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
}

.infoBox{
padding:14px;
border-radius:15px;
background:#07101d;
}

.label{
color:#64748b;
font-size:10px;
text-transform:uppercase;
letter-spacing:1px;
}

.value{
margin-top:6px;
font-weight:bold;
word-break:break-word;
}

.start{
width:100%;
margin-top:20px;
padding:18px;
border:0;
border-radius:55px;
color:#fff;
font-size:18px;
font-weight:900;
cursor:pointer;
background:linear-gradient(90deg,#06b6d4,#6366f1,#a855f7);
box-shadow:0 0 25px #06b6d440;
}

.start:disabled{
opacity:.5;
}

.status{
text-align:center;
margin-top:14px;
color:#94a3b8;
}

.hidden{
display:none;
}

.rocket{
font-size:70px;
text-align:center;
margin:10px;
}

.speed{
text-align:center;
font-family:monospace;
font-size:58px;
font-weight:900;
color:#38bdf8;
text-shadow:0 0 25px #38bdf866;
}

.unit{
text-align:center;
color:#94a3b8;
}

.results{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:10px;
margin-top:20px;
}

.advanced{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
margin-top:10px;
}

.result{
background:#07101d;
border-radius:16px;
padding:15px 8px;
text-align:center;
}

.number{
color:#38bdf8;
font-family:monospace;
font-size:22px;
font-weight:bold;
}

.result small{
display:block;
color:#64748b;
margin-top:6px;
font-size:10px;
}

.score{
margin:25px 0;
text-align:center;
font-size:42px;
font-weight:900;
color:#22c55e;
}

.service{
display:flex;
justify-content:space-between;
padding:14px;
margin-top:8px;
border-radius:14px;
background:#07101d;
}

.good{color:#22c55e}
.medium{color:#facc15}
.bad{color:#ef4444}

.advice{
margin-top:16px;
padding:16px;
border-radius:16px;
line-height:1.7;
color:#cbd5e1;
background:#38bdf812;
}

@media(max-width:550px){
.info{grid-template-columns:1fr}
.results{grid-template-columns:1fr}
.speed{font-size:48px}
.logo{font-size:34px}
}
</style>
</head>

<body>

<div class="container">

<div class="header">
<div class="welcome">WELCOME TO</div>
<div class="logo">⚡ NETPULSE</div>
<div class="subtitle">SMART INTERNET PERFORMANCE TEST</div>
</div>

<div class="card">

<h3>🌍 YOUR CONNECTION</h3>

<div class="info">

<div class="infoBox">
<div class="label">IP ADDRESS</div>
<div class="value" id="ip">Detecting...</div>
</div>

<div class="infoBox">
<div class="label">COUNTRY</div>
<div class="value" id="country">Detecting...</div>
</div>

<div class="infoBox">
<div class="label">CITY</div>
<div class="value" id="city">Detecting...</div>
</div>

<div class="infoBox">
<div class="label">ISP</div>
<div class="value" id="isp">Detecting...</div>
</div>

</div>

<button class="start" id="start" onclick="startTest()">
🚀 START SPEED TEST
</button>

<div class="status" id="status">
Ready to test your connection
</div>

</div>

<div class="card hidden" id="results">

<div class="rocket">🚀</div>

<div class="speed" id="liveSpeed">0.0</div>
<div class="unit">Mbps</div>

<div class="results">

<div class="result">
<div class="number" id="download">--</div>
<small>📥 DOWNLOAD Mbps</small>
</div>

<div class="result">
<div class="number" id="upload">--</div>
<small>📤 UPLOAD Mbps</small>
</div>

<div class="result">
<div class="number" id="ping">--</div>
<small>🌐 PING ms</small>
</div>

</div>

<div class="advanced">

<div class="result">
<div class="number" id="jitter">--</div>
<small>📊 JITTER ms</small>
</div>

<div class="result">
<div class="number" id="packetLoss">--</div>
<small>⚠️ PACKET LOSS %</small>
</div>

</div>

<div class="score" id="score">--/100</div>

<h3>📊 CONNECTION QUALITY</h3>

<div class="service">
<span>🎮 Competitive Gaming</span>
<strong id="gaming">--</strong>
</div>

<div class="service">
<span>🎬 4K Ultra HD</span>
<strong id="video">--</strong>
</div>

<div class="service">
<span>📡 Live Streaming</span>
<strong id="stream">--</strong>
</div>

<div class="service">
<span>📞 Video Calls</span>
<strong id="calls">--</strong>
</div>

<div class="service">
<span>📥 Large Downloads</span>
<strong id="files">--</strong>
</div>

<div class="advice" id="advice">
💡 Smart Advisor
</div>

</div>

</div>

<script>

const CF =
"https://speed.cloudflare.com";

async function loadIP(){

try{

const r=await fetch(
"https://api64.ipify.org?format=json",
{cache:"no-store"}
);

const data=await r.json();

const ip=data.ip;

document.getElementById("ip").innerText=ip;

const geo=await fetch(
"/lookup-ip?ip="+encodeURIComponent(ip)
);

const info=await geo.json();

document.getElementById("country").innerText=
(info.flag||"")+" "+(info.country||"Unknown");

document.getElementById("city").innerText=
info.city||"Unknown";

document.getElementById("isp").innerText=
info.isp||"Unknown";

}catch(e){

document.getElementById("ip").innerText="Unavailable";
document.getElementById("country").innerText="Unknown";
document.getElementById("city").innerText="Unknown";
document.getElementById("isp").innerText="Unknown";

}

}


async function pingTest(){

let values=[];
let lost=0;

for(let i=0;i<12;i++){

const start=performance.now();

try{

await fetch(
CF+"/cdn-cgi/trace?x="+Math.random(),
{
cache:"no-store",
mode:"cors"
}
);

values.push(
performance.now()-start
);

}catch(e){

lost++;

}

await new Promise(
r=>setTimeout(r,80)
);

}

if(values.length===0){

return{
ping:999,
jitter:0,
loss:100
};

}

values.sort((a,b)=>a-b);

let jitter=0;

for(let i=1;i<values.length;i++){

jitter+=Math.abs(
values[i]-values[i-1]
);

}

if(values.length>1){

jitter/=values.length-1;

}

return{
ping:Math.round(values[0]),
jitter:Math.round(jitter),
loss:Number(
((lost/12)*100).toFixed(1)
)
};

}


async function downloadTest(){

const start=performance.now();

let bytes=0;

const duration=10000;

while(
performance.now()-start<duration
){

const r=await fetch(
CF+"/__down?bytes=10000000&x="+Math.random(),
{
cache:"no-store"
}
);

const buffer=await r.arrayBuffer();

bytes+=buffer.byteLength;

const elapsed=
(performance.now()-start)/1000;

const speed=
bytes*8/elapsed/1000000;

document.getElementById(
"liveSpeed"
).innerText=
speed.toFixed(1);

}

const elapsed=
(performance.now()-start)/1000;

return bytes*8/elapsed/1000000;

}


async function uploadTest(){

const data=
new Uint8Array(1000000);

const start=performance.now();

let bytes=0;

const duration=8000;

while(
performance.now()-start<duration
){

await fetch(
CF+"/__up",
{
method:"POST",
body:data
}
);

bytes+=data.length;

const elapsed=
(performance.now()-start)/1000;

const speed=
bytes*8/elapsed/1000000;

document.getElementById(
"liveSpeed"
).innerText=
speed.toFixed(1);

}

const elapsed=
(performance.now()-start)/1000;

return bytes*8/elapsed/1000000;

}


function scoreTest(d,u,p,j,l){

let s=100;

if(d<10)s-=25;
else if(d<30)s-=15;
else if(d<50)s-=5;

if(u<5)s-=15;
else if(u<15)s-=8;

if(p>100)s-=25;
else if(p>50)s-=12;

if(j>20)s-=15;

s-=l*3;

return Math.max(0,Math.round(s));

}


function quality(id,text,cls){

const e=document.getElementById(id);

e.innerText=text;
e.className=cls;

}


function analyze(d,u,p,j,l){

if(p<=40&&j<=10&&l===0){

quality("gaming","🟢 Excellent","good");

}else if(p<=70&&l<5){

quality("gaming","🟡 Good","medium");

}else{

quality("gaming","🔴 Poor","bad");

}


if(d>=25){

quality(
"video",
"🟢 Excellent — 4K UHD",
"good"
);

}else if(d>=12){

quality(
"video",
"🟡 Good — Full HD",
"medium"
);

}else{

quality(
"video",
"🔴 Poor",
"bad"
);

}


if(u>=10&&j<15){

quality(
"stream",
"🟢 Excellent",
"good"
);

}else if(u>=5){

quality(
"stream",
"🟡 Moderate",
"medium"
);

}else{

quality(
"stream",
"🔴 Poor",
"bad"
);

}


if(p<=100&&l<2){

quality(
"calls",
"🟢 Excellent",
"good"
);

}else{

quality(
"calls",
"🟡 Fair",
"medium"
);

}


if(d>=50){

quality(
"files",
"🟢 Very Fast",
"good"
);

}else if(d>=20){

quality(
"files",
"🟡 Fast",
"medium"
);

}else{

quality(
"files",
"🔴 Slow",
"bad"
);

}


let message;

if(l>2){

message=
"High packet loss detected.";

}else if(j>20){

message=
"High jitter detected.";

}else if(p>80){

message=
"Ping is relatively high.";

}else if(d<15){

message=
"Download speed is relatively low.";

}else{

message=
"Your connection is fast and stable.";

}

document.getElementById(
"advice"
).innerText=
"💡 Smart Advisor: "+message;

}


async function startTest(){

const button=
document.getElementById("start");

const status=
document.getElementById("status");

document.getElementById(
"results"
).classList.remove("hidden");

button.disabled=true;

status.innerText=
"🌐 Measuring latency...";

const q=await pingTest();

document.getElementById("ping").innerText=q.ping;
document.getElementById("jitter").innerText=q.jitter;
document.getElementById("packetLoss").innerText=q.loss;

status.innerText=
"⬇️ Measuring real download speed...";

const d=await downloadTest();

document.getElementById("download").innerText=
d.toFixed(2);

status.innerText=
"⬆️ Measuring real upload speed...";

const u=await uploadTest();

document.getElementById("upload").innerText=
u.toFixed(2);

const score=
scoreTest(
d,u,q.ping,q.jitter,q.loss
);

document.getElementById("score").innerText=
score+"/100";

analyze(
d,u,q.ping,q.jitter,q.loss
);

status.innerText=
"✅ TEST COMPLETE";

button.disabled=false;

button.innerText=
"🔄 TEST AGAIN";

}

loadIP();

</script>

</body>
</html>
"""


def home():
    return render_template_string(HTML)@app.route("/robots.txt")
def robots():
    return """User-agent: *
Allow: /

Sitemap: https://netpulse-llgc.onrender.com/sitemap.xml
"""@app.route("/sitemap.xml")
def sitemap():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://netpulse-llgc.onrender.com/</loc>
    </url>
</urlset>
"""@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/lookup-ip")
def lookup_ip():

    ip=request.args.get("ip","").strip()

    if not ip:

        return jsonify({
            "country":"Unknown",
            "city":"Unknown",
            "isp":"Unknown",
            "flag":""
        })

    try:

        r=requests.get(
            "https://ipwho.is/"+ip,
            timeout=10,
            headers={
                "User-Agent":"NETPULSE"
            }
        )

        data=r.json()

        code=(
            data.get("country_code") or ""
        ).upper()

        flag=""

        if len(code)==2:

            flag="".join(
                chr(127397+ord(c))
                for c in code
            )

        connection=(
            data.get("connection") or {}
        )

        return jsonify({

            "country":
                data.get("country") or "Unknown",

            "city":
                data.get("city") or "Unknown",

            "isp":
                connection.get("isp") or "Unknown",

            "flag":flag
        })

    except Exception as e:

        print("IP lookup error:",e)

        return jsonify({
            "country":"Unknown",
            "city":"Unknown",
            "isp":"Unknown",
            "flag":""
        })


if __name__=="__main__":

    print()
    print("⚡ NETPULSE FINAL VERSION")
    print("🌐 http://127.0.0.1:5000")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
