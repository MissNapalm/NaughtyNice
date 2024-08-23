import sqlite3
import curses
import traceback

def fetch_records(db_name):
    """Fetch all records from the database."""
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM santa_list")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return []

def truncate_text(text, width):
    """Truncate text to fit within the given width."""
    text = str(text)
    return text if len(text) <= width else text[:width - 3] + '...'

def display_record_details(stdscr, db_name, record):
    """Display detailed view of a single record."""
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
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
        stdscr.addstr(idx + 1, 2, truncate_text(detail, w - 4), curses.color_pair(2))

    stdscr.addstr(h - 3, 2, "Press 'e' to edit, 'd' to delete, 'Enter' or 'Esc' to go back.", curses.A_BOLD)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('e'):  # Edit the record
            edit_record(stdscr, db_name, record)
            return 'edited'
        elif key == ord('d'):  # Delete the record
            confirm = get_user_input(stdscr, "Type 'yes' to confirm deletion: ").lower()
            if confirm == 'yes':
                delete_record(db_name, record[0])
                return 'deleted'  # Signal that the record was deleted
        elif key in [curses.KEY_ENTER, 10, 13, 27]:  # Enter or Esc key
            break

def edit_record(stdscr, db_name, record):
    """Edit a record's details."""
    h, w = stdscr.getmaxyx()
    fields = ["Name", "Age", "Date of Birth", "Location", "Reason"]
    field_keys = ["name", "age", "dob", "location", "reason"]
    record = list(record)  # Convert tuple to list for mutability
    selected_idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, f"Editing Record ID: {record[0]}", curses.A_BOLD | curses.A_UNDERLINE)
        for idx, field in enumerate(fields):
            value = str(record[idx + 1])
            if idx == selected_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 3, 4, f"{field}: {truncate_text(value, w - 10)}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 3, 4, f"{field}: {truncate_text(value, w - 10)}")
        stdscr.addstr(h - 3, 2, "Use UP/DOWN to select, ENTER to edit, ESC to save and exit.", curses.A_BOLD)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(fields) - 1:
            selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13]:  # Enter to edit the selected field
            prompt = f"Enter new value for {fields[selected_idx]} (Current: {record[selected_idx + 1]}): "
            new_value = get_user_input(stdscr, prompt)
            if new_value.strip() != '':
                record[selected_idx + 1] = new_value.strip()
        elif key == 27:  # Esc to save and exit
            update_record(db_name, record)
            break

def get_user_input(stdscr, prompt):
    """Get user input from the terminal."""
    curses.echo()
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2, (w - len(prompt)) // 2, prompt)
    stdscr.refresh()
    input_win = curses.newwin(1, w - 4, (h // 2) + 2, 2)
    curses.curs_set(1)
    user_input = input_win.getstr().decode('utf-8')
    curses.curs_set(0)
    curses.noecho()
    return user_input

def update_record(db_name, record):
    """Update the entire record in the database."""
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""
            UPDATE santa_list 
            SET name = ?, age = ?, dob = ?, location = ?, reason = ?
            WHERE id = ?
            """, (record[1], record[2], record[3], record[4], record[5], record[0]))
        conn.commit()
        conn.close()
    except Exception as e:
        pass  # Handle exception or log error as needed

def delete_record(db_name, record_id):
    """Delete a record from the database."""
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("DELETE FROM santa_list WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        pass  # Handle exception or log error as needed

def add_record(db_name, stdscr):
    """Add a new record to the database."""
    fields = ["Name", "Age", "Date of Birth (YYYY-MM-DD)", "Location", "Reason"]
    new_record = []
    for field in fields:
        value = get_user_input(stdscr, f"Enter {field}: ")
        new_record.append(value.strip())

    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("""
            INSERT INTO santa_list (name, age, dob, location, reason) 
            VALUES (?, ?, ?, ?, ?)
            """, tuple(new_record))
        conn.commit()
        conn.close()
    except Exception as e:
        pass  # Handle exception or log error as needed

def display_records(stdscr, db_name):
    """Display the records in a scrollable list with highlighting."""
    curses.curs_set(0)  # Hide the cursor
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Highlight color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Detail text color
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Footer text color

    records = fetch_records(db_name)
    if not records:
        stdscr.addstr(2, 2, "No records found. Press 'a' to add a new record or 'q' to quit.", curses.A_BOLD)
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == ord('a'):
                add_record(db_name, stdscr)
                records = fetch_records(db_name)
                break
            elif key == ord('q'):
                return

    h, w = stdscr.getmaxyx()
    current_row = 0
    start_row = 0  # Start of the visible window

    while True:
        stdscr.clear()
        stdscr.addstr(1, 2, "Santa's Naughty and Nice List", curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.addstr(2, 2, "-" * (w - 4))

        for idx in range(min(h - 5, len(records))):
            record_idx = start_row + idx
            if record_idx >= len(records):
                break  # Don't write beyond the screen
            record = records[record_idx]
            record_text = f"{record[0]:<3} | {truncate_text(record[1], 20):<20} | {str(record[2]):<3} | {truncate_text(record[4], 15):<15}"
            if record_idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 3, 2, record_text)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 3, 2, record_text)

        stdscr.addstr(h - 2, 2, "Use UP/DOWN to navigate | ENTER to view | 'a' to add | 'q' to quit", curses.color_pair(3))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            if current_row < start_row:
                start_row -= 1

        elif key == curses.KEY_DOWN and current_row < len(records) - 1:
            current_row += 1
            if current_row >= start_row + (h - 5):
                start_row += 1

        elif key in [curses.KEY_ENTER, 10, 13]:
            result = display_record_details(stdscr, db_name, records[current_row])
            if result == 'deleted':
                records = fetch_records(db_name)
                current_row = min(current_row, len(records) - 1)
                if not records:
                    stdscr.clear()
                    stdscr.addstr(h // 2, (w - 20) // 2, "No records remaining.", curses.A_BOLD)
                    stdscr.refresh()
                    curses.napms(2000)
                    break
            elif result == 'edited':
                records = fetch_records(db_name)
        elif key == ord('a'):
            add_record(db_name, stdscr)
            records = fetch_records(db_name)
            current_row = len(records) - 1
        elif key == ord('q'):
            break

def main(stdscr):
    db_name = "santa_naughty_nice_list.db"  # Replace with your database file name
    display_records(stdscr, db_name)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        print("An unexpected error occurred:")
        print(traceback.format_exc())
        print("Ensure your terminal supports curses and try again.")
