import sys
from os.path import dirname, realpath

sys.path.append(dirname(realpath(__file__)))

__version__ = "1.0.0"

from api import app, start_api

if __name__ == "__main__":
    start_api()
