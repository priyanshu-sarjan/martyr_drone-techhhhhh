# Grid & Swarm Simulation Configurations
GRID_SIZE = 10  # 10x10 Search Matrix
TOTAL_NODES = 4
BROADCAST_INTERVAL = 1.0  # seconds

# Auction Weight Factors
WEIGHT_BATTERY = 0.4
WEIGHT_PROXIMITY = 0.4
WEIGHT_RELIABILITY = 0.2

# Node Start Coordinates & Initial Health
INITIAL_NODES = [
    {"id": "DRONE-A", "x": 0, "y": 0, "battery": 95, "role": "Scout", "status": "ACTIVE"},
    {"id": "DRONE-B", "x": 0, "y": 9, "battery": 90, "role": "Scout", "status": "ACTIVE"},
    {"id": "DRONE-C", "x": 9, "y": 0, "battery": 85, "role": "Scout", "status": "ACTIVE"},
    {"id": "DRONE-D", "x": 9, "y": 9, "battery": 88, "role": "Scout", "status": "ACTIVE"}
]
