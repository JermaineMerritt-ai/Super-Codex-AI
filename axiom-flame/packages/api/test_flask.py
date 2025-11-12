from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Flask API is running"})

@app.route('/')
def root():
    return "Test Flask API Running"

if __name__ == "__main__":
    print("Starting test Flask API on port 8086...")
    app.run(host='127.0.0.1', port=8086, debug=False)