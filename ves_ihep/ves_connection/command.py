import os
import sys
import getopt
import traceback
import pexpect


def exit_with_usage():
    print globals()['__doc__']
    os.__exit(1)


def main():
    try:
        optlist, args = getopt.getopt(
            sys.argv[
                1:], 'h?ac:', [
                'help', 'h', '?'])
    finally:
        pass
