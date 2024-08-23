import sqlite3
import curses


def fetch_records(db_name):
    """Fetch all records from the database."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM santa_list")
    rows = c.fetchall()
    conn.close()
    return rows


def truncate_text(text, width):
    """Truncate text to fit within the given width."""
    return text if len(text) <= width else text[:width - 3] + '...'


def display_record_details(stdscr, record):
    """Display detailed view of a single record."""
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    details = [
        f"ID: {record[0]}",
        f"Name: {record[1]}",
        f"Age: {record[2]}",
        f"Date of Birth: {record[3]}",
        f"Location: {record[4]}",
        f"Reason: {record[5]}"
    ]

    for idx, detail in enumerate(details):
        stdscr.addstr(idx + 1, 0, truncate_text(detail, w))

    stdscr.addstr(h - 2, 0, "Press 'Enter' or 'Esc' to go back to the list.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_ENTER, 10, 13, 27]:  # Enter or Esc key
            break


def display_records(stdscr, records):
    """Display the records in a scrollable list with highlighting."""
    curses.curs_set(0)  # Hide the cursor
    h, w = stdscr.getmaxyx()  # Get the height and width of the window

    max_y = len(records)
    current_row = 0
    start_row = 0  # Start of the visible window

    while True:
        stdscr.clear()

        for idx in range(min(h - 2, max_y)):  # Adjust display to terminal height
            record_idx = start_row + idx
            if record_idx >= max_y:
                break
            record = records[record_idx]
            record_text = f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Location: {record[4]}, Reason: {record[5]}"
            record_text = truncate_text(record_text, w)  # Truncate the text to fit within the window width
            if record_idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 1, 0, record_text)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 1, 0, record_text)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
                if current_row < start_row:
                    start_row -= 1

        elif key == curses.KEY_DOWN:
            if current_row < max_y - 1:
                current_row += 1
                if current_row >= start_row + (h - 2):
                    start_row += 1

        elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key to view details
            display_record_details(stdscr, records[current_row])

        elif key == ord('q'):
            break


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Set up color pair for highlighting

    db_name = "santa_naughty_nice_list.db"  # Replace with your database file name
    records = fetch_records(db_name)

    display_records(stdscr, records)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error as e:
        print("Error initializing curses: ", str(e))
        print("Try resizing your terminal or running the script from a standard terminal environment.")
