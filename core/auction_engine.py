import math
from config import WEIGHT_BATTERY, WEIGHT_PROXIMITY, WEIGHT_RELIABILITY

class AuctionEngine:
    @staticmethod
    def calculate_bid(bidder_pos, bidder_battery, target_sector_coords, base_reliability=1.0):
        """
        Calculates a score for bidding on an abandoned/martyr sector.
        Higher score = better candidate to take over the mission.
        """
        bx, by = bidder_pos
        tx, ty = target_sector_coords
        
        # Euclidean distance
        distance = math.sqrt((bx - tx)**2 + (by - ty)**2)
        # Normalize distance (max distance on a 10x10 grid is ~14.14)
        proximity_score = max(0.0, 1.0 - (distance / 15.0))
        
        battery_score = bidder_battery / 100.0
        
        total_score = (
            (battery_score * WEIGHT_BATTERY) +
            (proximity_score * WEIGHT_PROXIMITY) +
            (base_reliability * WEIGHT_RELIABILITY)
        )
        return round(total_score, 4)

    @staticmethod
    def resolve_auction(bids):
        """
        Input format: [{'node_id': 'DRONE-B', 'bid': 0.82}, ...]
        Returns the winning node_id.
        """
        if not bids:
            return None
        winning_bid = max(bids, key=lambda b: b['bid'])
        return winning_bid['node_id']
