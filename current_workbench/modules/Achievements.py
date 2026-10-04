from typing import Callable, List


class Achievement:
    """ This class describes an achievement, unlocked when its condition is met. """
    def __init__(self, key:str, name:str, description:str, reward:int, condition:Callable[[dict], bool]) -> None:
        """
        Initialize a new object of Achievement class.

        args:
            key (str): identifier of the achievement, used in the save file.
            name (str): name shown to the player.
            description (str): how to unlock it.
            reward (int): Stellor given when unlocked.
            condition (callable): function(stats) -> bool, True when the achievement is unlocked.
        """
        self.key = key
        self.name = name
        self.description = description
        self.reward = reward
        self.condition = condition


# stats keys:
#   totals over all games : kills, bosses, bonus, games, purchases
#   current game          : score, game_time (s), no_hit (bool), att_speed
ACHIEVEMENTS = [
    Achievement("first_blood", "Premier sang", "Detruire 1 ennemi", 100,
                lambda s: s["kills"] >= 1),
    Achievement("hunter", "Chasseur", "Detruire 100 ennemis", 500,
                lambda s: s["kills"] >= 100),
    Achievement("exterminator", "Exterminateur", "Detruire 1000 ennemis", 2000,
                lambda s: s["kills"] >= 1000),
    Achievement("boss_slayer", "Tueur de boss", "Vaincre un boss", 1000,
                lambda s: s["bosses"] >= 1),
    Achievement("boss_hunter", "Fleau des boss", "Vaincre 5 boss", 3000,
                lambda s: s["bosses"] >= 5),
    Achievement("score_1000", "Ferrailleur", "1000 debris en une partie", 300,
                lambda s: s["score"] >= 1000),
    Achievement("score_5000", "Recycleur galactique", "5000 debris en une partie", 1500,
                lambda s: s["score"] >= 5000),
    Achievement("untouchable", "Intouchable", "1000 debris sans etre touche", 800,
                lambda s: s["no_hit"] and s["score"] >= 1000),
    Achievement("survivor", "Survivant", "Survivre 3 minutes", 600,
                lambda s: s["game_time"] >= 180),
    Achievement("collector", "Collectionneur", "Ramasser 20 bonus", 400,
                lambda s: s["bonus"] >= 20),
    Achievement("shopper", "Client fidele", "Acheter 5 objets au marche", 300,
                lambda s: s["purchases"] >= 5),
    Achievement("veteran", "Veteran", "Jouer 10 parties", 500,
                lambda s: s["games"] >= 10),
]


class AchievementManager:
    """ This class is used to track which achievements are unlocked. """

    def __init__(self) -> None:
        """ Initialize a new object of AchievementManager class, with nothing unlocked. """
        self.unlocked:set[str] = set()

    def check(self, stats:dict) -> List[Achievement]:
        """
        Unlocks the achievements whose condition is met.

        args:
            stats (dict): current statistics of the player.

        returns:
            list: the achievements unlocked by this call.
        """
        new = [a for a in ACHIEVEMENTS if a.key not in self.unlocked and a.condition(stats)]
        for achievement in new:
            self.unlocked.add(achievement.key)
        return new

    def to_list(self) -> List[str]:
        """ Returns the unlocked achievements, for the save file. """
        return sorted(self.unlocked)

    def load(self, keys:List[str]) -> None:
        """ Restores the unlocked achievements from the save file, unknown keys are ignored. """
        known = {a.key for a in ACHIEVEMENTS}
        self.unlocked = {key for key in keys if key in known}
