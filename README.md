Santa's security elves have been building a bit of a surveillance apparatus in his workshop. No big deal, as long as the
congress doesn't find out. But before some whistleblower rats us out, let's use Santa's CRUD app to manage his naughty and
nice list, and maybe edit ourselves into getting some presents before he wakes up from his milk-and-cookies induced stupor.

    Scrollable List: Browse through a list of records in a scrollable interface.
    Detailed View: View detailed information for each record, including personal details and behavioral traits.
    Search Functionality: Search through records by name, location, reason, or status using a built-in search box.
    Editing: Edit any record directly from the interface and save changes easily.
    Add New Records: Add new entries to the list with all necessary details.
    Delete Records: Remove records from the list when needed.
    Navigation: Use intuitive keyboard shortcuts to navigate through the application.

Screenshots

Setup Instructions
Prerequisites

Before running the Santa's Naughty and Nice List Viewer, make sure you have the following installed:

    Python 3.x: The program is built using Python, so you need Python 3.x installed on your machine.
    SQLite3: The application uses SQLite for managing records, which is included with Python by default.
    curses library: This library is required to create the terminal-based UI. It’s included with Python on Unix-based systems (Linux, macOS), but on Windows, you may need to install the windows-curses package.

Installation

    Clone the Repository:

    bash

git clone https://github.com/yourusername/santas-naughty-nice-list.git
cd santas-naughty-nice-list

Install Dependencies:

If you're on Windows, you need to install windows-curses:

bash

pip install windows-curses

For Unix-based systems, the required curses package should already be available.

Setup the Database:

Create a new SQLite database or use the provided sample database. If creating a new one, ensure it has the required schema:

sql

CREATE TABLE santa_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    dob TEXT,
    location TEXT,
    reason TEXT,
    status TEXT,
    ip_phone TEXT,
    ip_pc TEXT,
    gps_data TEXT,
    last_searches TEXT,
    tooth_brushing TEXT,
    favorite_tv_show TEXT,
    socks_lost INTEGER,
    social_media_hours INTEGER,
    frequented_website TEXT,
    browser_info TEXT
);

If you're using the provided sample database, simply copy it to the project directory:

bash

cp path_to_sample_database/santa_naughty_nice_list.db .

Run the Application:

Start the application by running the following command:

bash

    python3 main.py

    (Replace main.py with the actual file name of your script if different.)

Usage
Navigating the List

    UP/DOWN Arrows: Scroll through the list.
    ENTER: View detailed information for the selected record.
    ESC: Return to the main list from any screen.
    'a': Add a new record to the list.
    'f': Open the search box to find specific records.
    'q': Quit the application.

In Detailed View

    LEFT/RIGHT Arrows: Navigate between records.
    'e': Edit the current record.
    'd': Delete the current record.
    ESC: Save changes and return to the list.

Search Functionality

    f: Opens a search box. Type your search query and press Enter to see the results.
    ESC: Cancels the search and returns to the full list.

Contributing

Contributions are welcome! If you have ideas for features, improvements, or bug fixes, feel free to submit an issue or a pull request. Make sure to follow the guidelines below:

    Fork the repository.
    Create a new branch for your feature or bugfix.
    Make your changes and commit them with clear and descriptive messages.
    Submit a pull request, and we'll review it as soon as possible.

License

This project is licensed under the MIT License. See the LICENSE file for details.
