# =========================================
# C1 - Thread-Safe Singleton Logger
# =========================================

import threading
from datetime import datetime


class Logger:
    _instance = None
    _lock = threading.Lock()   # used to make singleton thread-safe

    def __new__(cls):
        # Double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{time}] {message}")


# ------------- Test ----------------
def worker(name):
    logger = Logger()
    logger.log(f"Message from {name}")
    print("Logger object id:", id(logger))


if __name__ == "__main__":

    # Simulate multiple threads
    t1 = threading.Thread(target=worker, args=("Thread-1",))
    t2 = threading.Thread(target=worker, args=("Thread-2",))
    t3 = threading.Thread(target=worker, args=("Thread-3",))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
