import sys

try:
    # Use IPython if available.

    from IPython.Debugger import Pdb
    from IPython.Shell import IPShell
    from IPython import ipapi

    shell = IPShell(argv=[''])

    def pdb_builder():
        return Pdb(ipapi.get().options.colors)

except ImportError:
    from pdb import Pdb
    def pdb_builder():
        return Pdb()



class WTFHandler(object):
    """
    Post-mortem debug handler.

    After an exception, a Pdb debugger will be started in the right frame.

    Instances can be used as a context manager:

        WTF = WTFHandler()

        with WTF:
            raise Something

    Or, can be used as a function call:

        WTF = WTFHandler()

        try:
            raise Something
        except:
            WTF()

    In both cases, the debugger will start on the 'raise Something' line.
    """

    def __init__(self, pdb_builder):
        """
        ``pdb_builder``:
            Called without arguments, this should return the ``pdb.Pdb``
            instance we will use for our debugging.
        """
        self._pdb_builder = pdb_builder

    def _interact(self, traceback):
        p = self._pdb_builder()
        p.reset()
        p.interaction(None, traceback)

    def __call__(self):
        self._interact(sys.exc_info()[2])

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        if traceback:
            self._interact(traceback)



WTF = WTFHandler(pdb_builder)

