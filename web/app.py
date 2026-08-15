import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from core.swarm_controller import SwarmMeshNetwork
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aegis-swarm-token'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

swarm = SwarmMeshNetwork()

def simulation_worker():
    """Background thread emitting real-time swarm updates to UI."""
    while True:
        swarm.update_tick()
        state = swarm.get_swarm_state()
        socketio.emit('swarm_update', state)
        time.sleep(1.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/failover', methods=['POST'])
def manual_failover():
    data = request.get_json()
    node_id = data.get('node_id')
    result = swarm.trigger_martyr_failover(node_id)
    return jsonify({"status": "SUCCESS", "result": result})

if __name__ == '__main__':
    threading.Thread(target=simulation_worker, daemon=True).start()
    print("🚀 Aegis Swarm Control Server running on http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
