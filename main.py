import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

def generate_random_date_of_birth(age):
    """Generate a random date of birth given the age."""
    current_year = datetime.now().year
    birth_year = current_year - age
    start_date = datetime(birth_year, 1, 1)
    end_date = datetime(birth_year, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d')

def generate_reason():
    """Generate a random reason for being on the list."""
    reasons = [
        "Ate all the cookies",
        "Did not share toys",
        "Helped a friend in need",
        "Forgot to brush teeth",
        "Was very polite all year",
        "Left reindeer food out on Christmas Eve",
        "Wrote a letter to Santa",
        "Didn't do homework",
        "Helped with chores",
        "Talked back to parents",
        "Made Christmas cards for everyone",
        "Didn't finish vegetables",
        "Shared a snack with a classmate",
        "Forgot to say please and thank you",
        "Helped decorate the Christmas tree",
        "Made a snowman",
        "Forgot to pick up toys",
        "Was kind to animals",
        "Was caught peeking at presents",
        "Helped wrap gifts for family"
    ]
    return random.choice(reasons)

def create_database(db_name):
    """Create a SQLite database with the Naughty/Nice List."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE santa_list
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  age INTEGER,
                  dob TEXT,
                  location TEXT,
                  reason TEXT)''')

    # Generate random data for 500 children
    fake = Faker()
    locations = [
        "Walla Walla, Washington", "Truth or Consequences, New Mexico", "Intercourse, Pennsylvania",
        "Boring, Oregon", "Santa Claus, Indiana", "Cut and Shoot, Texas", "Why, Arizona",
        "Hell, Michigan", "Booger Hole, West Virginia", "Hot Coffee, Mississippi",
        "Satan's Kingdom, Vermont", "Toad Suck, Arkansas", "Monkey's Eyebrow, Kentucky",
        "Normal, Illinois", "Chicken, Alaska", "Nothing, Arizona", "Embarrass, Minnesota",
        "French Lick, Indiana", "Ding Dong, Texas", "Lizard Lick, North Carolina"
    ]

    for _ in range(500):
        name = fake.name()
        age = random.randint(3, 15)
        dob = generate_random_date_of_birth(age)
        location = random.choice(locations)
        reason = generate_reason()

        # Insert a row of data
        c.execute("INSERT INTO santa_list (name, age, dob, location, reason) VALUES (?, ?, ?, ?, ?)",
                  (name, age, dob, location, reason))

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()

def main():
    db_name = "santa_naughty_nice_list.db"
    create_database(db_name)
    print(f"Database '{db_name}' created with 500 entries.")

if __name__ == "__main__":
    main()
