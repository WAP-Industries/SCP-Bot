from utils import *
import emoji

class Item:
    def __init__(self, name: str=None, repr: str=None, callback: Utils.Function=None):
        self.Name = name
        self.Repr = emoji.emojize(f":{repr}:") if repr else "⍰"
        self.Callback = callback


Items = [
    Item("Beer", "beer", lambda: 0),
    Item("Saw", "carpentry_saw", lambda: 0)
]