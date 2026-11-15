from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>RAUDY VIP PRO - PROFESSIONAL</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
body{margin:0;background:#0A0E14;color:#fff;font-family:'Inter',Arial,sans-serif;padding:0}
.top{background:linear-gradient(90deg,#0A0E14,#1A2A1A);padding:20px 15px 10px;border-bottom:2px solid #FFD700}
.logo{font-size:28px;font-weight:800;letter-spacing:1px}
.logo span{color:#FFD700}
.sub{color:#9AA4B2;font-size:13px;margin-top:4px}
.live{display:inline-block;background:#0F2A1A;color:#00FF88;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:700;margin-top:10px;border:1px solid #00FF88}
.tabs{display:flex;gap:8px;padding:15px 15px 0}
.tab{flex:1;text-align:center;padding:12px 5px;border-radius:14px;font-weight:800;cursor:pointer;background:#111722;border:1px solid #1E2A3A;color:#fff;font-size:13px}
.tab.active{background:#FFD700;color:#000;border-color:#FFD700}
.divisas{display:none;gap:8px;flex-wrap:wrap;padding:12px 15px 0}
.divisas.show{display:flex}
.pair{padding:10px 14px;border-radius:20px;background:#111722;border:1px solid #1E2A3A;font-weight:700;font-size:13px;cursor:pointer}
.pair.active{background:#00FFFF;color:#000;border-color:#00FFFF}
.pair.acc.active{background:#FF9F43;color:#000;border-color:#FF9F43}
.price-card{background:#111722;border:1px solid #1E2A3A;border-radius:18px;margin:15px;padding:18px;text-align:left}
.price-label{color:#9AA4B2;font-size:12px;letter-spacing:1px}
.price-val{font-size:38px;font-weight:800;color:#FFD700;margin:5px 0}
.price-sub{color:#00FFFF;font-size:12px}
.signal-big{margin:15px;border-radius:18px;padding:22px;text-align:center;font-size:26px;font-weight:800;letter-spacing:0.5px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 15px 15px}
.card{background:#111722;border:1px solid #1E2A3A;border-radius:18px;padding:16px;text-align:center;position:relative;overflow:hidden}
.card.prof{border:1px solid #00FFFF}
.card-time{font-size:11px;color:#9AA4B2;letter-spacing:1px;font-weight:700}
.card-title{font-size:18px;font-weight:800;margin:8px 0}
.vel
