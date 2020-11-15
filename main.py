import time
import curses
from csvinterface import verbreturns
import fuzzy as fzf
import csvinterface

global collections
collections = csvinterface.verbreturns()
# print(len(collections))
def main(stdscr, text: str, ind: int) -> str:
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.clear()
    curses.cbreak()
    tempcount = 2
    stdscr.addstr(text)
    halt = False
    while True:
        c = stdscr.getch()

        if c == 263:
            curses.flushinp()
            stdscr.clear()
            break

        if c == 258:
            ind += 1
            curses.flushinp()
            stdscr.clear()
            break

        if c == 259 and ind >= -1:
            ind -= 1
            curses.flushinp()
            stdscr.clear()
            break

        if c == 261:
            halt = True
            curses.flushinp()
            stdscr.clear()
            break

        if tempcount == 2:
            x = fzf.fuzzyfinder(text, collection=collections)
            for val in x:
                try:
                    if ind == x.index(val):
                        stdscr.addstr("\n>" + val)
                    else:
                        stdscr.addstr("\n" + val)
                except:
                    break
            tempcount = 0

        elif c != -1:
            text += str(chr(c))
            tempcount = 1

        if tempcount == 1:
            stdscr.clear()
            stdscr.addstr(text)
            for val in fzf.fuzzyfinder(text, collection=collections):
                try:
                    stdscr.addstr("\n" + val)
                except:
                    break
            tempcount = 0
        time.sleep(0.1)
    return text, ind, halt


global text
text = ""
ind2 = -1
halt = False
while True:
    try:
        text, ind, halt = curses.wrapper(main, text, ind2)
        if ind2 != ind:
            text = text
        if halt == True:
            break
        elif ind2 == ind:
            text = text[:-1]
        ind2 = ind
    except KeyboardInterrupt:
        break

x = fzf.fuzzyfinder(text, collections)
try:
    print(x[ind])
except:
    pass
