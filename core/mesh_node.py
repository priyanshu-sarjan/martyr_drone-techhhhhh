import time
import math
from core.auction_engine import AuctionEngine

class DroneNode:
    def __init__(self, node_id, x, y, battery, role="Scout"):
        self.node_id = node_id
        self.pos = [x, y]
        self.battery = battery
        self.role = role
        self.status = "ACTIVE"  # ACTIVE, MARTYR_FAILING, OFFLINE
        self.assigned_sectors = []
        self.completed_sectors = []
        self.peers = {}

    def step(self):
        """Simulates battery depletion, waypoint traversal, and grid coverage."""
        if self.status != "ACTIVE":
            return

        # Drain battery slightly
        self.battery = max(0, self.battery - 0.5)

        # Move towards assigned target if exists
        if self.assigned_sectors:
            target = self.assigned_sectors[0]
            tx, ty = target
            cx, cy = self.pos

            # Move 1 step towards target
            if cx < tx: self.pos[0] += 1
            elif cx > tx: self.pos[0] -= 1
            
            if cy < ty: self.pos[1] += 1
            elif cy > ty: self.pos[1] -= 1

            # Check if sector reached
            if self.pos[0] == tx and self.pos[1] == ty:
                self.completed_sectors.append(self.assigned_sectors.pop(0))

    def trigger_failure(self):
        """Simulate hardware damage / critical power failure."""
        self.status = "MARTYR_FAILING"
        self.battery = 5.0  # critical state

    def generate_heartbeat(self):
        return {
            "node_id": self.node_id,
            "pos": self.pos,
            "battery": round(self.battery, 1),
            "status": self.status,
            "remaining_tasks": len(self.assigned_sectors),
            "timestamp": time.time()
        }

    def evaluate_bid_request(self, martyr_pos, martyr_sectors):
        """Calculates bid if this drone is active."""
        if self.status != "ACTIVE" or self.battery < 20:
            return 0.0
        
        target = martyr_sectors[0] if martyr_sectors else martyr_pos
        return AuctionEngine.calculate_bid(self.pos, self.battery, target)
