import sqlite3

# below is only used if you have made an error in your database
# conn = sqlite3.connect('employee.db')
# c = conn.cursor()
# c.execute("DROP TABLE IF EXISTS memories")
# c.execute("DROP TABLE IF EXISTS reminders")
# c.execute("DROP TABLE IF EXISTS email")
# c.execute("DROP TABLE IF EXISTS opening")
# conn.commit()
# conn.close()

def insert_memory(memory, year, month, day, hour, image_path = None, reminder_day = None, reminder_month = None, reminder_year = None, reminder_hour = None):
    conn = sqlite3.connect('employee.db') # connecting to the database file

    c = conn.cursor()
    # creating the database
    c.execute("""CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory text NOT NULL,
            year int NOT NULL,
            month int NOT NULL,
            day int NOT NULL,
            hour int NOT NULL,
            image_path text,
            reminder_day int,
            reminder_month int,
            reminder_year int,
            reminder_hour int,
            UNIQUE(memory, year, month, day)
            )""")
    
    if image_path:
        try:
            if reminder_day:
                # Insert memory into the 'memories' table
                c.execute(
                    "INSERT INTO memories (memory, year, month, day, hour, image_path, reminder_day, reminder_month, reminder_year, reminder_hour) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (memory, year, month, day, hour, image_path, reminder_day, reminder_month, reminder_year, reminder_hour),
                )
                memory_id = c.lastrowid

                # Create the 'reminders' table if it doesn't exist
                c.execute("""CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER, sent BOOLEAN
                )""")

                # Insert a new row into the 'reminders' table
                c.execute("INSERT INTO reminders (id, sent) VALUES (?, ?)", (memory_id, False))
                error = False
            else:
                c.execute(
                    "INSERT INTO memories (memory, year, month, day, hour, image_path) VALUES (?, ?, ?, ?, ?, ?)",
                    (memory, year, month, day, hour, image_path),
                )
                error = False
        except sqlite3.IntegrityError:
            error = True
    else:
        try:
            if reminder_day:
                c.execute(
                    "INSERT INTO memories (memory, year, month, day, hour, reminder_day, reminder_month, reminder_year, reminder_hour) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (memory, year, month, day, hour, reminder_day, reminder_month, reminder_year, reminder_hour),
                )
                memory_id = c.lastrowid

                c.execute("""CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER, sent BOOLEAN
                )""")
                c.execute("INSERT INTO reminders (id, sent) VALUES (?, ?)", (memory_id, False))
                error = False
            else:
                c.execute(
                    "INSERT INTO memories (memory, year, month, day, hour) VALUES (?, ?, ?, ?, ?)",
                    (memory, year, month, day, hour),
                )
                error = False
        except sqlite3.IntegrityError:
            error = True

    c.execute("SELECT * FROM memories WHERE year=2025")

    # closing
    conn.commit()
    conn.close()

    see_reminders()

    return error

def insert_edited_memory(id, memory, image_path = None, reminder_day = None, reminder_month = None, reminder_year = None, reminder_hour = None):
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    try:
        if image_path:
            if reminder_day:
                c.execute("""UPDATE memories SET memory = ?, image_path = ?, reminder_day = ?, reminder_month = ?, reminder_year = ?, reminder_hour = ? WHERE id = ?""",
                          (memory, image_path, reminder_day, reminder_month, reminder_year, reminder_hour, id))
            else:
                c.execute("""UPDATE memories SET memory = ?, image_path = ? WHERE id = ?""",
                          (memory, image_path, id))
        else:
            if reminder_day:
                c.execute("""UPDATE memories SET memory = ?, image_path = ?, reminder_day = ?, reminder_month = ?, reminder_year = ?, reminder_hour = ? WHERE id = ?""",
                          (memory, image_path, reminder_day, reminder_month, reminder_year, reminder_hour, id))
            else:
                c.execute("""UPDATE memories SET memory = ?, image_path = ? None WHERE id = ?""",
                          (memory, image_path, id))
        conn.commit()
        error = False
    except sqlite3.IntegrityError:
        error = True
    finally:
        conn.close()

    return error

def get_memories():
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    # Fetch the most recent entries
    try:
        query = "SELECT * FROM memories ORDER BY ID DESC"
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError:
        return None

    # closing
    conn.commit()
    conn.close()

def delete_memory(id):
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    c.execute(f"DELETE FROM memories WHERE id = {id}")
    try:
        c.execute(f"DELETE FROM reminders WHERE id = {id}")
    except:
        pass

    # closing
    conn.commit()
    conn.close()

def access_memory(id):
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    c.execute(f"SELECT * FROM memories WHERE id = {id}")
    return c.fetchone()

    # closing
    conn.commit()
    conn.close()

def save_email(email):
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS email (email text)")
    c.execute("INSERT INTO email (email) VALUES (?)", (email,))

    # checking
    c.execute("SELECT * FROM email")

    # closing
    conn.commit()
    conn.close()

def get_email():
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM email")
        return c.fetchall()[-1][0]
    except sqlite3.OperationalError:
        return None

    # closing
    conn.commit()
    conn.close()

def see_reminders():
    connection = sqlite3.connect('employee.db')  # Replace with your database name
    cursor = connection.cursor()

    # Execute the query to retrieve all rows from the table
    table_name = 'reminders'  # Replace with your table name
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    connection.close()

def check_opening():
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    c.execute("SELECT * FROM opening")
    return c.fetchall()[-1][0]
    # return c.fetchall()

def opening(state = None):
    conn = sqlite3.connect('employee.db') # connecting to the database file
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS opening (
        manually BOOLEAN
    )""")
    conn.commit()

    try:
        c.execute(f"SELECT * FROM memories")

        if state == None:
            pass
        else:
            c.execute("INSERT INTO opening (manually) VALUES (?)", (state,))
    except sqlite3.OperationalError:
        c.execute("INSERT INTO opening (manually) VALUES (True)")

    conn.commit()
    conn.close()