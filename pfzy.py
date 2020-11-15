import time
import curses
from csvinterface import verbreturns
import fuzzy as fzf
import csvinterface

global collections
collections = csvinterface.verbreturns()
print(len(collections))
time.sleep(5)

def main(stdscr, text:str):
    stdscr.nodelay(True)
    stdscr.clear()
    tempcount = 2
    stdscr.addstr(text)
    while True:
        c = stdscr.getch()
        if c == curses.KEY_BACKSPACE:
            curses.flushinp()
            stdscr.clear()
            break
        
        if tempcount == 2:
            for val in fzf.fuzzyfinder(text, collection = collections):
                try:
                    stdscr.addstr("\n"+val)
                except:
                    break
            tempcount = 0

        if c != -1:
            text += str(chr(c))
            tempcount = 1
        if c == curses.KEY_ENTER:
            stdscr.addstr(text)
            print(text)
        if tempcount == 1:
            stdscr.clear()
            stdscr.addstr(text)
            for val in fzf.fuzzyfinder(text, collection = collections):
                try:
                    stdscr.addstr("\n"+val)
                except:
                    break
            tempcount = 0
        time.sleep(0.1)
    return text

text = ""

while True:
    text = curses.wrapper(main, text)
    text = text[:-1]