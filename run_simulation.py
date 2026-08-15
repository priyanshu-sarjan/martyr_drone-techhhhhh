import time
from core.swarm_controller import SwarmMeshNetwork

def main():
    print("=== Starting Headless Aegis Swarm Mesh Simulation ===")
    swarm = SwarmMeshNetwork()

    for step in range(1, 10):
        print(f"\n--- Simulation Cycle #{step} ---")
        swarm.update_tick()

        # Simulate unexpected hardware crash on Drone B at step 3
        if step == 3:
            print("\n💥 Simulating Hardware Failure on DRONE-B...")
            swarm.trigger_martyr_failover("DRONE-B")

        state = swarm.get_swarm_state()
        for node in state["nodes"]:
            print(f"[{node['node_id']}] Status: {node['status']} | Pos: {node['pos']} | Bat: {node['battery']}% | Remaining Tasks: {node['remaining_tasks']}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
