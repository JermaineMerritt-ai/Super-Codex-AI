from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'alive', 'service': 'axiom-flame-docker'}

@app.route('/')
def root():
    return 'Axiom-Flame Docker API - Ready for Testing'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8095, debug=False)