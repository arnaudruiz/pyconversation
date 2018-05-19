


class Slot(object):

    def __init__(self):
        self.name = None

    def parse(self, metadata):
        self._name = metadata["name"] if "name" in metadata else None
        self.constraint = metadata["slotConstraint"] if "slotConstraint" in metadata else 'Optional'
        self._type = metadata["slotType"] if "slotType" in metadata else None
        self.priority = metadata["priority"] if "priority" in metadata else None
        self.sampleUtterances = metadata["sampleUtterances"] if "sampleUtterances" in metadata else []
        self.ellicitationPrompt = metadata["valueElicitationPrompt"] if "valueElicitationPrompt" in metadata else None
        return self
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def ellicitation_msg(self):
        return self.ellicitationPrompt

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def elicitationRequired(self):
        if hasattr(self, "constraint"):
            if self.constraint == 'Required':
                return True
            else:
                return False
        else:
            return False

    @property
    def value(self):
        if hasattr(self,"_value"):
            return self._value
        else:
            return None

    @value.setter
    def value(self, val):
        self._value = val

class SlotType(object):

    def __init__(self, name):
         self.name = name