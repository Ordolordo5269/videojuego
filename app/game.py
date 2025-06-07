class GameState:
    """Simple game state for Swiss conflict simulator."""

    unit_types = {
        "infantry": {"power": 1},
        "mountain": {"power": 1.5},
        "mechanized": {"power": 2},
    }

    terrain_bonus = {
        "montana": {"mountain": 1},
        "urbano": {"mechanized": 0.5},
        "valle": {},
    }

    adjacency = {
        "Norte": ["Centro", "Este"],
        "Sur": ["Centro", "Oeste"],
        "Este": ["Centro", "Norte"],
        "Oeste": ["Centro", "Sur"],
        "Centro": ["Norte", "Sur", "Este", "Oeste"],
    }

    def __init__(self):
        self.score = 0
        self.regions = {
            "Norte": {
                "terrain": "montana",
                "human": {"infantry": 3, "mountain": 1, "mechanized": 0},
                "ai": {"infantry": 2, "mountain": 0, "mechanized": 0},
            },
            "Sur": {
                "terrain": "valle",
                "human": {"infantry": 2, "mountain": 0, "mechanized": 0},
                "ai": {"infantry": 2, "mountain": 1, "mechanized": 0},
            },
            "Este": {
                "terrain": "montana",
                "human": {"infantry": 1, "mountain": 0, "mechanized": 0},
                "ai": {"infantry": 3, "mountain": 1, "mechanized": 0},
            },
            "Oeste": {
                "terrain": "urbano",
                "human": {"infantry": 2, "mountain": 0, "mechanized": 1},
                "ai": {"infantry": 1, "mountain": 0, "mechanized": 0},
            },
            "Centro": {
                "terrain": "valle",
                "human": {"infantry": 1, "mountain": 0, "mechanized": 0},
                "ai": {"infantry": 1, "mountain": 0, "mechanized": 0},
            },
        }

    def reset(self):
        self.__init__()

    def move_unit(self, owner, unit_type, src, dest):
        if dest not in self.adjacency.get(src, []):
            return False
        if self.regions[src][owner].get(unit_type, 0) <= 0:
            return False
        self.regions[src][owner][unit_type] -= 1
        self.regions[dest][owner][unit_type] = (
            self.regions[dest][owner].get(unit_type, 0) + 1
        )
        if owner == "human":
            self.score += 5
            self._center_bonus()
        return True

    def _strength(self, region, owner):
        strength = 0
        terrain = self.regions[region]["terrain"]
        for utype, count in self.regions[region][owner].items():
            base = self.unit_types[utype]["power"] * count
            bonus = self.terrain_bonus.get(terrain, {}).get(utype, 0) * count
            strength += base + bonus
        return strength

    def attack(self, owner, src, dest):
        if dest not in self.adjacency.get(src, []):
            return False
        enemy = "ai" if owner == "human" else "human"
        atk = self._strength(src, owner)
        dfs = self._strength(dest, enemy)
        if atk > dfs:
            # move all units to target
            for utype, cnt in list(self.regions[src][owner].items()):
                if cnt > 0:
                    self.regions[dest][owner][utype] = (
                        self.regions[dest][owner].get(utype, 0) + cnt
                    )
                    self.regions[src][owner][utype] = 0
            # remove defenders
            for utype in list(self.regions[dest][enemy].keys()):
                self.regions[dest][enemy][utype] = 0
            if owner == "human":
                self.score += 10
        else:
            # attacker loses one unit
            for utype, cnt in self.regions[src][owner].items():
                if cnt > 0:
                    self.regions[src][owner][utype] -= 1
                    break
            if owner == "human":
                self.score -= 5
        if owner == "human":
            self._center_bonus()
        return True

    def region_control(self, region):
        h_total = sum(self.regions[region]["human"].values())
        ai_total = sum(self.regions[region]["ai"].values())
        if h_total > ai_total:
            return "human"
        if ai_total > h_total:
            return "ai"
        return "neutral"

    def _center_bonus(self):
        if self.region_control("Centro") == "human":
            self.score += 3

    def to_dict(self):
        data = {
            region: {
                "terrain": info["terrain"],
                "human": info["human"],
                "ai": info["ai"],
                "control": self.region_control(region),
            }
            for region, info in self.regions.items()
        }
        data["score"] = self.score
        return data
