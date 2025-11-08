


from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>WORKING! ✅</h1><p>Agar ye dikh raha hai to Flask chal raha hai!</p>'

if __name__ == '__main__':
    print('\n' + '='*40)
    print('✅ Server chal rahi hai!')
    print('🌐 Browser mein kholo: localhost:5000')
    print('='*40 + '\n')
    app.run(host='0.0.0.0', port=5000, debug=False)

