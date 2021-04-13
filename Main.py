import logging
from KeyListener import Listener

DEBUG = True

def setup_logger():
    log_level = logging.DEBUG if DEBUG else logging.ERROR
    logging.basicConfig(format="[%(levelname)s] %(message)s (%(module)s)", level=log_level)


if __name__ == '__main__':
    setup_logger()

    listener = Listener()
    listener.listen()
