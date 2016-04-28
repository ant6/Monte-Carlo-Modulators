import sys

from mcm.main import run_sim

if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_sim(sys.argv[1])
    else:
        run_sim()
