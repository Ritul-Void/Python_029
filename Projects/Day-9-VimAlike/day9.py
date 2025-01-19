import curses
import sys

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    filename = sys.argv[1] if len(sys.argv) > 1 else "output.txt"

    # Load file if exists
    try:
        with open(filename, "r", encoding="utf-8") as f:
            buffer = f.read().splitlines()
        if not buffer:
            buffer = [""]
    except FileNotFoundError:
        buffer = [""]

    row, col = 0, 0
    command_mode = False
    command = ""
    BACKSPACE_KEYS = (curses.KEY_BACKSPACE, 127, 8)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Draw text
        for i, line in enumerate(buffer[:h-1]):
            stdscr.addstr(i, 0, line[:w-1])

        # Status / command line
        if command_mode:
            status = ":" + command
        else:
            status = f"{filename}  |  :w save  :q quit  :wq save+quit"

        stdscr.addstr(h-1, 0, status[:w-1])

        # Cursor
        if command_mode:
            stdscr.move(h-1, len(command)+1)
        else:
            stdscr.move(row, col)

        stdscr.refresh()
        key = stdscr.getch()

        # ---------- COMMAND MODE ----------
        if command_mode:
            if key in (10, curses.KEY_ENTER):  # Enter
                if command == "w":
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("\n".join(buffer))
                elif command == "q":
                    break
                elif command == "wq":
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("\n".join(buffer))
                    break
                command = ""
                command_mode = False

            elif key in (27,):  # ESC
                command = ""
                command_mode = False

            elif key in BACKSPACE_KEYS:
                command = command[:-1]

            elif 32 <= key <= 126:
                command += chr(key)

            continue

        # ---------- NORMAL EDIT MODE ----------
        if key == ord(":"):
            command_mode = True
            command = ""

        elif key == curses.KEY_LEFT and col > 0:
            col -= 1

        elif key == curses.KEY_RIGHT and col < len(buffer[row]):
            col += 1

        elif key == curses.KEY_UP and row > 0:
            row -= 1
            col = min(col, len(buffer[row]))

        elif key == curses.KEY_DOWN and row < len(buffer) - 1:
            row += 1
            col = min(col, len(buffer[row]))

        elif key in (10, curses.KEY_ENTER):
            buffer.insert(row + 1, buffer[row][col:])
            buffer[row] = buffer[row][:col]
            row += 1
            col = 0

        elif key in BACKSPACE_KEYS:
            if col > 0:
                buffer[row] = buffer[row][:col-1] + buffer[row][col:]
                col -= 1
            elif row > 0:
                col = len(buffer[row-1])
                buffer[row-1] += buffer[row]
                buffer.pop(row)
                row -= 1

        elif 32 <= key <= 126:
            buffer[row] = buffer[row][:col] + chr(key) + buffer[row][col:]
            col += 1

curses.wrapper(main)
