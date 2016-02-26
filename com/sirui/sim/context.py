class Context(object):
    context = None
    def __init__(self, field, env):
        # No direct use by user
        self.field = field
        self.atoms = set([])
        self.process = {}
        self.env = env

    @classmethod
    def create(cls, field = None, env=None):
        cls.context = Context(field, env)
        return cls.context

    @classmethod
    def getContext(cls):
        return cls.context

    @classmethod
    def setField(cls, field):
        cls.getContext().field = field

    @classmethod
    def getField(cls):
        return cls.getContext().field

    @classmethod
    def getAtoms(cls):
        return cls.getContext().atoms

    @classmethod
    def addAtom(cls, atom):
        cls.getContext().atoms.add(atom)

    @classmethod
    def removeAtom(cls, atom):
        cls.getContext().atoms.remove(atom)

    @classmethod
    def popAtom(cls, atom):
        cls.getContext().atoms.pop(atom)

    @classmethod
    def addProcess(cls, name, process):
        cls.getContext().process[name] = process

    @classmethod
    def getProcess(cls, name):
        return cls.getContext().process[name]

    @classmethod
    def setEnv(cls, env):
        cls.getContext().env = env

    @classmethod
    def getEnv(cls):
        return cls.getContext().env