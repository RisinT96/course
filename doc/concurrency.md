# Concurrency

---

## Exercise - CPU-bound example

Find all the prime numbers until 'end' in a given amount of 'threads'.

    !python
    >>> list(calc_primes(end=50, threads=5))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

For each stage, run it on a multi-code CPU and measure the performance gain when using 5 workers vs 1 worker.

1) Use `threading.Thread`. Save your work. Try running with end=5000 and killing the the threads with Ctrl+C while they're running? Did it work?

2) Use `multiprocessing.dummy.Pool`.

3) Use `multiprocessing.Pool`.

What did you notice?

---

## Exercise - solution

    !python
    from multiprocessing import Pool

    def is_prime(n):
        if n == 1: # 1 is special
            return False

        divisors = range(2, (n // 2) + 1)
        return all(n % d != 0 for d in divisors)

    def calc_primes_pool(end, num_processes):
        p = Pool(num_processes)

        results = []
        for i in range(end):
            result = p.apply_async(is_prime, (i,))
            results.append((i, result))

        for i, result in results:
            if result.get():
                yield i

---

## The GIL

For CPU-bound tasks, Python threads don't offer a speedup.

Watch "Python's Infamous GIL" [https://www.youtube.com/watch?v=KVKufdTphKs](https://www.youtube.com/watch?v=KVKufdTphKs)

Watch "Gilectomy" [https://www.youtube.com/watch?v=P3AyI_u66Bw](https://www.youtube.com/watch?v=P3AyI_u66Bw)

---

## I/O-bound concurrency

Let's say we want to write a TCP server that counts the number of connection
attempts, and writes it back to the client.

    $ netcat localhost 5000
    <1, took 24.6 ms>

    $ netcat localhost 5000
    <2, took 14.8 ms>

    $ netcat localhost 5000
    <3, took 15.5 ms>

    $ netcat localhost 5000
    <4, took 15.9 ms>

    $ netcat localhost 5000
    <5, took 19.0 ms>

---

### Naive implementation

    !python

    # I'd have written this using the built in socketserver module

    import socket

    class Server(object):
        def __init__(self):
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.s.bind(('localhost', 5000))
            self.s.listen(10)
            self.n = 0

        def run(self):
            while True:
                conn, peer = self.s.accept()
                self.handle(conn, peer)

        def handle(self, conn, peer):
            tmp = self.n
            t = time.time()
            for i in xrange(1000000):
                pass  # simulate request processing
            dt = time.time() - t
            self.n = tmp + 1
            conn.sendall('<{0}, took {1:.1f} ms>\n'.format(self.n, dt*1e3))

---

### Naive threaded implementation

    !python

    # I'd have written this using the built in socketserver module,
    # and its ThreadingMixIn class.

    import socket, threading

    class Server(object):
        def __init__(self):
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.s.bind(('localhost', 5000))
            self.s.listen(10)
            self.n = 0

        def run(self):
            while True:
                conn, peer = self.s.accept()
                t = threading.Thread(target=self.handle, args=(conn, peer))
                t.start()

        def handle(self, conn, peer):
            tmp = self.n
            t = time.time()
            for i in xrange(1000000):
                pass  # simulate request processing
            dt = time.time() - t
            self.n = tmp + 1
            conn.sendall('<{0}, took {1:.1f} ms>\n'.format(self.n, dt*1e3))

---

## Let's test it!

    !bash
    $ nc localhost 5000
    <1, took 17.8 ms>

    $ nc localhost 5000
    <2, took 17.5 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &);
    <3, took 62.8 ms>
    <3, took 61.3 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &);
    <4, took 66.1 ms>
    <4, took 64.4 ms>

    $ (nc localhost 5000 &); (nc localhost 5000 &); (nc localhost 5000 &);
    <5, took 105.6 ms>
    <5, took 111.5 ms>
    <5, took 110.3 ms>

    $ nc localhost 5000
    <6, took 17.4 ms>

---

## Discussion

We need to make sure that `self.n` is updated **atomically**,
otherwise there's a race condition.

We have to **synchronize** all accesses to shared memory between threads,
using e.g. `threading.Lock` objects,
because we cannot tell when the threads will be scheduled to run.

Can we have something better?

We would like most of our code to run atomically, but to be able to yield control to
other tasks, when we allow it to.

This is called "cooperative multitasking", and the tasks (that use cooperation
to achieve concurrency) are also called "green threads" or "greenlets". This concept is not unique to Python!

Since Python currently does not support CPU-bound concurrency, we would like
our tasks to cooperate around I/O events.

Can we have **atomicity** on CPU access, but **cooperation** around I/O events?

---

## Yes, we can!

This is exactly what `gevent` ([https://pypi.org/project/gevent/](https://pypi.org/project/gevent/)) library provides us.

    !python
    >>> from gevent import socket
    >>> def request(addr):
    ...     s = socket.create_connection(('localhost', 5000))
    ...     return s.recv(1024)

    >>> addr = ('localhost', 5000)
    >>> request(addr)
    '<10, took 20.1 ms>'

    >>> request(addr)
    '<11, took 18.3 ms>'

    >>> request(addr)
    '<12, took 20.3 ms>'

---

## Concurrent requests

    !python
    >>> f1 = gevent.spawn(request, addr)
    >>> f2 = gevent.spawn(request, addr)
    >>> f3 = gevent.spawn(request, addr)
    >>> f1.get()
    '<13, took 103.6 ms>'
    >>> f2.get()
    '<13, took 110.2 ms>'
    >>> f3.get()
    '<13, took 111.5 ms>'

This is actual concurrent execution, reproducing our race condition :)

---

## Exceptions

`.get()` method raises an error if its greenlet failed with exception:

    >>> f = gevent.spawn(request, ('1.2.3.4', 5678))
    >>> f.get()
    Traceback (most recent call last):
      File "/usr/local/lib/python2.7/dist-packages/gevent/greenlet.py", line 327, in run
        result = self._run(*self.args, **self.kwargs)
      File "<stdin>", line 2, in request
      File "/usr/local/lib/python2.7/dist-packages/gevent/socket.py", line 591, in create_connection
        raise err
    error: [Errno 111] Connection refused
    <Greenlet at 0x7f2c3344bc30: request(1)> failed with error

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/usr/local/lib/python2.7/dist-packages/gevent/greenlet.py", line 274, in get
        raise self._exception
    socket.error: [Errno 111] Connection refused


It's much better than the default thread behaviour.

---

## gevent-based server

    !python
    class Server(object):

        def __init__(self):
            addr = ('localhost', 5001)
            self.s = gevent.server.StreamServer(addr, self.handle)
            self.n = 0

        def run(self):
            self.s.serve_forever()

        def handle(self, conn, peer):
            self.n = self.n + 1
            conn.sendall('<{0}>\n'.format(self.n))
            conn.close()
---

## How Does Gevent work?

Watch [https://pyvideo.org/pycon-us-2016/kavya-joshi-a-tale-of-concurrency-through-creativity-in-python-a-deep-dive-into-how-gevent-works.html](https://pyvideo.org/pycon-us-2016/kavya-joshi-a-tale-of-concurrency-through-creativity-in-python-a-deep-dive-into-how-gevent-works.html)

---

## Monkey Patching

Note we have to use gevent alternatives for every function that releases execution to the OS: gevent.sleep, gevent.socket, ...

If a greenlet accidentally calls time.sleep instead of gevent.sleep, the whole application sleep, not just that greenlet.
This is hard to catch, and causes significant performance problems.

It is similar to sleeping with a lock, because it's really sleeping with a lock - the GIL!

What if I call third-party code that call `time.sleep`?

Monkey patching replaces the standard non-gevent modules and function with their gevent implementations.
Better than littering your code with explicit import to gevent code, in my opinion. Others disagree.

What happens if the call to `time.sleep` happens before we perform monkey patching?

Monkey patching should be the first thing to happen in the app.

---

## The async and await keywords

Greenlets, like threads, yield control implicitly.

The `async` and `await` keywords enable explicit cooperative multitasking.

None of the main libraries make use of this syntax at this time (Django, Flask, ...). Their APIs are very stable so integrating use of the keywords will take time.

Watch [https://www.youtube.com/watch?v=BI0asZuqFXM](https://www.youtube.com/watch?v=BI0asZuqFXM)

---

## thredo

Ever tried to cancel a thread while it's working? Ctrl+C isn't always helpful.

Written by David Beazley ([github.com/dabeaz/thredo](https://github.com/dabeaz/thredo)):

    !python
    import thredo

    def worker(q):
        while True:
            item = q.get()
            if item is None:
                break
            print('Got:', item)

    def main():
        q = thredo.Queue()
        t = thredo.spawn(worker, q)
        for n in range(10):
            q.put(n)
            thredo.sleep(1)
        q.put(None)
        t.join()

    thredo.run(main)

Watch [https://www.youtube.com/watch?v=xOyJiN3yGfU](https://www.youtube.com/watch?v=xOyJiN3yGfU)

It utilizes the new `async` and `await` keywords, like Beazley's `curio` module ([github.com/dabeaz/curio](https://github.com/dabeaz/curio)).
