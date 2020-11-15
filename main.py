import time
import curses
from csvinterface import verbreturns
import fuzzy as fzf
import csvinterface

global collections
collections = csvinterface.verbreturns()

print(len(collections))


def clearbreak(stdscr):
    curses.flushinp()
    stdscr.clear()
    return 1


def main(stdscr, text: str, ind: int) -> str:
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.clear()
    curses.cbreak()
    tempcount = 2
    stdscr.addstr(text)
    halt = False

    while not halt:
        c = stdscr.getch()

        if c == 263:
            clearbreak(stdscr)
            break

        if c == 258:
            ind += clearbreak(stdscr)
            break

        if c == 259 and ind >= -1:
            ind -= clearbreak(stdscr)
            break

        if c == 261:
            halt = bool(clearbreak(stdscr))
            break

        if tempcount == 2:
            x = fzf.fuzzyfinder(text, collection=collections)
            for val in x:
                try:
                    if ind == x.index(val):
                        stdscr.addstr("\n->" + val, curses.color_pair(3))
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
            if ind == -1:
                stdscr.addstr(text, curses.color_pair(3))
            else:
                stdscr.addstr(text)

            for val in fzf.fuzzyfinder(text, collection=collections):
                try:
                    stdscr.addstr("\n" + val)
                except:
                    break
            tempcount = 0

        time.sleep(0.05)
    return text, ind, halt


global text
text = ""
ind2 = -1
halt = False
while not halt:
    try:
        text, ind, halt = curses.wrapper(main, text, ind2)
        if ind2 != ind:
            text = text
        elif ind2 == ind:
            text = text[:-1]
        ind2 = ind
    except KeyboardInterrupt:
        break

x = fzf.fuzzyfinder(text, collections)
try:
    print("You chose: " + str(x[ind]))
except:
    pass

z = str(x[ind])
from PyDictionary import PyDictionary

try:
    dictionary = PyDictionary(z)
    print(dictionary.printMeanings())
except:
    print("Definition not found")
