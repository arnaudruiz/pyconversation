
from .slot import Slot

class Intent(object):
    def __init__ (self):
        self.name = None
        self._introMsg = None
        self.sampleUtterances = []

    def parse(self, metadata):
        self.name = metadata["name"]
        if "introMsg" in metadata:
            self.intro = metadata["introMsg"]
        self.sampleUtterances = metadata["sampleUtterances"]  
        if "slots" in metadata:
            parsedSlots = []
            for slot in metadata["slots"]:
                parsedSlots.append(Slot().parse(slot))
            self.slots = parsedSlots
        return self

    @property
    def intro(self):
        return self._introMsg

    @intro.setter
    def intro(self, value):
        self._introMsg = value

    @property
    def slots(self):
        if not hasattr(self, "_slots"):
            self._slots = []
        return self._slots

    @slots.setter
    def slots(self, value):
        self._slots = value

    @property
    def hasSlots(self):
        if not hasattr(self, "slots"):
            return False
        elif len(self.slots) == 0:
            return False
        else: 
            return True