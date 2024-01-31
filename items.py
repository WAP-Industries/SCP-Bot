from utils import *

class Item:
    def __init__(self, name: str=None, repr: str=None, callback: Utils.Function=None):
        self.Name = name
        self.Repr = repr or "⍰"
        self.Callback = callback

    class Callbacks:
        @staticmethod
        def Beer(player):
            pass

        @staticmethod
        def Saw(player):
            pass

        @staticmethod
        def Cigarette(player):
            player.Health+=1

        @staticmethod
        def MagnifyingGlass(player):
            pass

        @staticmethod
        def Handcuffs(player):
            pass


Items = [
    # Item("Beer", "🍺", Item.Callbacks.Beer),
    # Item("Hand Saw", "🪚", Item.Callbacks.Saw),
    Item("Cigarette", "🚬", Item.Callbacks.Cigarette),
    # Item("Magnifying Glass", "🔍", Item.Callbacks.MagnifyingGlass),
    # Item("Handcuffs", "🔗", Item.Callbacks.Handcuffs)
]