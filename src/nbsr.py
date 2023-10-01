"""
    The NBSR module defines a Non-blocking stream reader (NBSR class).

    In short, the Minecraft stdout is a stream of data that doesn't end until
    the server shuts down. Traditionally, Python would not run any code until
    the server has shut down and returns its entire output.

    The NBSR class allows us to read from the stream without blocking the entire
    Python script. We will occasionally ask the NBSR for any updates, and it
    will give us the latest output, if it exists.
"""

from threading import Thread
from queue import Queue, Empty

class NonBlockingStreamReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass