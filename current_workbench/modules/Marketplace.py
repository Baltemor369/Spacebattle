class ShopItem:
    """ This class describes an item that can be bought in the Marketplace. """
    def __init__(self, key:str, name:str, description:str, cost:int, max_level:int, consumable:bool) -> None:
        """
        Initialize a new object of ShopItem class.

        args:
            key (str): identifier of the item, used in the save file.
            name (str): name shown to the player.
            description (str): what the item does.
            cost (int): price in Stellor (multiplied by the next level for permanent items).
            max_level (int): maximum level, or maximum stock for consumable items.
            consumable (bool): True if the item is used up during a game.
        """
        self.key = key
        self.name = name
        self.description = description
        self.cost = cost
        self.max_level = max_level
        self.consumable = consumable


class Marketplace:
    """ This class is used to manage the items bought by the player with Stellor. """

    ITEMS = [
        ShopItem("start_shield", "Bouclier de depart", "Bouclier de 5 s au debut de la partie", 300, 3, True),
        ShopItem("second_chance", "Seconde chance", "Revit avec 50 % des PV a la mort", 800, 3, True),
        ShopItem("magnet", "Aimant a bonus", "+4 % de chance de bonus par niveau", 1000, 3, False),
        ShopItem("bonus_time", "Bonus prolonges", "+2 s de duree des bonus par niveau", 800, 3, False),
    ]

    def __init__(self) -> None:
        """ Initialize a new object of Marketplace class, with nothing bought. """
        self.owned = {item.key: 0 for item in Marketplace.ITEMS}

    def level(self, key:str) -> int:
        """ Returns the level (or stock for consumable items) of an item. """
        return self.owned[key]

    def price(self, item:ShopItem) -> int:
        """ Returns the price of the next purchase of an item. """
        if item.consumable:
            return item.cost
        return item.cost * (self.owned[item.key] + 1)

    def is_maxed(self, item:ShopItem) -> bool:
        """ Returns True if the item cannot be bought anymore. """
        return self.owned[item.key] >= item.max_level

    def buy(self, item:ShopItem, stellor:int) -> int:
        """
        Buys an item if possible.

        args:
            item (ShopItem): the item to buy.
            stellor (int): Stellor owned by the player.

        returns:
            int: the price paid, 0 if the item was not bought.
        """
        price = self.price(item)
        if self.is_maxed(item) or stellor < price:
            return 0
        self.owned[item.key] += 1
        return price

    def use(self, key:str) -> bool:
        """
        Uses one consumable item.

        returns:
            bool: True if the player had one.
        """
        if self.owned[key] > 0:
            self.owned[key] -= 1
            return True
        return False

    def to_dict(self) -> dict:
        """ Returns the owned items, for the save file. """
        return dict(self.owned)

    def load(self, data:dict) -> None:
        """ Restores the owned items from the save file, unknown keys are ignored. """
        for item in Marketplace.ITEMS:
            self.owned[item.key] = max(0, min(item.max_level, int(data.get(item.key, 0))))
