import os
import smtplib
from email.mime.text import MIMEText
import sqlite3
from datetime import datetime
import random
import subprocess
from database_handling import opening

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your email provider's SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = 'digitaltimecapsule0@gmail.com'
EMAIL_PASSWORD = 'mkol whbn qhus pjmf'

def send_verification_email(email):
    """Send a verification email with a code."""
    code = generate_verification_code()
    body = f"Your verification code is: {code}\nPlease enter this code in the app to verify your email."
    send_email(to_address=email, subject="Email Verification", body=body)
    return code

def verify_user_email(input_code, stored_code):
    """Verify the user's email by comparing codes."""
    return input_code == stored_code

def generate_verification_code():
    """Generate a 6-digit verification code."""
    return random.randint(100000, 999999)

def send_email(to_address, subject, body):
    """Send an email notification."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception:
        pass  # Suppress errors for now

def open_app():
    """Open the application programmatically."""
    try:
        opening(False)
        if os.name == 'nt':  # Windows
            subprocess.Popen(['python', 'DigitalTimeCapsule/digital_time_capsule.py'], shell=True)
        else:
            subprocess.Popen(['python3', 'DigitalTimeCapsule/digital_time_capsule.py'])
    except Exception:
        pass

def check_reminders():
    """Check if any reminders are due."""
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    try:
        c.execute("SELECT id FROM reminders WHERE sent = 0")
        reminders = c.fetchall()
        if reminders:
            current_datetime = datetime.now()
            for reminder in reminders:
                c.execute("SELECT * FROM memories WHERE id = ?", (reminder[0],))
                memory = c.fetchone()
                if not memory:
                    continue  # Skip if memory is missing

                reminder_datetime = datetime(
                    int(memory[9]),  # Year
                    int(memory[8]),  # Month
                    int(memory[7]),  # Day
                    int(memory[10])  # Hour
                )

                if current_datetime >= reminder_datetime:
                    id, memories, year, month, day, hour, image_path = memory[:7]

                    try:
                        c.execute("SELECT * FROM email")
                        email = c.fetchone()
                        if email:
                            email = email[0]
                    except Exception:
                        email = None

                    body = f"Your reminder is due: {memories}\nCreated on: {day}/{month}/{year} {hour}:00\nMemory ID: {id}"
                    if image_path:
                        body += f"\nImage Paths: {image_path.replace('|', '\n')}"

                    if email:
                        send_email(to_address=email, subject="Reminder Notification", body=body)

                    # Mark reminder as sent
                    c.execute("UPDATE reminders SET sent = 1 WHERE id = ?", (id,))
                    conn.commit()
                    
                    # Open the app
                    open_app()
    except sqlite3.OperationalError:
        pass
    finally:
        conn.close()

"""Run the reminder check and log it."""
check_reminders()

with open('C:/Users/Adi/Coding/DigitalTimeCapsule/wearechecking.txt', 'a') as f:
    f.write(f"Checked successfully at {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

# def exit_app(icon, item):
#     """Exit the system tray app."""
#     icon.stop()
#     os._exit(0)

# # ✅ **System Tray Setup**
# script_dir = os.path.dirname(os.path.abspath(__file__))
# image_path = os.path.join(script_dir, "Assets", "clock.png")
# image = Image.open(image_path)

# menu = Menu(
#     MenuItem("Open App", open_app),
#     MenuItem("Exit", exit_app)
# )

# icon = Icon("ReminderApp", image, "Reminder App", menu)

# def run_tray():
#     icon.run()  # Runs the tray in a separate thread

# threading.Thread(target=run_tray, daemon=True).start()