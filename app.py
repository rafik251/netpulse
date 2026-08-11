from flask import Flask, render_template_string, jsonify, request, Response
import requests
import time
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>NETPULSE — Internet Speed Test</title>

<style>
*{
    box-sizing:border-box;
}

body{
    margin:0;
    min-height:100vh;
    font-family:Arial,Helvetica,sans-serif;
    color:white;
    background:
        radial-gradient(circle at 50% 0%,#12365b 0%,#07111f 35%,#02050a 75%);
    overflow-x:hidden;
}

.container{
    width:100%;
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
    font-size:14px;
    letter-spacing:3px;
    text-transform:uppercase;
}

.logo{
    margin-top:8px;
    font-size:42px;
    font-weight:900;
    color:#38bdf8;
    text-shadow:
        0 0 10px #38bdf8,
        0 0 35px rgba(56,189,248,.55);
}

.subtitle{
    color:#64748b;
    margin-top:7px;
    letter-spacing:1px;
}

.card{
    background:rgba(8,17,32,.86);
    border:1px solid rgba(148,163,184,.12);
    border-radius:25px;
    padding:22px;
    margin-bottom:17px;
    box-shadow:
        0 20px 70px rgba(0,0,0,.45),
        inset 0 1px rgba(255,255,255,.03);
    backdrop-filter:blur(15px);
}

.card h3{
    margin-top:0;
}

.info{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}

.infoBox{
    padding:13px;
    border-radius:15px;
    background:#07101d;
    border:1px solid rgba(255,255,255,.05);
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
    color:#e2e8f0;
    word-break:break-word;
}

.start{
    position:relative;
    overflow:hidden;
    width:100%;
    margin-top:20px;
    padding:18px;
    border:0;
    border-radius:55px;
    color:white;
    font-size:19px;
    font-weight:900;
    letter-spacing:1px;
    cursor:pointer;

    background:linear-gradient(
        90deg,
        #06b6d4,
        #6366f1,
        #a855f7,
        #06b6d4
    );
    background-size:300% 100%;

    box-shadow:
        0 0 20px rgba(6,182,212,.35),
        0 0 50px rgba(99,102,241,.2);

    animation:gradient 5s linear infinite;
    transition:.25s;
}

.start:hover{
    transform:translateY(-3px) scale(1.01);
    box-shadow:
        0 0 30px rgba(56,189,248,.7),
        0 0 70px rgba(99,102,241,.35);
}

.start:active{
    transform:scale(.97);
}

.start:disabled{
    opacity:.55;
    cursor:not-allowed;
    animation:none;
}

@keyframes gradient{
    0%{background-position:0%}
    100%{background-position:300%}
}

.rocket{
    font-size:75px;
    text-align:center;
    margin:15px 0;
    filter:drop-shadow(0 0 15px #38bdf8);
}

.rocket.running{
    animation:rocket 1s infinite ease-in-out;
}

@keyframes rocket{
    0%,100%{
        transform:translateY(0) rotate(-4deg);
    }
    50%{
        transform:translateY(-18px) rotate(4deg);
    }
}

.flame{
    display:none;
    text-align:center;
    color:#38bdf8;
    font-size:20px;
    letter-spacing:6px;
    animation:flame .25s infinite alternate;
}

.running + .flame{
    display:block;
}

@keyframes flame{
    from{opacity:.4;transform:scaleX(.8)}
    to{opacity:1;transform:scaleX(1.2)}
}

.gauge{
    text-align:center;
    padding:10px 0 20px;
}

.speed{
    font-family:monospace;
    font-size:64px;
    font-weight:900;
    color:#38bdf8;
    text-shadow:0 0 25px rgba(56,189,248,.4);
}

.unit{
    color:#94a3b8;
    font-size:14px;
}

.results{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
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
    border:1px solid rgba(255,255,255,.05);
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
    margin:20px 0;
    text-align:center;
    font-size:42px;
    font-weight:900;
    color:#22c55e;
    text-shadow:0 0 20px rgba(34,197,94,.3);
}

.service{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:14px;
    margin-top:8px;
    border-radius:14px;
    background:#07101d;
    border:1px solid rgba(255,255,255,.04);
}

.good{
    color:#22c55e;
}

.medium{
    color:#facc15;
}

.bad{
    color:#ef4444;
}

.advice{
    margin-top:16px;
    padding:16px;
    border-radius:16px;
    line-height:1.7;
    color:#cbd5e1;
    background:rgba(56,189,248,.07);
    border:1px solid rgba(56,189,248,.14);
}

.status{
    text-align:center;
    margin-top:14px;
    color:#94a3b8;
}

.hidden{
    display:none;
}

@media(max-width:550px){

    .info{
        grid-template-columns:1fr;
    }

    .results{
        grid-template-columns:1fr;
    }

    .advanced{
        grid-template-columns:1fr 1fr;
    }

    .speed{
        font-size:48px;
    }

    .logo{
        font-size:34px;
    }
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

<div class="rocket" id="rocket">🚀</div>
<div class="flame">• • • • •</div>

<div class="gauge">
<div class="speed" id="liveSpeed">0.0</div>
<div class="unit" id="speedType">Mbps</div>
</div>

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

<div class="score" id="score">
--/100
</div>

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
<span>📥 Large File Downloads</span>
<strong id="files">--</strong>
</div>

<div class="advice" id="advice">
💡 Smart Advisor will appear here after the test.
</div>

</div>

</div>

<script>

async function loadIP(){

    try{

        const res = await fetch(
            "https://ipapi.co/json/",
            {cache:"no-store"}
        );

        const data = await res.json();

        document.getElementById("ip").innerText =
            data.ip || "Unknown";

        document.getElementById("country").innerText =
            (data.country_code ? getFlag(data.country_code) + " " : "") +
            (data.country_name || "Unknown");

        document.getElementById("city").innerText =
            data.city || "Unknown";

        document.getElementById("isp").innerText =
            data.org || "Unknown";

    }catch(e){

        document.getElementById("ip").innerText="Unavailable";
        document.getElementById("country").innerText="Unknown";
        document.getElementById("city").innerText="Unknown";
        document.getElementById("isp").innerText="Unknown";
    }
}

function getFlag(code){

    if(!code || code.length !== 2)
        return "🌍";

    return String.fromCodePoint(
        ...[...code.toUpperCase()].map(
            c => 127397 + c.charCodeAt()
        )
    );
}

async function pingTest(){

    let values=[];
    let lost=0;
    const total=10;

    for(let i=0;i<total;i++){

        const controller=new AbortController();

        const timeout=setTimeout(
            ()=>controller.abort(),
            2000
        );

        const start=performance.now();

        try{

            await fetch(
                "/ping?x="+Math.random(),
                {
                    cache:"no-store",
                    signal:controller.signal
                }
            );

            const end=performance.now();

            clearTimeout(timeout);

            values.push(end-start);

        }catch(e){

            lost++;
        }

        await new Promise(
            r=>setTimeout(r,70)
        );
    }

    if(values.length===0){

        return {
            ping:999,
            jitter:0,
            packetLoss:100
        };
    }

    values.sort((a,b)=>a-b);

    let jitter=0;

    for(let i=1;i<values.length;i++){

        jitter += Math.abs(
            values[i]-values[i-1]
        );
    }

    jitter =
        values.length>1
        ? jitter/(values.length-1)
        : 0;

    return {

        ping:Math.round(values[0]),

        jitter:Math.round(jitter),

        packetLoss:
            Number(
                ((lost/total)*100).toFixed(1)
            )
    };
}

async function downloadTest(){

    const live=
        document.getElementById("liveSpeed");

    const duration=6000;

    const start=performance.now();

    let bytes=0;

    while(
        performance.now()-start < duration
    ){

        const res=await fetch(
            "/download?x="+Math.random(),
            {cache:"no-store"}
        );

        const blob=await res.blob();

        bytes += blob.size;

        const elapsed=
            (performance.now()-start)/1000;

        const speed=
            bytes*8/
            elapsed/
            1000000;

        live.innerText=
            speed.toFixed(1);
    }

    const elapsed=
        (performance.now()-start)/1000;

    return bytes*8/
        elapsed/
        1000000;
}

async function uploadTest(){

    const live=
        document.getElementById("liveSpeed");

    const duration=5000;

    const start=performance.now();

    let bytes=0;

    const size=512*1024;

    const payload=
        new Uint8Array(size);

    while(
        performance.now()-start < duration
    ){

        await fetch(
            "/upload?x="+Math.random(),
            {
                method:"POST",
                body:payload
            }
        );

        bytes += size;

        const elapsed=
            (performance.now()-start)/1000;

        const speed=
            bytes*8/
            elapsed/
            1000000;

        live.innerText=
            speed.toFixed(1);
    }

    const elapsed=
        (performance.now()-start)/1000;

    return bytes*8/
        elapsed/
        1000000;
}

function scoreTest(
    download,
    upload,
    ping,
    jitter,
    loss
){

    let score=100;

    if(download<10)
        score-=25;
    else if(download<30)
        score-=15;
    else if(download<50)
        score-=5;

    if(upload<5)
        score-=15;
    else if(upload<15)
        score-=8;

    if(ping>100)
        score-=25;
    else if(ping>50)
        score-=12;

    if(jitter>20)
        score-=15;

    score -= loss*3;

    return Math.max(
        0,
        Math.round(score)
    );
}

function setResult(
    id,
    text,
    type
){

    const el=
        document.getElementById(id);

    el.innerText=text;

    el.className=type;
}

function analyze(
    download,
    upload,
    ping,
    jitter,
    loss
){

    if(
        ping<=40 &&
        jitter<=10 &&
        loss===0
    ){

        setResult(
            "gaming",
            "🟢 Excellent",
            "good"
        );

    }else if(
        ping<=70 &&
        loss<5
    ){

        setResult(
            "gaming",
            "🟡 Good",
            "medium"
        );

    }else{

        setResult(
            "gaming",
            "🔴 Poor",
            "bad"
        );
    }

    if(download>=25){

        setResult(
            "video",
            "🟢 Excellent — 4K UHD",
            "good"
        );

    }else if(download>=12){

        setResult(
            "video",
            "🟡 Good — Full HD",
            "medium"
        );

    }else{

        setResult(
            "video",
            "🔴 Poor",
            "bad"
        );
    }

    if(upload>=10 && jitter<15){

        setResult(
            "stream",
            "🟢 Excellent — 1080p",
            "good"
        );

    }else if(upload>=5){

        setResult(
            "stream",
            "🟡 Moderate — 720p",
            "medium"
        );

    }else{

        setResult(
            "stream",
            "🔴 Poor",
            "bad"
        );
    }

    if(ping<=100 && loss<2){

        setResult(
            "calls",
            "🟢 Excellent",
            "good"
        );

    }else{

        setResult(
            "calls",
            "🟡 Fair",
            "medium"
        );
    }

    if(download>=50){

        setResult(
            "files",
            "🟢 Very Fast",
            "good"
        );

    }else if(download>=20){

        setResult(
            "files",
            "🟡 Fast",
            "medium"
        );

    }else{

        setResult(
            "files",
            "🔴 Slow",
            "bad"
        );
    }

    let advice="";

    if(loss>2){

        advice=
        "High packet loss detected. Check your Wi-Fi signal, router or network cable.";

    }else if(jitter>20){

        advice=
        "Your connection has high jitter. This can cause unstable gaming and calls.";

    }else if(ping>80){

        advice=
        "Your ping is relatively high. This may affect competitive online gaming.";

    }else if(download<15){

        advice=
        "Your download speed is relatively low for heavy downloads and 4K streaming.";

    }else{

        advice=
        "Your connection is fast and stable for gaming, streaming and everyday use.";
    }

    document.getElementById("advice").innerText=
        "💡 Smart Advisor: "+advice;
}

async function startTest(){

    const button=
        document.getElementById("start");

    const status=
        document.getElementById("status");

    const results=
        document.getElementById("results");

    const rocket=
        document.getElementById("rocket");

    const speedType=
        document.getElementById("speedType");

    button.disabled=true;

    results.classList.remove("hidden");

    rocket.classList.add("running");

    document.getElementById("liveSpeed").innerText="0.0";

    document.getElementById("download").innerText="--";
    document.getElementById("upload").innerText="--";
    document.getElementById("ping").innerText="--";
    document.getElementById("jitter").innerText="--";
    document.getElementById("packetLoss").innerText="--";

    status.innerText=
        "🌐 Testing connection quality...";

    const quality=
        await pingTest();

    document.getElementById("ping").innerText=
        quality.ping;

    document.getElementById("jitter").innerText=
        quality.jitter;

    document.getElementById("packetLoss").innerText=
        quality.packetLoss;

    status.innerText=
        "⬇️ Measuring download speed...";

    speedType.innerText=
        "Mbps — DOWNLOAD";

    const download=
        await downloadTest();

    document.getElementById("download").innerText=
        download.toFixed(2);

    status.innerText=
        "⬆️ Measuring upload speed...";

    speedType.innerText=
        "Mbps — UPLOAD";

    const upload=
        await uploadTest();

    document.getElementById("upload").innerText=
        upload.toFixed(2);

    speedType.innerText="Mbps";

    document.getElementById("liveSpeed").innerText=
        download.toFixed(1);

    const score=
        scoreTest(
            download,
            upload,
            quality.ping,
            quality.jitter,
            quality.packetLoss
        );

    document.getElementById("score").innerText=
        score+"/100";

    analyze(
        download,
        upload,
        quality.ping,
        quality.jitter,
        quality.packetLoss
    );

    rocket.classList.remove("running");

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


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/ping")
def ping():
    return jsonify({
        "ok": True,
        "time": time.time()
    })


@app.route("/download")
def download():

    data=os.urandom(
        2*1024*1024
    )

    return Response(
        data,
        mimetype="application/octet-stream",
        headers={
            "Cache-Control":
                "no-store, no-cache, must-revalidate",
            "Content-Length":
                str(len(data))
        }
    )


@app.route("/upload", methods=["POST"])
def upload():

    request.get_data()

    return jsonify({
        "ok":True
    })


if __name__=="__main__":

    print()
    print("⚡ NETPULSE v2 ENGINE ONLINE")
    print("==========================================")
    print("🌐 Local: http://127.0.0.1:5000")
    print("==========================================")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
