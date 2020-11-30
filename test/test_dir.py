import os
import sys


os.chdir(os.path.dirname(sys.argv[0]))

if __name__ == '__main__':
    print()
    print(os.popen('pwd').read())
