import sys
import logging

from . import Agify, AgifyException

logging.basicConfig(level=logging.WARN)

exit_code = 0
age_guess = Agify()

for line in sys.stdin:
    name = line.strip()
    try:
        data = age_guess.get_one(name)
        print("{data[name]}: {data[age]}".format(data=data))
    except AgifyException:
        exit_code = 1
        logging.exception("Failed to get age from %s", name)

exit(exit_code)
