#!/usr/bin/env python3
# vim:fileencoding=utf-8
# License: GPL v3 Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>

from contextlib import suppress
import fcntl
import os
import re
import select
import sys
from ..tui.operations import alternate_screen, styled


def main(args):
    if sys.stdin.isatty():
        if '--help' not in args and '-h' not in args:
            print('You must pass the text to be hinted on STDIN', file=sys.stderr)
            input('Press Enter to quit')
            return

    global readline
    import readline as rl
    readline = rl
    from kitty.shell import init_readline

    init_readline(readline)

    sys.stdin = open(os.ctermid())
    term = ""
    with alternate_screen():
        with suppress(KeyboardInterrupt, EOFError):
            term = input("Enter search regex: ")
    if term == "":
        return

    fcntl.fcntl(sys.__stdin__.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    def replace_func(matchobj):
        return styled(matchobj.group(0), bold=True, fg="black", bg="green")

    try:
        while True:
            if select.select([sys.__stdin__], [], [], 0) == ([sys.__stdin__], [], []):
                text = sys.__stdin__.read()
                text =  re.sub(term, replace_func, text, count=0)
                sys.stdout.write(text)
    except KeyboardInterrupt:
        sys.stderr.write("exiting\n")
        pass
    return


def handle_result(args, data, target_window_id, boss):
    print("in handle_result")
    pass


handle_result.type_of_input = 'live-history'


if __name__ == '__main__':
    # Run with kitty +kitten live_demo
    ans = main(sys.argv)
    if ans:
        print(ans)
