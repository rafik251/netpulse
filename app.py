from flask import Flask, render_template_string, jsonify, request, Response
import requests
import time
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NETPULSE</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    min-height:100vh;
    font-family:Arial,sans-serif;
    color:white;
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
    font-size:14px;
    letter-spacing:3px;
}

.logo{
    margin-top:8px;
    font-size:42px;
    font-weight:900;
    color:#38bdf8;
    text-shadow:0 0 10px #38bdf8,0 0 35px #38bdf855;
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
    padding:13px;
    border-radius:15px;
    background:#07101d;
}

.label{
    color:#64748b;
    font-size:10px;
    text-transform:uppercase;
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
    color:white;
    font-size:19px;
    font-weight:900;
    cursor:pointer;
    background:linear-gradient(
        90deg,#06b6d4,#6366f1,#a855f7
    );
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
    margin:15px;
}

.speed{
    text-align:center;
    font-family:monospace;
    font-size:60px;
    font-weight:900;
    color:#38bdf8;
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
    .info{
        grid-template-columns:1fr;
    }

    .results{
        grid-template-columns:1fr;
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
    <div class="subtitle">
        SMART INTERNET PERFORMANCE TEST
    </div>
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
<span>📥 Large File Downloads</span>
<strong id="files">--</strong>
</div>

<div class="advice" id="advice">
💡 Smart Advisor
</div>

</div>

</div>

<script>

async function loadIP(){

    try{

        const response = await fetch(
            "https://api64.ipify.org?format=json"
        );

        const data = await response.json();

        const ip = data.ip;

        document.getElementById("ip").innerText = ip;

        const geo = await fetch(
            "/lookup-ip?ip=" + encodeURIComponent(ip)
        );

        const info = await geo.json();

        document.getElementById("country").innerText =
            (info.flag || "") + " " +
            (info.country || "Unknown");

        document.getElementById("city").innerText =
            info.city || "Unknown";

        document.getElementById("isp").innerText =
            info.isp || "Unknown";

    }catch(error){

        document.getElementById("ip").innerText =
            "Unavailable";

        document.getElementById("country").innerText =
            "Unknown";

        document.getElementById("city").innerText =
            "Unknown";

        document.getElementById("isp").innerText =
            "Unknown";
    }
}


async function pingTest(){

    let values = [];
    let lost = 0;

    for(let i=0;i<10;i++){

        const start = performance.now();

        try{

            await fetch(
                "/ping?x=" + Math.random(),
                {cache:"no-store"}
            );

            values.push(
                performance.now() - start
            );

        }catch(error){

            lost++;
        }

        await new Promise(
            resolve => setTimeout(resolve,70)
        );
    }

    if(values.length === 0){

        return {
            ping:999,
            jitter:0,
            loss:100
        };
    }

    values.sort((a,b)=>a-b);

    let jitter = 0;

    for(let i=1;i<values.length;i++){

        jitter += Math.abs(
            values[i]-values[i-1]
        );
    }

    if(values.length > 1){

        jitter =
            jitter/(values.length-1);
    }

    return {
        ping:Math.round(values[0]),
        jitter:Math.round(jitter),
        loss:Number(
            ((lost/10)*100).toFixed(1)
        )
    };
}


async function downloadTest(){

    const start = performance.now();
    let bytes = 0;

    while(performance.now()-start < 5000){

        const response = await fetch(
            "/download?x=" + Math.random(),
            {cache:"no-store"}
        );

        const blob = await response.blob();

        bytes += blob.size;

        const seconds =
            (performance.now()-start)/1000;

        const speed =
            bytes*8/seconds/1000000;

        document.getElementById(
            "liveSpeed"
        ).innerText =
            speed.toFixed(1);
    }

    const seconds =
        (performance.now()-start)/1000;

    return bytes*8/seconds/1000000;
}


async function uploadTest(){

    const start = performance.now();
    let bytes = 0;

    const data =
        new Uint8Array(512*1024);

    while(performance.now()-start < 5000){

        await fetch(
            "/upload?x=" + Math.random(),
            {
                method:"POST",
                body:data
            }
        );

        bytes += data.length;

        const seconds =
            (performance.now()-start)/1000;

        const speed =
            bytes*8/seconds/1000000;

        document.getElementById(
            "liveSpeed"
        ).innerText =
            speed.toFixed(1);
    }

    const seconds =
        (performance.now()-start)/1000;

    return bytes*8/seconds/1000000;
}


function scoreTest(
    download,
    upload,
    ping,
    jitter,
    loss
){

    let score = 100;

    if(download < 10){
        score -= 25;
    }else if(download < 30){
        score -= 15;
    }else if(download < 50){
        score -= 5;
    }

    if(upload < 5){
        score -= 15;
    }else if(upload < 15){
        score -= 8;
    }

    if(ping > 100){
        score -= 25;
    }else if(ping > 50){
        score -= 12;
    }

    if(jitter > 20){
        score -= 15;
    }

    score -= loss * 3;

    return Math.max(
        0,
        Math.round(score)
    );
}


function setQuality(
    id,
    text,
    color
){

    const element =
        document.getElementById(id);

    element.innerText = text;
    element.className = color;
}


function analyze(
    download,
    upload,
    ping,
    jitter,
    loss
){

    if(ping <= 40 && jitter <= 10 && loss === 0){

        setQuality(
            "gaming",
            "🟢 Excellent",
            "good"
        );

    }else if(ping <= 70 && loss < 5){

        setQuality(
            "gaming",
            "🟡 Good",
            "medium"
        );

    }else{

        setQuality(
            "gaming",
            "🔴 Poor",
            "bad"
        );
    }


    if(download >= 25){

        setQuality(
            "video",
            "🟢 Excellent — 4K UHD",
            "good"
        );

    }else if(download >= 12){

        setQuality(
            "video",
            "🟡 Good — Full HD",
            "medium"
        );

    }else{

        setQuality(
            "video",
            "🔴 Poor",
            "bad"
        );
    }


    if(upload >= 10 && jitter < 15){

        setQuality(
            "stream",
            "🟢 Excellent",
            "good"
        );

    }else if(upload >= 5){

        setQuality(
            "stream",
            "🟡 Moderate",
            "medium"
        );

    }else{

        setQuality(
            "stream",
            "🔴 Poor",
            "bad"
        );
    }


    if(ping <= 100 && loss < 2){

        setQuality(
            "calls",
            "🟢 Excellent",
            "good"
        );

    }else{

        setQuality(
            "calls",
            "🟡 Fair",
            "medium"
        );
    }


    if(download >= 50){

        setQuality(
            "files",
            "🟢 Very Fast",
            "good"
        );

    }else if(download >= 20){

        setQuality(
            "files",
            "🟡 Fast",
            "medium"
        );

    }else{

        setQuality(
            "files",
            "🔴 Slow",
            "bad"
        );
    }


    let advice;

    if(loss > 2){

        advice =
            "High packet loss detected.";

    }else if(jitter > 20){

        advice =
            "Your connection has high jitter.";

    }else if(ping > 80){

        advice =
            "Your ping is relatively high.";

    }else if(download < 15){

        advice =
            "Your download speed is relatively low.";

    }else{

        advice =
            "Your connection is fast and stable.";
    }

    document.getElementById(
        "advice"
    ).innerText =
        "💡 Smart Advisor: " + advice;
}


async function startTest(){

    const button =
        document.getElementById("start");

    const status =
        document.getElementById("status");

    document.getElementById(
        "results"
    ).classList.remove("hidden");

    button.disabled = true;

    status.innerText =
        "🌐 Testing connection...";

    const quality =
        await pingTest();

    document.getElementById(
        "ping"
    ).innerText = quality.ping;

    document.getElementById(
        "jitter"
    ).innerText = quality.jitter;

    document.getElementById(
        "packetLoss"
    ).innerText = quality.loss;


    status.innerText =
        "⬇️ Measuring download...";

    const download =
        await downloadTest();

    document.getElementById(
        "download"
    ).innerText =
        download.toFixed(2);


    status.innerText =
        "⬆️ Measuring upload...";

    const upload =
        await uploadTest();

    document.getElementById(
        "upload"
    ).innerText =
        upload.toFixed(2);


    const score =
        scoreTest(
            download,
            upload,
            quality.ping,
            quality.jitter,
            quality.loss
        );

    document.getElementById(
        "score"
    ).innerText =
        score + "/100";


    analyze(
        download,
        upload,
        quality.ping,
        quality.jitter,
        quality.loss
    );


    status.innerText =
        "✅ TEST COMPLETE";

    button.disabled = false;

    button.innerText =
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


@app.route("/lookup-ip")
def lookup_ip():

    ip = request.args.get("ip", "").strip()

    if not ip:
        return jsonify({
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "flag": ""
        })

    try:

        response = requests.get(
            "https://ipwho.is/" + ip,
            timeout=10,
            headers={
                "User-Agent": "NETPULSE"
            }
        )

        data = response.json()

        country_code = (
            data.get("country_code") or ""
        ).upper()

        flag = ""

        if len(country_code) == 2:

            flag = "".join(
                chr(127397 + ord(c))
                for c in country_code
            )

        connection = data.get("connection") or {}

        return jsonify({
            "country":
                data.get("country") or "Unknown",

            "city":
                data.get("city") or "Unknown",

            "isp":
                connection.get("isp") or "Unknown",

            "flag": flag
        })

    except Exception as error:

        print("IP lookup error:", error)

        return jsonify({
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "flag": ""
        })


@app.route("/ping")
def ping():

    return jsonify({
        "ok": True,
        "time": time.time()
    })


@app.route("/download")
def download():

    data = os.urandom(
        2 * 1024 * 1024
    )

    return Response(
        data,
        mimetype="application/octet-stream",
        headers={
            "Cache-Control": "no-store",
            "Content-Length": str(len(data))
        }
    )


@app.route("/upload", methods=["POST"])
def upload():

    request.get_data()

    return jsonify({
        "ok": True
    })


if __name__ == "__main__":

    print()
    print("⚡ NETPULSE ENGINE ONLINE")
    print("🌐 http://127.0.0.1:5000")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
