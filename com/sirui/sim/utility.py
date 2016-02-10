import simpy
from com.sirui.sim.context import Context
class yield_guard:
    def __enter__(self, event, id):
        try:
            yield event
        except simpy.Interrupt as i:
            (reason, info) = i.cause
            if reason == 'Stop':
                Context.removeAtom(self)
                print('Atom %s process terminated' % id)
                return
            else:
                raise ValueError('Unknown interruption! ')

    def __exit__(self, type, value, traceback):
        pass
