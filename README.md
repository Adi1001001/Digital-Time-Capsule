# Digital Time Capsule - Summary

A Python application that allows users to store memories, set reminders, and receive notifications via email. It includes:

 - A graphical user interface (GUI) built with Tkinter and CustomTkinter.
 - SQLite database for storing memories and reminders.
 - A system tray application for background notifications.
 - Automatic task scheduling using Task Scheduler (Windows) or Crontab (Linux/Mac).

# 📌 Digital Time Capsule - Installation Guide

## 🖥️ System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **Python Version:** 3.8 or higher
- **Required Libraries:** Listed in `requirements.txt`
- **Internet Connection:** Required for email notifications

---

## 🔽 Step 1: Install Python

### 🏁 Windows

1. Download Python from [python.org](https://www.python.org/downloads/).
2. Run the installer **as administrator**.
3. **IMPORTANT:** Check ✅ "Add Python to PATH" before clicking "Install".
4. Verify installation:
   ```sh
   python --version
   ```

### 🍏 macOS

1. Open Terminal and install Python using Homebrew:
   ```sh
   brew install python
   ```
2. Verify installation:
   ```sh
   python3 --version
   ```

### 🐧 Linux (Debian/Ubuntu)

1. Install Python via APT:
   ```sh
   sudo apt update && sudo apt install python3 python3-pip -y
   ```
2. Verify installation:
   ```sh
   python3 --version
   ```

### 🐧 Linux (Arch-based)

```sh
sudo pacman -S python python-pip
```

---

## 👥 Step 2: Clone the Repository

First, ensure you have git.
Second, download the project files from GitHub.

### Windows (Command Prompt / PowerShell)

```sh
git clone https://github.com/your-username/DigitalTimeCapsule.git
```

```sh
cd DigitalTimeCapsule
```

### macOS & Linux (Terminal)

```sh
git clone https://github.com/your-username/DigitalTimeCapsule.git
```
```sh
cd DigitalTimeCapsule
```

---

## 📦 Step 3: Install Dependencies

Navigate to the project folder and run:

```sh
pip install -r requirements.txt
```

If `requirements.txt` is missing, manually install the packages:

```sh
pip install pystray pillow schedule smtplib sqlite3
```

---

## 🚀 Step 4: Run the Application

### Windows

```sh
python DigitalTimeCapsule/main.py
```

### macOS/Linux

```sh
python3 DigitalTimeCapsule/main.py
```

If using **Task Scheduler (Windows) or Cron (Linux/macOS)** for automatic startup, see **Step 5**.

---

## ⏲️ Step 5: Set Up Automatic Reminders

### 🏁 Windows (Task Scheduler)

1. Open **Task Scheduler** (`Win + R`, type `taskschd.msc`, press Enter).
2. Click **Create Basic Task**.
3. Set a name (e.g., "Digital Time Capsule Reminder").
4. Under **Trigger**, select "Daily" or "At startup".
5. Under **Action**, select "Start a program".
6. Browse for `python.exe`.
7. In **Arguments**, enter:
   ```sh
   "C:\path\to\DigitalTimeCapsule\main.py"
   ```
8. Click **Finish**.

### 🍏 macOS/Linux (Crontab)

1. Open Terminal and edit crontab:
   ```sh
   crontab -e
   ```
2. Add a new line to run the script every hour:
   ```sh
   0 * * * * /usr/bin/python3 /path/to/DigitalTimeCapsule/main.py
   ```
3. Save and exit (`Ctrl + X`, then `Y`, then `Enter`).

---

## 🔍 Troubleshooting

### "Command Not Found" Errors

- Ensure Python is installed and added to PATH.
- Try `python3` instead of `python`.

### Permissions Errors (Linux/macOS)

- Run with `sudo` if necessary.

### Email Not Sending

- Ensure you have enabled **Less Secure Apps** or App Passwords in Gmail.

---

## 🎉 You're All Set!

Now your Digital Time Capsule should work seamlessly. Enjoy! 🚀

If you have any errors or improvements or bugs I have to fix, please email digitaltimecapsule0@gmail.com. This will help me a ton so that I can improve this app.
Cheers, Jan 31st 2025
