from flask import Flask, render_template_string, jsonify, request, Response
import requests
import time
import os
import random

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NETPULSE — Smart Internet Speed Test</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    min-height:100vh;
    font-family:Arial,Helvetica,sans-serif;
    color:#fff;
    background:
      radial-gradient(circle at 50% 10%,#123b63 0%,#071321 35%,#03060b 75%);
    display:flex;
    justify-content:center;
    overflow-x:hidden;
}

body.testing{
    background:
      radial-gradient(circle at 50% 35%,#123e61 0%,#061522 35%,#020409 75%);
}

.container{
    width:100%;
    max-width:720px;
    padding:24px 15px 40px;
}

.header{
    text-align:center;
    margin-bottom:18px;
}

.logo{
    font-size:38px;
    font-weight:900;
    letter-spacing:2px;
    color:#38bdf8;
    text-shadow:
      0 0 10px #38bdf8,
      0 0 30px rgba(56,189,248,.5);
}

.welcome{
    margin-top:7px;
    color:#cbd5e1;
    font-size:14px;
    letter-spacing:1px;
}

.card{
    background:rgba(9,18,32,.88);
    border:1px solid rgba(255,255,255,.08);
    border-radius:24px;
    padding:20px;
    margin-bottom:15px;
    box-shadow:0 15px 50px rgba(0,0,0,.45);
    backdrop-filter:blur(12px);
}

.connection-title{
    text-align:center;
    color:#e2e8f0;
    margin-top:0;
}

.info{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}

.infoBox{
    background:#07101d;
    border:1px solid rgba(255,255,255,.06);
    border-radius:14px;
    padding:12px;
}

.label{
    color:#64748b;
    font-size:10px;
    text-transform:uppercase;
}

.value{
    margin-top:6px;
    color:#f8fafc;
    font-size:14px;
    font-weight:bold;
    word-break:break-word;
}

/* SPEED AREA */

.speedArea{
    position:relative;
    height:270px;
    display:flex;
    justify-content:center;
    align-items:center;
    margin:5px 0;
}

.ring{
    position:absolute;
    width:225px;
    height:225px;
    border-radius:50%;
    border:7px solid #13263a;
    border-top-color:#38bdf8;
    border-right-color:#6366f1;
    box-shadow:
      0 0 20px rgba(56,189,248,.15),
      inset 0 0 20px rgba(56,189,248,.05);
}

.testing .ring{
    animation:spin 1s linear infinite;
    box-shadow:
      0 0 25px #38bdf8,
      0 0 70px rgba(99,102,241,.35);
}

@keyframes spin{
    to{transform:rotate(360deg)}
}

.speedCenter{
    position:relative;
    z-index:2;
    text-align:center;
}

.liveSpeed{
    font-size:50px;
    font-weight:900;
    color:#fff;
    font-family:monospace;
    text-shadow:0 0 20px rgba(56,189,248,.5);
}

.speedUnit{
    color:#38bdf8;
    font-size:14px;
}

/* ROCKET */

.rocket{
    position:absolute;
    z-index:3;
    font-size:48px;
    bottom:15px;
    opacity:.15;
    filter:drop-shadow(0 0 10px #38bdf8);
}

.testing .rocket{
    opacity:1;
    animation:rocketFly 1.8s ease-in-out infinite;
}

@keyframes rocketFly{
    0%{
        transform:translateY(30px) scale(.85);
    }
    50%{
        transform:translateY(-65px) scale(1.05);
    }
    100%{
        transform:translateY(30px) scale(.85);
    }
}

/* START BUTTON */

.start{
    position:relative;
    overflow:hidden;
    width:100%;
    border:0;
    border-radius:55px;
    padding:18px;
    font-size:19px;
    font-weight:900;
    color:#fff;
    cursor:pointer;
    background:linear-gradient(135deg,#06b6d4,#6366f1,#8b5cf6);
    background-size:200% 200%;
    box-shadow:
      0 0 20px rgba(56,189,248,.35),
      0 8px 25px rgba(0,0,0,.35);
    transition:.3s;
}

.start:hover{
    transform:translateY(-2px) scale(1.01);
    background-position:100% 50%;
    box-shadow:
      0 0 35px rgba(56,189,248,.65),
      0 10px 30px rgba(0,0,0,.4);
}

.start:active{
    transform:scale(.97);
}

.start:disabled{
    opacity:.65;
    cursor:not-allowed;
}

.start::after{
    content:"";
    position:absolute;
    top:0;
    left:-100%;
    width:50%;
    height:100%;
    background:linear-gradient(
      90deg,
      transparent,
      rgba(255,255,255,.45),
      transparent
    );
    transform:skewX(-20deg);
}

.start:active::after{
    animation:shine .6s;
}

@keyframes shine{
    to{left:150%}
}

.status{
    text-align:center;
    color:#94a3b8;
    margin-top:13px;
    font-size:13px;
}

/* RESULTS */

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
    border:1px solid rgba(255,255,255,.06);
    border-radius:15px;
    padding:14px 8px;
    text-align:center;
}

.number{
    color:#38bdf8;
    font-size:21px;
    font-weight:900;
    font-family:monospace;
}

.result small{
    display:block;
    margin-top:5px;
    color:#94a3b8;
    font-size:11px;
}

.score{
    text-align:center;
    margin:18px 0;
}

.scoreNumber{
    font-size:44px;
    font-weight:900;
    color:#22c55e;
    text-shadow:0 0 20px rgba(34,197,94,.35);
}

.scoreText{
    color:#94a3b8;
    font-size:13px;
}

.service{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
    padding:13px;
    margin-top:8px;
    background:#07101d;
    border-radius:13px;
    border:1px solid rgba(255,255,255,.05);
    font-size:13px;
}

.good{color:#22c55e;font-weight:bold}
.medium{color:#facc15;font-weight:bold}
.bad{color:#ef4444;font-weight:bold}

.advice{
    margin-top:15px;
    padding:15px;
    border-radius:15px;
    background:rgba(56,189,248,.07);
    border:1px solid rgba(56,189,248,.15);
    color:#dbeafe;
    line-height:1.7;
    font-size:13px;
}

.hidden{display:none}

.footer{
    text-align:center;
    color:#475569;
    font-size:11px;
    margin-top:20px;
}

@media(max-width:500px){
    .info{grid-template-columns:1fr}
    .results{grid-template-columns:1fr}
    .advanced{grid-template-columns:1fr}
    .speedArea{height:250px}
    .ring{width:205px;height:205px}
    .liveSpeed{font-size:42px}
}
</style>
</head>

<body>

<div class="container">

<div class="header">
    <div class="logo">⚡ NETPULSE</div>
    <div class="welcome">WELCOME TO THE SMART INTERNET TEST</div>
</div>

<div class="card">

<h3 class="connection-title">🌍 YOUR CONNECTION</h3>

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

<div class="speedArea">

<div class="ring"></div>

<div class="rocket" id="rocket">🚀</div>

<div class="speedCenter">
<div class="liveSpeed" id="liveSpeed">0.0</div>
<div class="speedUnit" id="speedType">Mbps</div>
</div>

</div>

<button class="start" id="start" onclick="startTest()">
🚀 START SPEED TEST
</button>

<div class="status" id="status">Ready to test your connection</div>

</div>

<div class="card hidden" id="results">

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

<div class="score">
<div class="scoreNumber" id="score">--/100</div>
<div class="scoreText">NETPULSE CONNECTION SCORE</div>
</div>

<h3>📊 CONNECTION QUALITY</h3>

<div class="service">
<span>🎮 Competitive Gaming</span>
<span id="gaming">--</span>
</div>

<div class="service">
<span>🎬 4K Ultra HD</span>
<span id="video">--</span>
</div>

<div class="service">
<span>📡 Live Streaming</span>
<span id="stream">--</span>
</div>

<div class="service">
<span>📞 Video Calls</span>
<span id="calls">--</span>
</div>

<div class="service">
<span>📥 Large File Downloads</span>
<span id="files">--</span>
</div>

<div class="advice" id="advice">
💡 Smart Advisor will analyze your connection after the test.
</div>

</div>

<div class="footer">
NETPULSE — Smart Internet Performance Engine
</div>

</div>

<script>

async function loadIP(){

    try{

        const response = await fetch("/my-ip");
        const data = await response.json();

        document.getElementById("ip").innerText =
            data.ip || "Unknown";

        document.getElementById("country").innerText =
            data.flag + " " + (data.country || "Unknown");

        document.getElementById("city").innerText =
            data.city || "Unknown";

        document.getElementById("isp").innerText =
            data.isp || "Unknown";

    }catch(e){

        document.getElementById("ip").innerText="Unavailable";
        document.getElementById("country").innerText="Unknown";
        document.getElementById("city").innerText="Unknown";
        document.getElementById("isp").innerText="Unknown";

    }

}


async function pingTest(){

    const results=[];
    let lost=0;

    const total=10;

    for(let i=0;i<total;i++){

        const controller=new AbortController();

        const timeout=setTimeout(
            ()=>controller.abort(),
            1500
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

            results.push(end-start);

        }catch(e){

            clearTimeout(timeout);
            lost++;

        }

        await new Promise(
            r=>setTimeout(r,60)
        );

    }

    if(results.length===0){

        return {
            ping:999,
            jitter:999,
            packetLoss:100
        };

    }

    results.sort((a,b)=>a-b);

    const ping=results[0];

    let jitter=0;

    for(let i=1;i<results.length;i++){

        jitter+=Math.abs(
            results[i]-results[i-1]
        );

    }

    jitter =
        results.length>1
        ? jitter/(results.length-1)
        : 0;

    return{

        ping:Math.round(ping),

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

    const duration=5000;

    const start=performance.now();

    let bytes=0;

    while(
        performance.now()-start < duration
    ){

        const response=
            await fetch(
                "/download?x="+Math.random(),
                {cache:"no-store"}
            );

        const blob=
            await response.blob();

        bytes+=blob.size;

        const elapsed=
            (performance.now()-start)/1000;

        const speed=
            (bytes*8)/elapsed/1000000;

        live.innerText=
            speed.toFixed(1);

    }

    const elapsed=
        (performance.now()-start)/1000;

    return (bytes*8)/elapsed/1000000;

}


async function uploadTest(){

    const live=
        document.getElementById("liveSpeed");

    const duration=4000;

    const start=performance.now();

    let bytes=0;

    const chunk=512*1024;

    const payload=
        new Uint8Array(chunk);

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

        bytes+=chunk;

        const elapsed=
            (performance.now()-start)/1000;

        const speed=
            (bytes*8)/elapsed/1000000;

        live.innerText=
            speed.toFixed(1);

    }

    const elapsed=
        (performance.now()-start)/1000;

    return (bytes*8)/elapsed/1000000;

}


function calculateScore(
    download,
    upload,
    ping,
    jitter,
    packetLoss
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

    if(packetLoss>0)
        score-=packetLoss*3;

    return Math.max(
        Math.round(score),
        0
    );

}


function setStatus(id,text,type){

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
    packetLoss
){

    let gaming;

    if(
        ping<=40 &&
        jitter<=10 &&
        packetLoss===0
    ){

        gaming="🟢 Excellent";
        setStatus("gaming",gaming,"good");

    }else if(
        ping<=70 &&
        packetLoss<5
    ){

        gaming="🟡 Good";
        setStatus("gaming",gaming,"medium");

    }else{

        gaming="🔴 Poor";
        setStatus("gaming",gaming,"bad");

    }


    if(download>=25){

        setStatus(
            "video",
            "🟢 Excellent — 4K Ready",
            "good"
        );

    }else if(download>=12){

        setStatus(
            "video",
            "🟡 Good — Full HD",
            "medium"
        );

    }else{

        setStatus(
            "video",
            "🔴 Poor",
            "bad"
        );

    }


    if(upload>=10 && jitter<15){

        setStatus(
            "stream",
            "🟢 Excellent — 1080p",
            "good"
        );

    }else if(upload>=5){

        setStatus(
            "stream",
            "🟡 Good — 720p",
            "medium"
        );

    }else{

        setStatus(
            "stream",
            "🔴 Poor",
            "bad"
        );

    }


    if(
        ping<=100 &&
        packetLoss<2
    ){

        setStatus(
            "calls",
            "🟢 Excellent",
            "good"
        );

    }else{

        setStatus(
            "calls",
            "🟡 Fair",
            "medium"
        );

    }


    if(download>=50){

        setStatus(
            "files",
            "🟢 Very Fast",
            "good"
        );

    }else if(download>=20){

        setStatus(
            "files",
            "🟡 Good",
            "medium"
        );

    }else{

        setStatus(
            "files",
            "🔴 Slow",
            "bad"
        );

    }


    let advice;

    if(packetLoss>2){

        advice=
        "High packet loss detected. Check your Wi-Fi signal, router, or Ethernet cable.";

    }else if(jitter>20){

        advice=
        "Your connection has high jitter. Ethernet may provide a more stable connection.";

    }else if(ping>80){

        advice=
        "Your ping is relatively high. This may affect competitive online gaming.";

    }else if(download<15){

        advice=
        "Download speed is relatively low for 4K streaming and large downloads.";

    }else{

        advice=
        "Your connection is fast and stable for gaming, 4K streaming, calls and everyday use.";

    }

    document.getElementById("advice").innerText=
        "💡 Smart Advisor: "+advice;

}


async function startTest(){

    const button=
        document.getElementById("start");

    const status=
        document.getElementById("status");

    const speedType=
        document.getElementById("speedType");

    document.body.classList.add("testing");

    button.disabled=true;

    button.innerText=
        "⚡ TESTING...";

    document
        .getElementById("results")
        .classList.remove("hidden");


    document.getElementById("liveSpeed")
        .innerText="0.0";


    status.innerText=
        "🌐 Measuring connection quality...";

    const quality=
        await pingTest();


    document.getElementById("ping")
        .innerText=quality.ping;

    document.getElementById("jitter")
        .innerText=quality.jitter;

    document.getElementById("packetLoss")
        .innerText=quality.packetLoss;


    status.innerText=
        "⬇️ Measuring download speed...";

    speedType.innerText=
        "Mbps — DOWNLOAD";


    const download=
        await downloadTest();


    document.getElementById("download")
        .innerText=download.toFixed(2);


    status.innerText=
        "⬆️ Measuring upload speed...";

    speedType.innerText=
        "Mbps — UPLOAD";


    const upload=
        await uploadTest();


    document.getElementById("upload")
        .innerText=upload.toFixed(2);


    speedType.innerText="Mbps";

    document.getElementById("liveSpeed")
        .innerText=download.toFixed(1);


    const score=
        calculateScore(
            download,
            upload,
            quality.ping,
            quality.jitter,
            quality.packetLoss
        );


    document.getElementById("score")
        .innerText=score+"/100";


    analyze(
        download,
        upload,
        quality.ping,
        quality.jitter,
        quality.packetLoss
    );


    document.body.classList.remove("testing");

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


@app.route("/my-ip")
def my_ip():

    try:

        response=requests.get(
            "https://ipapi.co/json/",
            timeout=5
        )

        data=response.json()

        country=data.get(
            "country_name",
            "Unknown"
        )

        country_code=data.get(
            "country_code",
            ""
        )

        flag="🌍"

        if len(country_code)==2:

            flag="".join(
                chr(
                    127397+ord(c)
                )
                for c in country_code.upper()
            )

        return jsonify({

            "ip":data.get(
                "ip",
                "Unknown"
            ),

            "country":country,

            "city":data.get(
                "city",
                "Unknown"
            ),

            "isp":data.get(
                "org",
                "Unknown"
            ),

            "flag":flag

        })

    except Exception:

        return jsonify({

            "ip":"Unavailable",

            "country":"Unknown",

            "city":"Unknown",

            "isp":"Unknown",

            "flag":"🌍"

        })


@app.route("/ping")
def ping():

    return jsonify({
        "ok":True,
        "time":time.time()
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


@app.route("/upload",methods=["POST"])
def upload():

    request.get_data()

    return jsonify({
        "ok":True
    })


if __name__=="__main__":

    print()
    print("⚡ NETPULSE ENGINE ONLINE")
    print("==========================================")
    print("🌐 Open: http://127.0.0.1:5000")
    print("==========================================")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
