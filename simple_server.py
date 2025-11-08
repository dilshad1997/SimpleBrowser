


from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quote Generator</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px}
.box{max-width:500px;margin:0 auto;background:#fff;border-radius:20px;padding:25px;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
h1{color:#764ba2;text-align:center;margin-bottom:20px}
textarea{width:100%;padding:15px;border:2px solid #ddd;border-radius:10px;font-size:16px;min-height:150px;font-family:inherit}
textarea:focus{outline:none;border-color:#764ba2}
button{width:100%;padding:15px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:10px;font-size:18px;font-weight:bold;margin-top:15px;cursor:pointer}
button:active{transform:scale(0.98)}
#preview{margin-top:20px;padding:20px;background:#f8f9fa;border-radius:10px;display:none}
.quote-card{background:linear-gradient(135deg,#2a0000,#000);color:#fff;padding:30px;border-radius:15px;margin-bottom:15px;box-shadow:0 5px 15px rgba(0,0,0,0.3);text-align:center}
.quote-card h2{color:#ff5577;margin-bottom:15px;font-size:20px}
.quote-card p{font-size:16px;line-height:1.8}
.btn-copy{background:#28a745;padding:10px 20px;color:#fff;border:none;border-radius:8px;cursor:pointer;margin-top:10px}
</style>
</head>
<body>
<div class="box">
<h1>🎬 Quote Generator</h1>
<p style="text-align:center;color:#666;margin-bottom:15px">अपने quotes की beautiful preview बनाएं</p>

<label style="display:block;margin-bottom:5px;font-weight:600;color:#333">📝 Title</label>
<input type="text" id="title" value="💔 दर्द भरे अल्फ़ाज़ 💔" style="width:100%;padding:12px;border:2px solid #ddd;border-radius:10px;font-size:16px;margin-bottom:15px">

<label style="display:block;margin-bottom:5px;font-weight:600;color:#333">✍️ Quotes (हर लाइन पर एक)</label>
<textarea id="quotes">😢 तू अगर छोड़ के जाने पे तुला है तो जा
जान भी जिस्म से जाती है तो कब पूछती है 💔

💔 मुझे शौक-ए-शायरी, मुझे दर्द से प्यार है
दर्द देता है जो वो मुझे बहुत प्यारा है

💫 ज़िंदगी खूबसूरत है, पर यादें बदसूरत हैं
खुशियाँ आती हैं मगर टिकती नहीं</textarea>

<button onclick="generate()">✨ Generate Preview</button>

<div id="preview"></div>
</div>

<script>
function generate(){
const title=document.getElementById('title').value;
const quotes=document.getElementById('quotes').value.trim();
const preview=document.getElementById('preview');

if(!quotes){alert('Quotes लिखें!');return}

const quotesList=quotes.split('\\n\\n').filter(q=>q.trim());
let html='<h3 style="margin-bottom:15px;color:#333">📱 Preview:</h3>';

quotesList.forEach(quote=>{
html+=`<div class="quote-card">
<h2>${title}</h2>
<p>${quote.replace(/\\n/g,'<br>')}</p>
<button class="btn-copy" onclick="copyQuote(this)">📋 Copy</button>
</div>`;
});

html+=`<p style="text-align:center;color:#666;margin-top:15px">
💡 Tip: Screenshot लें और share करें!
</p>`;

preview.innerHTML=html;
preview.style.display='block';
preview.scrollIntoView({behavior:'smooth'});
}

function copyQuote(btn){
const text=btn.parentElement.innerText;
if(navigator.clipboard){
navigator.clipboard.writeText(text);
btn.textContent='✅ Copied!';
setTimeout(()=>btn.textContent='📋 Copy',2000);
}
}
</script>
</body>
</html>'''

@app.route('/')
def home():
    return HTML

if __name__=='__main__':
    print('\\n'+'='*50)
    print('✅ SERVER RUNNING!')
    print('🌐 Open: http://localhost:5000')
    print('='*50+'\\n')
    app.run(host='0.0.0.0',port=5000,debug=False)

