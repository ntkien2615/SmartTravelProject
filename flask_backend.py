"""
Flask backend for session management
Runs alongside Streamlit to provide persistent sessions
Uses in-memory dictionary to persist session across requests
"""
from flask import Flask, request, jsonify
from datetime import timedelta
import secrets

app = Flask(__name__)

# Simple in-memory session storage
# This will persist as long as Flask is running
session_storage = {}

@app.route('/api/session', methods=['GET'])
def get_session():
    """Get current session data"""
    return jsonify({
        'logged_in': session_storage.get('logged_in', False),
        'username': session_storage.get('username', ''),
        'user_id': session_storage.get('user_id', None)
    })

@app.route('/api/session', methods=['POST'])
def set_session():
    """Set session data"""
    data = request.json
    if data:
        session_storage['logged_in'] = data.get('logged_in', False)
        session_storage['username'] = data.get('username', '')
        session_storage['user_id'] = data.get('user_id', None)
    return jsonify({'success': True})

@app.route('/api/session', methods=['DELETE'])
def clear_session():
    """Clear session (logout)"""
    session_storage.clear()
    return jsonify({'success': True})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Flask backend is running'})

if __name__ == '__main__':
    # Run without reloader to avoid issues with Streamlit
    # Use threaded mode for better concurrency
    app.run(
        host='127.0.0.1',
        port=5000, 
        debug=False,  # Disable debug to prevent reloader issues
        use_reloader=False,  # Explicitly disable reloader
        threaded=True  # Enable threading for concurrent requests
    )
