import os
import sys
from pathlib import Path

class RedirectAllStdout:

    '''

    A utility to redirect stdout to a file while within a 'with' statement.

    contextlib.stdout_redirected supports this to some extent, but does not suppress forked processes
    sharing the same stdout stream as the main program (such as blender rendering)

    '''

    def __init__(self, path):
        self.path = Path(path)
        self.path.touch()
            

    def __enter__(self):
        self.orig_output_stream = os.dup(1)
        os.close(1)
        os.open(self.path, os.O_WRONLY)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout.flush()
        os.close(1)
        os.dup(self.orig_output_stream)
        os.close(self.orig_output_stream)

