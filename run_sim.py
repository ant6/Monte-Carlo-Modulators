import sys

from mcm.main import run_sim

if __name__ == '__main__':
    try:
        run_sim(*sys.argv[1:])
    except KeyboardInterrupt:
        print('\nExiting...', file=sys.stderr)
