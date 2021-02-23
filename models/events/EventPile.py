class EventPile:
    def __init__(self, event):
        self.event = event
        self.callbacks = []

    def emit(self, **config):
        for callback in self.callbacks:
            callback(**config)

    def on(self, callback):
        self.subscribe(callback)
        return lambda: self.unsubscribe(callback)

    def subscribe(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unsubscribe(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def match(self, event):
        if self.event == '*':
            return True

        skeys = self.event.split('/')
        okeys = event.split('/')

        if len(skeys) != len(okeys):
            return False

        for skey, okey in zip(skeys, okeys):
            if skey == '*':
                continue
            if skey == okey:
                continue
            return False

        return True
