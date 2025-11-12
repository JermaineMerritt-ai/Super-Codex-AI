from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'working', 'message': 'Flask native binding test'}

@app.route('/')
def root():
    return 'Flask Native Test - Binding to 0.0.0.0:8096'

if __name__ == '__main__':
    print('Starting Flask on 0.0.0.0:8096...')
    app.run(host='0.0.0.0', port=8096, debug=False)