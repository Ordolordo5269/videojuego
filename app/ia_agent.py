import random


class AIAgent:
    """Rule-based AI for the Swiss conflict simulator."""

    def __init__(self, game_state):
        self.game = game_state

    def decide_and_act(self):
        regions = self.game.regions
        # look for advantageous attacks
        for src, info in regions.items():
            if self.game.region_control(src) != "ai":
                continue
            for dest in self.game.adjacency.get(src, []):
                if self.game.region_control(dest) == "human":
                    atk = self.game._strength(src, "ai")
                    dfs = self.game._strength(dest, "human")
                    if atk > dfs:
                        self.game.attack("ai", src, dest)
                        return
        # otherwise move random unit
        own_regions = [r for r in regions if sum(regions[r]["ai"].values()) > 0]
        if not own_regions:
            return
        src = random.choice(own_regions)
        neighbors = self.game.adjacency[src]
        dest = random.choice(neighbors)
        types = [u for u, c in regions[src]["ai"].items() if c > 0]
        if types:
            utype = random.choice(types)
            self.game.move_unit("ai", utype, src, dest)
