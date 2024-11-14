import json

class DeckConf:
    def __init__(self, card_dict):
        self.card_dict = card_dict # card dict : list of dict = [ {"name": name , "quantity": 1}, ...]

def loadDeck():
    url = "./cards/decks.json"
    deck_conf = {}
    with open(url) as jsonData:
        data = json.load(jsonData)
        for deck_type in data:
            deck_conf[deck_type] = DeckConf(data[deck_type])
    
    return deck_conf

DECK_DEFS = loadDeck()

    