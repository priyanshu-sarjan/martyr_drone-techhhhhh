import random
from core.mesh_node import DroneNode
from core.auction_engine import AuctionEngine
from config import GRID_SIZE, INITIAL_NODES

class SwarmMeshNetwork:
    def __init__(self):
        self.nodes = {}
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.event_logs = []
        self._init_swarm()

    def _init_swarm(self):
        # Partition grid sectors across nodes
        sectors_per_node = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                sectors_per_node.append((r, c))
        random.shuffle(sectors_per_node)

        # Initialize nodes with distributed workload
        split_size = len(sectors_per_node) // len(INITIAL_NODES)
        for idx, cfg in enumerate(INITIAL_NODES):
            drone = DroneNode(cfg["id"], cfg["x"], cfg["y"], cfg["battery"], cfg["role"])
            drone.assigned_sectors = sectors_per_node[idx * split_size : (idx + 1) * split_size]
            self.nodes[drone.node_id] = drone

    def update_tick(self):
        """Execute one simulation cycle."""
        for drone in self.nodes.values():
            drone.step()
            # Mark covered cells on the global map
            for cx, cy in drone.completed_sectors:
                self.grid[cx][cy] = 1

    def trigger_martyr_failover(self, failing_node_id):
        """
        Martyr protocol: Node initiates auction for all its unfinished sectors
        """
        if failing_node_id not in self.nodes:
            return None

        martyr = self.nodes[failing_node_id]
        martyr.trigger_failure()
        orphan_tasks = list(martyr.assigned_sectors)
        martyr.assigned_sectors = []

        self.event_logs.append(f"⚠️ [ALERT] {failing_node_id} reported critical failure! Triggering Decentralized Auction...")

        if not orphan_tasks:
            martyr.status = "OFFLINE"
            return {"winner": None, "tasks_reallocated": 0}

        # Collect P2P Bids from surviving peers
        bids = []
        for peer_id, peer in self.nodes.items():
            if peer_id != failing_node_id and peer.status == "ACTIVE":
                bid_value = peer.evaluate_bid_request(martyr.pos, orphan_tasks)
                bids.append({"node_id": peer_id, "bid": bid_value})
                self.event_logs.append(f"📡 Bid Received from {peer_id}: Score = {bid_value}")

        # Determine Auction Winner
        winner_id = AuctionEngine.resolve_auction(bids)
        if winner_id:
            self.nodes[winner_id].assigned_sectors.extend(orphan_tasks)
            self.event_logs.append(f"✅ Handover complete! {winner_id} won {len(orphan_tasks)} sectors from {failing_node_id}.")
        
        martyr.status = "OFFLINE"
        return {"winner": winner_id, "tasks_reallocated": len(orphan_tasks)}

    def get_swarm_state(self):
        return {
            "nodes": [node.generate_heartbeat() for node in self.nodes.values()],
            "grid": self.grid,
            "logs": self.event_logs[-8:] # return latest logs
        }
