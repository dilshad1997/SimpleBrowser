


from flask import Flask, render_template_string, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import io
import tempfile
from datetime import datetime

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>🎬 Poster to GIF Generator</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:system-ui,-apple-system,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:15px;color:#fff}
  .container{max-width:600px;margin:0 auto}
  .card{background:rgba(255,255,255,0.95);border-radius:20px;padding:20px;margin-bottom:20px;box-shadow:0 10px 40px rgba(0,0,0,0.3)}
  h1{color:#764ba2;margin-bottom:15px;font-size:24px;text-align:center}
  .emoji{font-size:32px;text-align:center;margin:10px 0}
  label{display:block;margin-top:15px;font-weight:600;color:#333;font-size:14px}
  textarea,input[type=text],input[type=number]{width:100%;padding:12px;border:2px solid #ddd;border-radius:10px;font-size:15px;margin-top:5px;transition:border 0.3s}
  textarea:focus,input:focus{outline:none;border-color:#764ba2}
  textarea{min-height:150px;font-family:inherit;resize:vertical}
  .row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
  button{width:100%;padding:15px;border:none;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer;margin-top:15px;transition:all 0.3s;box-shadow:0 4px 15px rgba(0,0,0,0.2)}
  .btn-primary{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff}
  .btn-primary:active{transform:scale(0.98)}
  .btn-secondary{background:linear-gradient(135deg,#f093fb,#f5576c);color:#fff}
  .btn-success{background:linear-gradient(135deg,#4facfe,#00f2fe);color:#fff}
  button:disabled{opacity:0.6;cursor:not-allowed}
  .status{text-align:center;margin-top:10px;padding:10px;border-radius:8px;font-size:14px;color:#333}
  .status.loading{background:#fff3cd;border:2px solid #ffc107}
  .status.success{background:#d4edda;border:2px solid #28a745}
  .status.error{background:#f8d7da;border:2px solid #dc3545}
  .preview{margin-top:20px;text-align:center;display:none}
  .preview img{max-width:100%;border-radius:15px;box-shadow:0 8px 30px rgba(0,0,0,0.3)}
  .actions{display:flex;gap:10px;margin-top:15px}
  .spinner{border:3px solid rgba(255,255,255,0.3);border-top:3px solid #fff;border-radius:50%;width:30px;height:30px;animation:spin 1s linear infinite;margin:20px auto}
  @keyframes spin{to{transform:rotate(360deg)}}
  .info{background:rgba(118,75,162,0.1);padding:15px;border-radius:10px;margin-top:15px;color:#333;font-size:13px;line-height:1.6}
  .badge{display:inline-block;padding:4px 8px;background:#764ba2;color:#fff;border-radius:5px;font-size:11px;margin-left:5px}
</style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div class="emoji">🎬✨</div>
      <h1>Poster to GIF Generator</h1>
      <p style="text-align:center;color:#666;margin-bottom:15px">दर्द भरे अल्फ़ाज़ — अपनी quotes की animated GIF बनाएं</p>

      <label>📝 Title (हैडर)</label>
      <input id="title" type="text" placeholder="💔 दर्द भरे अल्फ़ाज़ 💔" value="💔 दर्द भरे अल्फ़ाज़ 💔">

      <label>✍️ Quotes (हर लाइन पर एक quote) <span class="badge">3-5 quotes recommended</span></label>
      <textarea id="quotes" placeholder="हर लाइन पर एक शेर / quote लिखें...">😢 तू अगर छोड़ के जाने पे तुला है तो जा,
जान भी जिस्म से जाती है तो कब पूछती है। 💔

💔 मुझे शौक-ए-शायरी, मुझे दर्द से प्यार है
दर्द देता है जो वो मुझे बहुत प्यारा है

💫 ज़िंदगी खूबसूरत है, पर यादें बदसूरत हैं
खुशियाँ आती हैं मगर टिकती नहीं

🥀 दिल टूटा है, पर उम्मीद अभी बाकी है
ज़िंदगी चलती रहती है, साथ हो या न हो</textarea>

      <div class="row">
        <div>
          <label>⏱️ Duration (per quote)</label>
          <input id="duration" type="number" min="3" max="10" value="5" style="width:100%">
          <small style="color:#666">seconds</small>
        </div>
        <div>
          <label>📐 Size</label>
          <select id="size" style="width:100%;padding:12px;border:2px solid #ddd;border-radius:10px;margin-top:5px">
            <option value="story">📱 Instagram Story</option>
            <option value="post" selected>📷 Square Post</option>
            <option value="wide">🖼️ Wide (16:9)</option>
          </select>
        </div>
      </div>

      <button class="btn-primary" onclick="generateGif()">
        🎬 Generate GIF
      </button>

      <div id="loading" style="display:none">
        <div class="spinner"></div>
        <p style="text-align:center;color:#333;margin-top:10px">GIF बन रही है... कृपया प्रतीक्षा करें</p>
      </div>

      <div id="status"></div>
    </div>

    <div class="card preview" id="previewCard">
      <h2 style="color:#764ba2;margin-bottom:15px">✨ Preview</h2>
      <img id="gifPreview" src="" alt="Generated GIF">
      <div class="actions">
        <a id="downloadBtn" class="btn-success" style="text-decoration:none;text-align:center;flex:1" download="dard-bhare-alfaaz.gif">
          📥 Download GIF
        </a>
      </div>
      <button class="btn-secondary" onclick="shareGif()">
        📱 Share
      </button>
    </div>

    <div class="info">
      <strong>ℹ️ कैसे उपयोग करें:</strong><br>
      • हर quote को नई लाइन पर लिखें<br>
      • खाली लाइन से quotes को अलग करें<br>
      • Duration adjust करें (3-10 seconds)<br>
      • Size चुनें: Story (1080x1920), Post (1080x1080), या Wide<br>
      • Generate करने के बाद Download या Share करें
    </div>
  </div>

<script>
async function generateGif() {
  const title = document.getElementById('title').value.trim();
  const quotes = document.getElementById('quotes').value.trim();
  const duration = parseInt(document.getElementById('duration').value);
  const size = document.getElementById('size').value;

  if (!quotes) {
    showStatus('कृपया कम से कम एक quote लिखें!', 'error');
    return;
  }

  const loading = document.getElementById('loading');
  const status = document.getElementById('status');
  const previewCard = document.getElementById('previewCard');

  loading.style.display = 'block';
  status.innerHTML = '';
  previewCard.style.display = 'none';

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({title, quotes, duration, size})
    });

    if (!response.ok) throw new Error('Generation failed');

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    document.getElementById('gifPreview').src = url;
    document.getElementById('downloadBtn').href = url;
    previewCard.style.display = 'block';
    
    showStatus('✅ GIF तैयार है! अब Download या Share करें', 'success');
    
    // Scroll to preview
    previewCard.scrollIntoView({behavior: 'smooth', block: 'center'});
  } catch (error) {
    showStatus('❌ Error: ' + error.message, 'error');
  } finally {
    loading.style.display = 'none';
  }
}

function showStatus(message, type) {
  const status = document.getElementById('status');
  status.innerHTML = message;
  status.className = 'status ' + type;
  status.style.display = 'block';
}

async function shareGif() {
  const gifUrl = document.getElementById('downloadBtn').href;
  
  if (navigator.share) {
    try {
      const response = await fetch(gifUrl);
      const blob = await response.blob();
      const file = new File([blob], 'dard-bhare-alfaaz.gif', {type: 'image/gif'});
      
      await navigator.share({
        title: 'दर्द भरे अल्फ़ाज़',
        text: 'Check out this beautiful quote GIF!',
        files: [file]
      });
    } catch (err) {
      alert('Share करने में समस्या: ' + err.message);
    }
  } else {
    alert('आपका browser share feature support नहीं करता। Download करके manually share करें।');
  }
}
</script>
</body>
</html>
'''

def create_gif_frame(width, height, title, quote, bg_color=(42, 0, 0), frame_num=0):
    """Create a single frame for the GIF"""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load custom font
    try:
        font_path = os.path.expanduser('~/NotoNastaliqUrdu-Regular.ttf')
        if os.path.exists(font_path):
            title_font = ImageFont.truetype(font_path, int(height * 0.05))
            quote_font = ImageFont.truetype(font_path, int(height * 0.035))
        else:
            title_font = ImageFont.load_default()
            quote_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        quote_font = ImageFont.load_default()
    
    # Draw gradient effect (simulate with rectangles)
    for i in range(height):
        alpha = i / height
        color = (
            int(42 + (0 - 42) * alpha),
            int(0 + (0 - 0) * alpha),
            int(0 + (0 - 0) * alpha)
        )
        draw.rectangle([(0, i), (width, i+1)], fill=color)
    
    # Draw title with glow effect
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = int(height * 0.15)
    
    # Glow effect
    for offset in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
        draw.text((title_x + offset[0], title_y + offset[1]), title, 
                 fill=(170, 0, 0), font=title_font)
    draw.text((title_x, title_y), title, fill=(255, 85, 119), font=title_font)
    
    # Draw quote (multiline)
    lines = quote.split('\n')
    total_height = len(lines) * int(height * 0.08)
    y_start = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        if line.strip():
            bbox = draw.textbbox((0, 0), line, font=quote_font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2
            y = y_start + i * int(height * 0.08)
            
            # Shadow
            draw.text((x+2, y+2), line, fill=(0, 0, 0), font=quote_font)
            # Main text
            draw.text((x, y), line, fill=(255, 255, 255), font=quote_font)
    
    # Add animated hearts
    heart_emoji = "💔"
    num_hearts = 8
    for i in range(num_hearts):
        offset = (frame_num * 2) % height
        x = int(width * 0.1) + (i % 2) * int(width * 0.8)
        y = (i * int(height * 0.15) + offset) % height
        try:
            draw.text((x, y), heart_emoji, font=title_font, 
                     fill=(255, 0, 0, 128))
        except:
            pass
    
    return img

def create_animated_gif(title, quotes_list, duration=5, size='post'):
    """Create animated GIF from quotes"""
    # Size presets
    sizes = {
        'story': (1080, 1920),   # Instagram Story
        'post': (1080, 1080),    # Square Post
        'wide': (1920, 1080)     # Wide format
    }
    width, height = sizes.get(size, (1080, 1080))
    
    frames = []
    fps = 10  # Frames per second for animation
    
    for quote in quotes_list:
        # Create multiple frames for smooth animation
        for frame_num in range(duration * fps):
            frame = create_gif_frame(width, height, title, quote, frame_num=frame_num)
            frames.append(frame)
    
    # Save to temporary file
    output = io.BytesIO()
    
    # Optimize and save
    frames[0].save(
        output,
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=int(1000/fps),  # Duration per frame in ms
        loop=0,
        optimize=True
    )
    
    output.seek(0)
    return output

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        
        title = data.get('title', '💔 दर्द भरे अल्फ़ाज़ 💔')
        quotes_text = data.get('quotes', '')
        duration = int(data.get('duration', 5))
        size = data.get('size', 'post')
        
        # Parse quotes (split by double newline or single if no empty lines)
        quotes_list = []
        current_quote = []
        
        for line in quotes_text.split('\n'):
            line = line.strip()
            if line:
                current_quote.append(line)
            elif current_quote:
                quotes_list.append('\n'.join(current_quote))
                current_quote = []
        
        if current_quote:
            quotes_list.append('\n'.join(current_quote))
        
        if not quotes_list:
            quotes_list = ["😢 तू अगर छोड़ के जाने पे तुला है तो जा,\nजान भी जिस्म से जाती है तो कब पूछती है। 💔"]
        
        # Generate GIF
        gif_data = create_animated_gif(title, quotes_list, duration, size)
        
        return send_file(
            gif_data,
            mimetype='image/gif',
            as_attachment=True,
            download_name=f'dard-bhare-alfaaz-{datetime.now().strftime("%Y%m%d_%H%M%S")}.gif'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting server...")
    print("📱 Open in browser: http://localhost:5000")
    print("🌐 Or use your local IP to access from other devices")
    print("⏹️  Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5000, debug=True)

