import textwrap
import curses
import sys

menu = ["Normal Input", "Upload File", "About", "Exit"]

def draw_frame(stdscr, title, h, w):
    stdscr.addstr(0, 0, "╔" + "═"*(w-2) + "╗")
    stdscr.addstr(1, 0, title.center(w))
    stdscr.addstr(1, 0, "║")
    stdscr.addstr(1, w-1, "║")
    stdscr.addstr(2, 0, "╠" + "═"*(w-2) + "╣")
    
    for y in range(3,h+3):
        stdscr.addstr(y, 0, "║")
        stdscr.addstr(y, w-1, "║")

    stdscr.addstr(h+3, 0, "╚" + "═"*(w-2) + "╝")

def process_string(s):
    s = s.strip().replace(" ", "")
    if not s:
        return "Empty string detected"
    if all(c in ('0', '1') for c in s):
        return "Accepted" if s.count('0') % 2 else "Not Accepted"
    else:
        return "Please input a string containing only 0s and 1s"

def get_color(result):
    if result == "Accepted":
        return curses.color_pair(1) | curses.A_BOLD
    elif result == "Not Accepted":
        return curses.color_pair(2) | curses.A_BOLD
    else:
        return curses.color_pair(3)

def upload(stdscr, title="Upload File"):
    try:
        longest = 0
        files = []
        h = 0
        while True:
            w = max(54, longest)
            i = 0
            stdscr.clear()

            with open("upload_input_ins.txt", "r") as file:
                i = 3
                for line in file:
                    if line == "\n":
                        i += 1
                        continue

                    splitted_text = textwrap.wrap("• " + line, width=(w-4))
                    for t in splitted_text:
                        stdscr.addstr(i, 2, t)
                        i += 1

            draw_frame(stdscr, title, len(files)+h+(i-2), w)
            h = 1

            for file in files:
                stdscr.addstr(i, 2, "Enter the filename: " + file)
                try:
                    with open(file, "r") as fn:
                        for line in fn:
                            if line.isspace():
                                continue
                            i += 1
                            h += 1
                            l = line.strip().replace(" ", "")
                            x = process_string(l)
                            longest = max(longest, len(f"  {l}: {x}")+4)

                            stdscr.addstr(i, 2, "  " + l + ": " + x, get_color(x))
                    i -= 1

                except FileNotFoundError:
                    if file.isspace():
                        stdscr.addstr(i+1, 2, "  Please input a non-empty string")
                    else:
                        stdscr.addstr(i+1, 2, "  File not found")
                    h += 1

                i += 2

            curses.echo()
            curses.curs_set(1)
            stdscr.addstr(i, 2, "Enter the filename: ")
            fn = stdscr.getstr(i, len("Enter the filename: ") + 2).decode("utf-8")
            curses.curs_set(0)
            curses.noecho()
            stdscr.refresh()

            key = fn.lower().strip().replace(" ", "")

            if key == "menu":
                return
            elif key == "exit":
                exit(stdscr)
            elif key == "clear":
                longest = 0
                files.clear()
                h = 0
            else:
                files.append(fn)
                try:
                    with open(fn, "r") as file:
                        for line in file:
                            if line.isspace():
                                continue
                            i += 1
                            h += 1
                            l = line.strip().replace(" ", "")
                            x = process_string(l)
                            longest = max(longest, len(f"  {l}: {x}")+4)

                    i -= 2
                    h -= 1
                except FileNotFoundError:
                    pass

    except curses.error:
        stdscr.clear()
        draw_frame(stdscr, "Error", 1, 54)
        stdscr.addstr(3,2, "Error: Terminal window is too small")
        stdscr.getch()
        upload(stdscr, title)

def exit(stdscr, title="Exit"):
    stdscr.clear()
    draw_frame(stdscr, title, 1, 54)
    stdscr.addstr(3, 2, "Thank you for using our program!")
    stdscr.getch()
    sys.exit()

def normal(stdscr, title):
    try:
        inputs = []

        while True:
            try:
                w = max(54, len(max(inputs, key=len))+20)
            except:
                w = 54

            h = (len(inputs))*2
            i = 0
            stdscr.clear()

            with open("normal_input_ins.txt", "r") as file:
                i = 3
                for line in file:
                    if line == "\n":
                        i += 1
                        continue

                    splitted_text = textwrap.wrap("• " + line, width=(w-4))
                    for t in splitted_text:
                        stdscr.addstr(i, 2, t)
                        i += 1

            draw_frame(stdscr, title, h+(i-2), w)

            for inp in inputs:
                result = process_string(inp)
                stdscr.addstr(i, 2, "Enter a string: ")
                stdscr.addstr(inp, get_color(result))
                stdscr.addstr(i+1, 2, "  "+result, get_color(result))
                i += 2

            curses.echo()
            curses.curs_set(1)
            stdscr.addstr(i, 2, "Enter a string: ")
            s = stdscr.getstr(i, len("Enter a string: ") + 2).decode("utf-8")
            curses.curs_set(0)
            curses.noecho()
            stdscr.refresh()

            key = s.lower().strip().replace(" ", "")

            if key == "menu":
                return
            elif key == "exit":
                exit(stdscr)
            elif key == "clear":
                inputs.clear()
            else:
                inputs.append(s)

    except curses.error:
        stdscr.clear()
        draw_frame(stdscr, "Error", 1, 54)
        stdscr.addstr(3,2, "Error: Terminal window is too small")
        stdscr.getch()
        upload(stdscr, title)

def about(stdscr, title):
    while True:
        h, w = 12, 54
        with open("about.txt", "r") as file:
            y = 3
            for line in file:
                if line == "\n":
                    y += 1
                    continue

                splitted_text = textwrap.wrap(line, width=(w-4))
                for t in splitted_text:
                    stdscr.addstr(y, 2, t)
                    y += 1

        stdscr.addstr(y+1, 0, "Press any key to return to Main Menu".center(w-4), curses.color_pair(1) | curses.A_BOLD)
        draw_frame(stdscr, title, y, w)
        stdscr.refresh()

        stdscr.getch()
        return

def main(stdscr):
    curses.curs_set(0)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)

    curr = 0

    while True:
        stdscr.clear()
        h, w = len(menu), 30

        for i, item in enumerate(menu):
            if curr == i:
                stdscr.addstr(i+3, 2, f"► {item}", curses.color_pair(1))
            else:
                stdscr.addstr(i+3, 2, item)

        draw_frame(stdscr, "0dd - Main Menu", h, w)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            curr = (curr-1) % h
        elif key == curses.KEY_DOWN:
            curr = (curr+1) % h
        elif key in (10, 13):
            selected = menu[curr]
            stdscr.clear()
            stdscr.refresh()

            if selected == "Normal Input":
                normal(stdscr, selected)
            elif selected == "Upload File":
                upload(stdscr)
            elif selected == "About":
                about(stdscr, selected+" 0dd")
            elif selected == "Exit":
                exit(stdscr)

curses.wrapper(main)

