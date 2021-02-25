from .EventPile import EventPile


class EventManager:
    def __init__(self):
        self.piles = {}

    def on(self, event, callback):
        if event in self.piles:
            pile = self.piles[event]
        else:
            pile = EventPile(event)
            self.piles[event] = pile

        return pile.on(callback)

    def emit(self, event, **config):
        for pile in tuple(self.piles.values()):
            if pile.match(event):
                pile.emit(event=event, **config)
