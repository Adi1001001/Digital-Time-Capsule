
import tkinter as tk
from datetime import datetime
from tkinter import Toplevel # for the notification
from database_handling import *
# for attaining images
from tkinter import filedialog
from PIL import Image, ImageTk
from validate_email_address import validate_email
from reminders import send_verification_email, verify_user_email, check_reminders
import customtkinter as ctk
from tkcalendar import Calendar
import os

# standards
dark_grey = '#1b1c18'
white_text = '#eef2df'
image_path = [] # file path to the images/files
image_there = False
image_counter = 0
recent_memories = []
big_memory_box = None
toggle_switch_on = True
edited = None
image_number = 0
delete_image_preview_button1 = None
delete_image_preview_button2 = None
delete_image_preview_button3 = None
delete_image_preview_button4 = None
verification = False
verification_code = None
stored_code = None
No_memories = None
confirm_reminder_date = False
title_label = None
reminder_index = 0
reminders = None
# colour set
sky_blue = '#74a1e8'
deep_rust = '#763626'
dark_charcoal = '#2A3132'
charcoal = '#4d4d4d'
burnt_orange = '#ff6f3c'
teal = '#3aafa9'
mint_green = '#a8d5ba'
cream = '#d9ffed'
light_gray = '#bdbdbd'
primary_color = "#007bff"  # Bootstrap primary blue
hover_color = "#0056b3"    # Darker blue for hover
text_color = "#ffffff"     # White text

# window configuration
window = ctk.CTk() #window = ttk.Window()
window.title('Digital Time Capsule')
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() - 100
window.geometry(f"{screen_width}x{screen_height}")
window.resizable(True, True) # allowing the window to be resizable

script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script

# icons
icon_image_path = os.path.join(script_dir, "Assets", "delete.png")
delete_button_image = Image.open(icon_image_path)
delete_button_image.thumbnail((50, 50))  # Resize for preview
delete_button_image_tk = ImageTk.PhotoImage(delete_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "delete.png")
small_delete_button_image = Image.open(icon_image_path)
small_delete_button_image.thumbnail((30, 30))
small_delete_button_image_tk = ImageTk.PhotoImage(small_delete_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "on-button.png")
on_button_image = Image.open(icon_image_path)
on_button_image.thumbnail((30, 30))  # Resize for preview
on_button_image_tk = ImageTk.PhotoImage(on_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "off-button.png")
off_button_image = Image.open(icon_image_path)
off_button_image.thumbnail((30, 30))  # Resize for preview
off_button_image_tk = ImageTk.PhotoImage(off_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "pencil.png")
edit_button_image = Image.open(icon_image_path)
edit_button_image.thumbnail((50, 50))  # Resize for preview
edit_button_image_tk = ImageTk.PhotoImage(edit_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "off-button.png")
create_button_image = Image.open(icon_image_path)
create_button_image.thumbnail((50, 50))  # Resize for preview
create_button_image_tk = ImageTk.PhotoImage(create_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "expand.png")
expand_button_image = Image.open(icon_image_path)
expand_button_image.thumbnail((50, 50))  # Resize for preview
expand_button_image_tk = ImageTk.PhotoImage(expand_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "photo-camera.png")
camera_button_image = Image.open(icon_image_path)
camera_button_image.thumbnail((50, 50))  # Resize for preview
camera_button_image_tk = ImageTk.PhotoImage(camera_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "fast-forward.png")
forward_button_image = Image.open(icon_image_path)
forward_button_image.thumbnail((50, 50))  # Resize for preview
forward_button_image_tk = ImageTk.PhotoImage(forward_button_image) # you have to convert into photoimage to display images in tkinter

icon_image_path = os.path.join(script_dir, "Assets", "backward.png")
backward_button_image = Image.open(icon_image_path)
backward_button_image.thumbnail((50, 50))  # Resize for preview
backward_button_image_tk = ImageTk.PhotoImage(backward_button_image) # you have to convert into photoimage to display images in tkinter

# the different screens
frame0 = tk.Frame(window)
frame0.configure(bg = dark_charcoal)
frame1 = tk.Frame(window)
frame1.configure(bg = dark_charcoal)
frame2 = tk.Frame(window)
frame2.configure(bg = dark_charcoal)

navigation_frame0 = tk.Frame(frame0)
navigation_frame0.configure(bg = dark_charcoal)
navigation_frame1 = tk.Frame(frame1)
navigation_frame1.configure(bg = dark_charcoal)
navigation_frame2 = tk.Frame(frame2)
navigation_frame2.configure(bg = dark_charcoal)

# navigating between different windows/frames
def enter_home():
    email = get_email()
    frame0.tkraise()
    navigation_frame0.pack(side = "bottom")
    frame0.place(relwidth=1, relheight=1)
    if email == None:
        email_frame.pack()
    else:
        change_email_frame.pack(side='top', anchor='n')
        email_frame.pack_forget()
        verification_frame.pack_forget()
    try:
        clear_big_memory_box()
    except AttributeError:
        pass
    reminder_window()
def enter_main_screen():
    frame1.tkraise()
    navigation_frame1.place(y = 927)
    frame1.place(relwidth=1, relheight=1)
    try:
        clear_big_memory_box()
    except AttributeError:
        pass
def enter_memory_log():
    global No_memories
    navigation_frame2.pack(side = "bottom")
    recent_memories = get_memories()
    frame2.tkraise()
    frame2.place(relwidth=1, relheight=1)
    if recent_memories == None or recent_memories == []:
        if No_memories:
            No_memories.destroy()
        No_memories = ctk.CTkLabel(master = frame2, text = 'No memories created yet', font = ("Times New Roman", 24, "bold"), bg_color= dark_charcoal, text_color= teal)
        No_memories.pack(pady = 25)
        try:
            canvas.pack_forget()
        except UnboundLocalError:
            pass
    else:
        create_table(recent_memories)
        window.after(100, update_scroll_region)  # Delay scroll region update by 100ms
        try:
            No_memories.destroy()
        except UnboundLocalError:
            pass
        except AttributeError:
            pass

home_button = ctk.CTkButton(navigation_frame0, text="Enter Home", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, state = 'disabled')
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
home_button = ctk.CTkButton(navigation_frame1, text="Enter Home", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_home)
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
home_button = ctk.CTkButton(navigation_frame2, text="Enter Home", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_home)
home_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')

main_screen_button = ctk.CTkButton(navigation_frame0, text="Enter Main Screen", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_main_screen)
main_screen_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
main_screen_button = ctk.CTkButton(navigation_frame1, text="Enter Main Screen", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, state = 'disabled')
main_screen_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')
main_screen_button = ctk.CTkButton(navigation_frame2, text="Enter Main Screen", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_main_screen)
main_screen_button.pack(pady=10, padx=150, ipadx = 55, side = 'left')

memory_log_button = ctk.CTkButton(navigation_frame0, text="Enter Memory Log", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_memory_log)
memory_log_button.pack(pady=10, padx=150, ipadx = 55, side = 'right')
memory_log_button = ctk.CTkButton(navigation_frame1, text="Enter Memory Log", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = enter_memory_log)
memory_log_button.pack(pady=10, padx=150, ipadx = 55, side = 'right')
memory_log_button = ctk.CTkButton(navigation_frame2, text="Enter Memory Log", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, state = 'disabled')
memory_log_button.pack(pady=10, padx=150, ipadx = 55, side = 'right')

# Create the canvas inside the frame
canvas = tk.Canvas(frame2, background=dark_charcoal, width=screen_width, height=screen_height-200)
# Add a vertical scrollbar to the canvas
scrollbar = ctk.CTkScrollbar(canvas, command=canvas.yview)
# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# main stuff
title_text = ctk.CTkLabel(master = frame1, text = 'The Digital Time Capsule', font = ("Times New Roman", 38, "bold"), text_color = teal)
title_text.pack(pady = 25)

memory_input = ctk.CTkTextbox(master = frame1, width = 1200, height = 300, wrap = 'word', activate_scrollbars = True, font = ('Times New Roman', 18), text_color = deep_rust, corner_radius = 15, fg_color = light_gray)
memory_input.pack()

frame1_left = ctk.CTkFrame(frame1, width = 770, height = 260, fg_color='transparent')
frame1_left.place(x = 5, y = 410)
frame1_left.propagate(False)

frame1_left_text = ctk.CTkLabel(master = frame1_left, text = 'Images', font = ("Times New Roman", 31, "bold"), text_color = teal)
frame1_left_text.pack(pady = 5)

frame1_right = ctk.CTkFrame(frame1, width = 750, height = 260, fg_color='transparent')
frame1_right.place(x = 782, y = 410)
frame1_right.propagate(False)

frame1_right_text = ctk.CTkLabel(master = frame1_right, text = 'Reminders', font = ("Times New Roman", 31, "bold"), text_color = teal)
frame1_right_text.pack(pady = 5)

thumbnail_box = ctk.CTkFrame(frame1_left, width = 550, height = 125)
thumbnail_box.pack(pady=10)

# notifications
def show_notification(frame, msg):
    # Create a top-level window
    notification = Toplevel(frame)
    
    # Set the window size and position
    notification.geometry(f"1000x200+{int(screen_width/2 - 250)}+{int(screen_height/2)}")  # Width, Height, X, Y
    notification.resizable(False, False)
    
    # Remove the border and title bar for a "floating" effect
    notification.overrideredirect(True)
    
    # Add the message
    label = tk.Label(notification, text=msg, font=("Arial", 24, "bold"))
    label.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Automatically close the notification after 2 seconds
    notification.after(3000, notification.destroy)

toggle_switch_label_false = ctk.CTkLabel(master = frame1, text = 'Reminders are OFF', font = ("Times New Roman", 25), text_color = '#ff1222')
toggle_switch_label_false.place(x = 1150, y = 470)
toggle_switch_label_true = ctk.CTkLabel(master = frame1, text = 'Reminders are ON', font = ("Times New Roman", 25), text_color = '#27ff1c')
    
reminder_date_enter_label = ctk.CTkLabel(master = frame1, text = '* Enter Date (DD/MM/YYYY) and \nhours (HH) (24 hour time)', font = ("Times New Roman", 14), text_color = light_gray)
reminder_date_enter_label.place(x = 1200, y = 520)

def get_selected_datetime():
    global confirm_reminder_date
    selected_date = reminder_cal.get_date()  # Get the selected date from the calendar
    selected_hour = hour_combobox.get()  # Get the selected hour from the combobox

    confirm_reminder_date = True

    # Format the selected date and time
    selected_datetime = f"Selected Date and Time: {selected_date} {selected_hour}:00"
    result_label.configure(text=selected_datetime)

# Get the current date and time
now = datetime.now()
current_year = now.year
current_month = now.month
current_day = now.day
current_hour = now.hour

# Set the hour to one hour ahead
one_hour_ahead = (current_hour + 1) % 24  # Ensure it wraps around if it goes past 23

# calendar
reminder_cal = Calendar(frame1, selectmode="day", year=current_year, month=current_month, day=current_day, date_pattern = 'dd-mm-yy')
reminder_cal.place(x = 1200, y = 650)

# Create a combobox for hour selection
hour_combobox = ctk.CTkComboBox(frame1, values=[f"{i:02d}" for i in range(24)], width=100)
hour_combobox.set("12")  # Set default hour
hour_combobox.place(x = 1250, y = 565)

# Create a button to confirm the selection
confirm_button = ctk.CTkButton(frame1, text="Confirm", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=150, height=30, command=get_selected_datetime, state='disabled')
confirm_button.place(x = 1225, y = 605)

# Create a label to display the selected date and time
result_label = ctk.CTkLabel(frame1, text="Selected Date and Time: ", font=("Times New Roman", 14), text_color=burnt_orange)
result_label.place(x = 1200, y = 640)

def expand_table_entry(memory_id):
    """
    Creates a pop-up overlay to display detailed memory information based on the given memory ID.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()

    # Fetch memory details by ID
    c.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
    memory = c.fetchone()
    conn.close()

    if not memory:
        return

    # Unpack memory details
    id, memory_text, year, month, day, hour, image_path, reminder_day, reminder_month, reminder_year, reminder_hour = memory
    date_str = f"{day}/{month}/{year} {hour}:00"
    reminder_date_str = f"{reminder_day}/{reminder_month}/{reminder_year} {reminder_hour}:00" if reminder_year else "No reminder set"

    # Create overlay window
    overlay = ctk.CTkToplevel(fg_color=dark_charcoal)

    # Get screen width and height
    screen_width = overlay.winfo_screenwidth()
    screen_height = overlay.winfo_screenheight()

    overlay_width = screen_width - 500
    overlay_height = screen_height - 250

    # Calculate position x and y coordinates
    position_x = (screen_width // 4) - 100# - (overlay_width // 2)
    position_y = (screen_height // 4) - 100# - (overlay_height // 2)

    overlay.geometry(f"{overlay_width}x{overlay_height}+{position_x}+{position_y}")
    overlay.title(f"Memory ID: {id}")
    overlay.attributes("-topmost", True)  # Keep overlay above the main window
    overlay.grab_set()  # Disable interaction with main windowW

    # Create a frame inside the canvas
    content_frame = ctk.CTkFrame(overlay, fg_color=dark_charcoal)
    content_frame.pack()

    # Title
    title_label = ctk.CTkLabel(content_frame, text="Memory Details", font=("Times New Roman", 35, "bold"), text_color = teal)
    title_label.pack(pady=20)

    # Memory details
    memory_text_label = ctk.CTkLabel(
        content_frame, text=f"Memory Text: {memory_text}", font=("Times New Roman", 16), wraplength=750, justify="left", text_color = light_gray)
    memory_text_label.pack(pady=10)

    date_label = ctk.CTkLabel(content_frame, text=f"Date: {date_str}", font=("Times New Roman", 16), text_color = light_gray)
    date_label.pack(pady=10)

    reminder_label = ctk.CTkLabel(content_frame, text=f"Reminder: {reminder_date_str}", font=("Times New Roman", 16), text_color = light_gray)
    reminder_label.pack(pady=10)

    # Frame for images
    images_frame = ctk.CTkFrame(content_frame, fg_color="white")
    images_frame.pack(pady=10)

    # Image display
    try:
        if image_path == [] or image_path == None:
            images_frame.pack_forget()
            img_label = ctk.CTkLabel(content_frame, text="No images added", font=("Times New Roman", 16), text_color = burnt_orange)
            img_label.pack(pady = 10)
        elif '|' in image_path:
            image_paths = image_path.split('|')
            for image_path in image_paths:
                img = Image.open(image_path)
                img.thumbnail((300, 200))  # Resize for display
                img_tk = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(images_frame, image=img_tk, text="")
                img_label.image = img_tk  # Keep reference to avoid garbage collection
                img_label.pack(side='left', padx=10)
        else:  # 1 image
            img = Image.open(image_path)
            img.thumbnail((300, 200))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(images_frame, image=img_tk, text="")
            img_label.image = img_tk  # Keep reference to avoid garbage collection
            img_label.pack(side='left', padx=10)
    except Exception as e:
        error_label = ctk.CTkLabel(content_frame, text="Image could not be loaded.", font=("Arial", 14), fg_color="red")
        error_label.pack(pady=10)

    # Close button
    close_button = ctk.CTkButton(overlay, text="Close", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=50, height=30, command = lambda: overlay.destroy())
    close_button.pack(pady=(10, 20))

def count_digits(number):
    return len(str(abs(number)))

def validate_date():
    global confirm_reminder_date, reminder_cal, hour_combobox
    try:
        if confirm_reminder_date != True:
            raise UnboundLocalError
        reminder_date = reminder_cal.get_date()
        reminder_hour = int(hour_combobox.get())
        day, month, year = map(int, reminder_date.split('-'))
        year += 2000
        if 1 <= day <= 31 and 1 <= month <= 12 and 0 <= reminder_hour <= 24:  # Basic validation
            current_date, current_time = str(datetime.today()).split(' ')
            current_year, current_month, current_day = current_date.split('-')
            current_hour, current_min = current_time.split(':')[:2]
            current_hour = int(current_hour)
            current_min = int(current_min)
            current_year = int(current_year)
            current_month = int(current_month)
            current_day = int(current_day)
            if current_min >= 30:
                current_hour += 1
            if year < current_year:
                raise ValueError
            elif year == current_year:
                if month < current_month:
                    raise ValueError
                elif month == current_month:
                    if day < current_day:
                        raise ValueError
                    elif day == current_day:
                        if reminder_hour <= current_hour:
                            raise ValueError
            return day, month, year, reminder_hour
        else:
            raise AttributeError
    except ValueError:
        show_notification(frame1, "You have entered the reminder date incorrectly!")
        toggle_switch_on = False
        toggle_switch()
    except AttributeError:
        show_notification(frame1, "You cannot have an hour above 24!")
        toggle_switch_on = False
        toggle_switch()
    except UnboundLocalError:
        show_notification(frame1, "You have to confirm the reminder date!")
    

def toggle_switch():
    global toggle_switch_on, reminder_date_enter_label, reminder_cal, hour_combobox, confirm_button, result_label, confirm_reminder_date

    if toggle_switch_on == True:
        set_reminder_button.configure(image = on_button_image_tk)
        toggle_switch_label_true.place(x = 1150, y = 470)
        toggle_switch_label_false.place_forget()

        confirm_button.configure(state = 'enabled')
        confirm_reminder_date = False

        toggle_switch_on = False
    else:
        set_reminder_button.configure(image = off_button_image_tk)
        toggle_switch_label_false.place(x = 1150, y = 470)
        toggle_switch_label_true.place_forget()

        result_label.configure(text="Selected Date and Time: ")
        confirm_button.configure(state = 'disabled')

        toggle_switch_on = True

set_reminder_button = ctk.CTkButton(frame1, image = off_button_image_tk, text='', command = toggle_switch, width=30, height=30)
set_reminder_button.place(x = 1050, y = 470)

def create_new_memory():
    global image_there, image_path, image_counter, edited, toggle_switch_on, image_number, delete_image_preview_button1, delete_image_preview_button2, delete_image_preview_button3, delete_image_preview_button4

    if toggle_switch_on == False:
        reminder_day, reminder_month, reminder_year, reminder_hour = validate_date()
        # toggle_switch()

    # get clean data on the memory text
    memory = memory_input.get("1.0", "end").strip()
    memory_input.delete("1.0", "end")

    if edited == None:
        # process the date and time
        date = str(datetime.today())
        date, date_time = date.split(' ')
        date_hour, date_minute = date_time.split(':')[:2] # split the date for the first 2 occurences that the : appears
        final_hour = int(date_hour)
        date_minute = int(date_minute)
        if date_minute >= 30:
            final_hour += 1
        final_year, final_month, final_day = date.split('-')
        final_year = int(final_year)
        final_month = int(final_month)
        final_day = int(final_day)

        #amount of days
        total_days = sum([
            31,  # January
            28,  # February (ignoring leap years for now)
            31,  # March
            30,  # April
            31,  # May
            30,  # June
            31,  # July
            31,  # August
            30,  # September
            31,  # October
            30,  # November
        ][:final_month - 1]) + final_day

        # inserting the image path into the database

        if image_path != []:
            image_counter = 0
            if len(image_path) == 1:
                image_paths = image_path[0]
            else:
                image_paths = "|".join(image_path)
            if toggle_switch_on == True:
                error = insert_memory(memory, final_year, final_month, final_day, final_hour, image_paths)
            else:
                error = insert_memory(memory, final_year, final_month, final_day, final_hour, image_paths, reminder_day, reminder_month, reminder_year, reminder_hour)
        else:
            if toggle_switch_on == True:
                error = insert_memory(memory, final_year, final_month, final_day, final_hour)
            else:
                image_paths = None
                error = insert_memory(memory, final_year, final_month, final_day, final_hour, image_paths, reminder_day, reminder_month, reminder_year, reminder_hour)
    else:
        if image_path != []:
            image_counter = 0
            if len(image_path) == 1:
                image_paths = image_path[0]
            else:
                image_paths = "|".join(image_path)
            if toggle_switch_on == True:
                error = insert_edited_memory(edited, memory, image_paths)
            else:
                error = insert_edited_memory(edited, memory, image_paths, reminder_day, reminder_month, reminder_year, reminder_hour)
        else:
            image_paths = None
            if toggle_switch_on == True:
                error = insert_edited_memory(edited, memory, image_paths)
            else: 
                error = insert_edited_memory(edited, memory, image_paths, reminder_day, reminder_month, reminder_year, reminder_hour)
        edited = None
    image_path = []
    image_there = False
    image_number = 0

    # Clear the thumbnails from the display
    for widget in thumbnail_box.winfo_children():
        widget.destroy()

    if delete_image_preview_button1:
        delete_image_preview_button1.destroy()
    if delete_image_preview_button2:
        delete_image_preview_button2.destroy()
    if delete_image_preview_button3:    
        delete_image_preview_button3.destroy()
    if delete_image_preview_button4:
        delete_image_preview_button4.destroy()

    # show notification
    if error:
        show_notification(frame1, "Your memory has ALREADY been saved!")
    else:
        show_notification(frame1, "Your memory has been saved!")

    if toggle_switch_on == False:
        toggle_switch()

new_memory_button = ctk.CTkButton(frame1, text = "Create a new memory", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width = 150, height = 30, command = create_new_memory)
new_memory_button.place(x = 670, y = 700)

def remove_image(image_index):
    global image_path, image_number, image_counter
    image_path.pop(image_index)
    image_number -= 1
    image_counter -= 1
    thumbnail_box.winfo_children()[image_index].destroy()
    if image_counter == 0:
        delete_image_preview_button1.destroy()
    elif image_counter == 1:
        delete_image_preview_button2.destroy()
    elif image_counter == 2:
        delete_image_preview_button3.destroy()
    else:
        delete_image_preview_button4.destroy()
    rearange_delete_buttons(image_number)

def rearange_delete_buttons(image_number):
    global delete_image_preview_button1, delete_image_preview_button2, delete_image_preview_button3, delete_image_preview_button4
    if delete_image_preview_button1:
        delete_image_preview_button1.destroy()
    if delete_image_preview_button2:
        delete_image_preview_button2.destroy()
    if delete_image_preview_button3:
        delete_image_preview_button3.destroy()
    if delete_image_preview_button4:
        delete_image_preview_button4.destroy()
    delete_image_preview_button1 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(0), width=20, height=20)
    delete_image_preview_button2 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(1), width=20, height=20)
    delete_image_preview_button3 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(2), width=20, height=20)
    delete_image_preview_button4 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(3), width=20, height=20)
    if image_number == 1:
        delete_image_preview_button1.place(x = 370, y = 560)
    if image_number == 2:
        delete_image_preview_button1.place(x = 305, y = 560)
        delete_image_preview_button2.place(x = 440, y = 560)
    if image_number == 3:
        delete_image_preview_button1.place(x = 240, y = 560)
        delete_image_preview_button2.place(x = 370, y = 560)
        delete_image_preview_button3.place(x = 500, y = 560)
    if image_number == 4:
        delete_image_preview_button1.place(x = 170, y = 560)
        delete_image_preview_button2.place(x = 300, y = 560)
        delete_image_preview_button3.place(x = 400, y = 560)
        delete_image_preview_button4.place(x = 570, y = 560)

# for desktop only
def show_image_preview(image_path, image_number):
    global delete_image_preview_button1, delete_image_preview_button2, delete_image_preview_button3, delete_image_preview_button4
    # Load and display the selected image as a thumbnail
    img = Image.open(image_path)
    img.thumbnail((150, 150))  # Resize for preview
    img_tk = ImageTk.PhotoImage(img) # you have to convert into photoimage to display images in tkinter
    # Add the thumbnail to the box
    label = tk.Label(thumbnail_box, image=img_tk, width = 150, height = 150)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack(side="left", padx=5)  # Adjust padding as needed
    if delete_image_preview_button1:
        delete_image_preview_button1.destroy()
    if delete_image_preview_button2:
        delete_image_preview_button2.destroy()
    if delete_image_preview_button3:
        delete_image_preview_button3.destroy()
    if delete_image_preview_button4:
        delete_image_preview_button4.destroy()
    delete_image_preview_button1 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(0), width=20, height=20)
    delete_image_preview_button2 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(1), width=20, height=20)
    delete_image_preview_button3 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(2), width=20, height=20)
    delete_image_preview_button4 = ctk.CTkButton(frame1, image = small_delete_button_image_tk, text='', command = lambda: remove_image(3), width=20, height=20)
    if image_number == 1:
        delete_image_preview_button1.place(x = 370, y = 560)
    if image_number == 2:
        delete_image_preview_button1.place(x = 305, y = 560)
        delete_image_preview_button2.place(x = 440, y = 560)
    if image_number == 3:
        delete_image_preview_button1.place(x = 240, y = 560)
        delete_image_preview_button2.place(x = 370, y = 560)
        delete_image_preview_button3.place(x = 500, y = 560)
    if image_number == 4:
        delete_image_preview_button1.place(x = 170, y = 560)
        delete_image_preview_button2.place(x = 300, y = 560)
        delete_image_preview_button3.place(x = 430, y = 560)
        delete_image_preview_button4.place(x = 570, y = 560)

def get_images():
    global image_path, image_there, image_counter, image_number
    image_path.append(filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]))
    if image_path:
        image_counter += 1
        if image_counter > 4:
            del image_path[-1]
            show_notification(frame1, "Too many images!")
        else:
            image_number += 1
            image_there = True
            show_image_preview(image_path[-1], image_number)

camera_button = ctk.CTkButton(frame1_left, image = camera_button_image_tk, text='', command = get_images, width = 50, height = 50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
camera_button.pack(pady = 5)
camera_button.image = camera_button_image_tk

# Enable mouse wheel scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * int(event.delta / 120), "units")
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Update the scrollregion whenever the scrollable frame changes size
def update_scroll_region():
    canvas.configure(scrollregion=canvas.bbox("all"))

def edit_table_entry(id):
    global toggle_switch_on, reminder_cal, hour_combobox, confirm_button, edited, image_number, delete_image_preview_button1, delete_image_preview_button2, delete_image_preview_button3, delete_image_preview_button4, image_path, image_counter
    enter_main_screen()

    # clearing the main screen
    if toggle_switch_on == False:
        toggle_switch()
    memory_input.delete("1.0", "end")
    for widget in thumbnail_box.winfo_children():
        widget.destroy()
    if delete_image_preview_button1:
        delete_image_preview_button1.destroy()
    if delete_image_preview_button2:
        delete_image_preview_button2.destroy()
    if delete_image_preview_button3:    
        delete_image_preview_button3.destroy()
    if delete_image_preview_button4:
        delete_image_preview_button4.destroy()

    # getting the memory
    memory = access_memory(id)

    image_number = 0
    image_counter = 0

    # images
    if memory[6] != None: # if there are images
        if '|' in memory[6]: # more than 1 image
            image_paths = memory[6].split('|')
            for image_path1 in image_paths:
                image_number += 1
                image_counter += 1
                image_path.append(image_path1)
                show_image_preview(image_path1, image_number)
        else: # 1 image
            image_path1 = memory[6]
            image_number += 1
            image_counter += 1
            image_path.append(image_path1)
            show_image_preview(image_path1, image_number)

    # reminder time
    if memory[7] != None:
        toggle_switch()
        if count_digits(memory[7]) == 1:
            if count_digits(memory[8]) == 1:
                reminder_date_str = f"0{memory[7]}-0{memory[8]}-{memory[9]}"
            else:
                reminder_date_str = f"0{memory[7]}-{memory[8]}-{memory[9]}"
        elif count_digits(memory[8]) == 1:
            reminder_date_str = f"{memory[7]}-0{memory[8]}-{memory[9]}"
        else:
            reminder_date_str = f"{memory[7]}-{memory[8]}-{memory[9]}"
        if count_digits(memory[10]) == 1:
            reminder_hour_str = f"0{memory[10]}"
        else:
            reminder_hour_str = str(memory[10])

        reminder_cal.selection_set(reminder_date_str)
        hour_combobox.set(reminder_hour_str)

    # memory text
    memory_input.insert("end", memory[1])

    edited = id

def delete_table_entry(id):
    delete_memory(id)
    show_notification(frame1, "Your memory has been deleted!")
    clear_big_memory_box()
    recent_memories = get_memories()
    create_table(recent_memories)

def create_table(memories):
    global big_memory_box, screen_height, screen_width

    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    big_memory_box = ctk.CTkFrame(canvas, width=screen_width, height=screen_height)
    canvas.create_window((0, 0), window=big_memory_box, anchor="nw")  # Add big_memory_box to the canvas

    # Configure column weights for resizing
    big_memory_box.grid_columnconfigure(0, weight=1, minsize=10)  # ID column, smaller size
    big_memory_box.grid_columnconfigure(1, weight=3, minsize=750)  # Memory Text column, larger size
    big_memory_box.grid_columnconfigure(2, weight=1, minsize=150)  # Date column, smaller size
    big_memory_box.grid_columnconfigure(3, weight=1, minsize=150)  # Reminder Date column, smaller size
    big_memory_box.grid_columnconfigure(4, weight=2, minsize=350)  # Images column, larger size
    big_memory_box.grid_columnconfigure(5, weight=1, minsize=75)  # Edit column, smaller size
    big_memory_box.grid_columnconfigure(6, weight=1, minsize=75)  # Expand column, smaller size
    big_memory_box.grid_columnconfigure(7, weight=1, minsize=75)  # Delete column, smaller size

    # Creating table headers
    headers = ['ID', 'Memory Text', 'Date', 'Reminder Date', 'Images', 'Edit', 'Expand', 'Delete']

    # Adding headers to the first row
    for col, header in enumerate(headers):  # enumerate allows you to use the for loop normally and keep track of the index for each element
        header_label = ctk.CTkLabel(big_memory_box, text=header, font=("Arial", 12, "bold"), anchor="center", wraplength=500, justify='left')
        header_label.grid(row=1, column=col, padx=10, pady=5)

    # ADDING THE ACTUAL ROWS

    # Iterate through the database results and populate rows
    for i, memory in enumerate(memories):
        id, memory_text, year, month, day, hour, image_path, reminder_day, reminder_month, reminder_year, reminder_hour = memory

        # Displaying the ID, memory text, and formatted date
        date_str = f"{day}/{month}/{year} {hour}:00"
        if reminder_year != None:
            reminder_date_str = f"{reminder_day}/{reminder_month}/{reminder_year} {reminder_hour}:00"
        if reminder_year == None:
            reminder_date_str = "No reminder set"
        row_data = [id, memory_text, date_str, reminder_date_str]

        for j, data in enumerate(row_data):
            data_label = ctk.CTkLabel(big_memory_box, text=data, font=("Arial", 12), wraplength=650, justify='left')
            data_label.grid(row=i + 2, column=j, padx=10, pady=5, sticky="nsew")

        # Adding the images
        if image_path == None:
            image_box = ctk.CTkLabel(big_memory_box, text="No images", font=("Arial", 12))
            image_box.grid(row=i + 2, column=4, padx=10, pady=5)
        else:
            if '|' in image_path:  # more than 1 image
                # Create a frame for image navigation
                img_frame = ctk.CTkFrame(big_memory_box)
                img_frame.grid(row=i + 2, column=4, padx=10, pady=5)

                image_paths = image_path.split('|')
                for idx, image in enumerate(image_paths):
                    try:
                        img = Image.open(image)
                        img.thumbnail((100, 100))  # Resize for preview
                        img_tk = ImageTk.PhotoImage(img)
                        img_label = ctk.CTkLabel(img_frame, image=img_tk, text="")
                        img_label.image = img_tk  # Keep a reference to avoid garbage collection
                        img_label.grid(row=0, column=idx, padx=10, pady=5)
                    except PermissionError as e:
                        pass
                    except FileNotFoundError as e:
                        pass
                    except Exception as e:
                        pass
            else:  # 1 image
                img = Image.open(image_path)
                img.thumbnail((200, 150))  # Resize for preview
                img_tk = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(big_memory_box, image=img_tk, text="")
                img_label.image = img_tk  # Keep a reference to avoid garbage collection
                img_label.grid(row=i + 2, column=4, padx=10, pady=5)

        # adding the edit button
        edit_button = ctk.CTkButton(big_memory_box, image=edit_button_image_tk, text='', command=lambda x=id: edit_table_entry(x), width=50, height=50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        edit_button.grid(row=i + 2, column=5, padx=10, pady=5)
        edit_button.image = edit_button_image_tk

        # adding the expand button
        expand_button = ctk.CTkButton(big_memory_box, image=expand_button_image_tk, text='', command=lambda x=id: expand_table_entry(x), width=50, height=50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        expand_button.grid(row=i + 2, column=6, padx=10, pady=5)
        expand_button.image = expand_button_image_tk

        # adding the delete button
        delete_button = ctk.CTkButton(big_memory_box, image=delete_button_image_tk, text='', command=lambda x=id: delete_table_entry(x), width=50, height=50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        delete_button.grid(row=i + 2, column=7, padx=10, pady=5)
        delete_button.image = delete_button_image_tk

    # add_row_click_events(big_memory_box, memories)
    update_scroll_region()

# FRAME 2

def clear_big_memory_box():
    global big_memory_box
    big_memory_box.destroy()

# FRAME 0

def check_email_exists(email):
    """Check if an email address exists."""
    is_valid = validate_email(email, verify=True)
    return is_valid

def confirm_email():
    global email, stored_code, verification_frame
    reminder_frame.pack_forget()
    email = email_entry.get()
    if email == '':
        show_notification(frame0, "You have to enter an email to get reminders!")
    else:
        is_valid = check_email_exists(email)
        if is_valid:
            email = email.lower().strip()
            email_frame.pack_forget()
            verification_frame.pack()
            stored_code = send_verification_email(email)
            msg = f"This email has been saved: {email}. Type the verification code."
            show_notification(frame0, msg)
        else:
            show_notification(frame0, "Your email doesn't exist! Please re-enter!")

def verify_email():
    global email, verification, stored_code, change_email_frame, current_email_label
    reminder_frame.pack_forget()
    entered_code = verification_entry.get()
    verification_entry.delete(0, tk.END)
    entered_code = int(entered_code.strip())
    verification = verify_user_email(entered_code, stored_code)
    if verification == True:
        save_email(email)
        show_notification(frame0, "Your email has been verified!")
        verification_frame.pack_forget()
        current_email_label.pack_forget()
        current_email_label = ctk.CTkLabel(master = change_email_frame, text = f'Current email: {get_email()}', font = ("Times New Roman", 26), text_color = burnt_orange)
        current_email_label.pack(side='left', padx=10)
        change_email_button.pack(side='right', padx=10)
        change_email_frame.pack(side='top', anchor='n')
    else:
        show_notification(frame0, "Your email verification code was incorrect")
        verification_entry.delete(0, tk.END)

# email_frame
email_frame = tk.Frame(frame0)
email_frame.configure(bg = dark_charcoal)
email_label = ctk.CTkLabel(master = email_frame, text = 'Email:', font = ("Times New Roman", 26), text_color = burnt_orange)
email_entry = ctk.CTkEntry(email_frame, width = 250)
email_entry_button = ctk.CTkButton(email_frame, text="Enter", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=150, height=30, command = confirm_email)

email_label.pack(padx=100, side='left', pady = 10)
email_entry.pack(padx=100, side='left', pady = 10)
email_entry_button.pack(padx=50, side='right', pady = 10)

# verification_frame
verification_frame = tk.Frame(frame0)
verification_frame.configure(bg = dark_charcoal)
verification_label = ctk.CTkLabel(master = verification_frame, text = 'Verification code:', font = ("Times New Roman", 26), text_color = burnt_orange)
verification_entry = ctk.CTkEntry(verification_frame, width = 250)
verification_button = ctk.CTkButton(verification_frame, text="Enter", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=150, height=30, command = verify_email)

verification_label.pack(padx=100, side='left', pady = 10)
verification_entry.pack(padx=100, side='left', pady = 10)
verification_button.pack(padx=50, side='right', pady = 10)

change_email_frame = tk.Frame(frame0)
change_email_frame.configure(bg = dark_charcoal)
change_email_button = ctk.CTkButton(change_email_frame, text="Change email", fg_color=primary_color, hover_color=hover_color, text_color=text_color, corner_radius=10, font=("Times New Roman", 16), width=150, height=30, command = lambda: (email_frame.pack(), change_email_button.pack_forget(), verification_frame.pack_forget()))

current_email_label = ctk.CTkLabel(master = change_email_frame, text = f'Current email: {get_email()}', font = ("Times New Roman", 26), text_color = burnt_orange)
current_email_label.pack(side='left', padx=10, pady = 10)
change_email_button.pack(side='right', padx=10, pady = 10)

def apply_memory(reminder):
    conn = sqlite3.connect('employee.db')
    c = conn.cursor()
    c.execute("SELECT * FROM memories WHERE id = ?", (reminder))
    memory = c.fetchone()

    id = memory[0]
    memories = memory[1]
    year = memory[2]
    month = memory[3]
    day = memory[4]
    hour = memory[5]
    image_path = memory[6]
    reminder_day = memory[7]
    reminder_month = memory[8]
    reminder_year = memory[9]
    reminder_hour = memory[10]

    datestr = f"{day}/{month}/{year} {hour}:00"
    reminderdatestr = f"{reminder_day}/{reminder_month}/{reminder_year} {reminder_hour}:00"

    if image_path != None:
        if '|' in image_path:
            image_paths = image_path.replace('|', '\n')
        else:
            image_paths = image_path
    # ADDING EVERYTHING
    # Title
    title_label = ctk.CTkLabel(reminder_frame, text="Memory Details", font=("Times New Roman", 35, "bold"), text_color = teal)
    title_label.pack(pady=20)

    # Memory details
    memory_text_label = ctk.CTkLabel(reminder_frame, text=f"Memory Text: {memories}", font=("Times New Roman", 16), wraplength=750, justify="left", text_color = light_gray)
    memory_text_label.pack(pady=10)

    date_label = ctk.CTkLabel(reminder_frame, text=f"Date: {datestr}", font=("Times New Roman", 16), text_color = light_gray)
    date_label.pack(pady=10)

    reminder_label = ctk.CTkLabel(reminder_frame, text=f"Reminder: {reminderdatestr}", font=("Times New Roman", 16), text_color = light_gray)
    reminder_label.pack(pady=10)

    # Frame for images
    images_frame = ctk.CTkFrame(reminder_frame, fg_color="white")
    images_frame.pack(pady=10)

    # Image display
    try:
        if image_path == [] or image_path == None:
            images_frame.pack_forget()
            img_label = ctk.CTkLabel(reminder_frame, text="No images added", font=("Times New Roman", 16), text_color = burnt_orange)
            img_label.pack(pady = 10)
        elif '|' in image_path:
            image_paths = image_path.split('|')
            for image_path in image_paths:
                img = Image.open(image_path)
                img.thumbnail((300, 200))  # Resize for display
                img_tk = ImageTk.PhotoImage(img)
                img_label = ctk.CTkLabel(images_frame, image=img_tk, text="")
                img_label.image = img_tk  # Keep reference to avoid garbage collection
                img_label.pack(side='left', padx=10)
        else:  # 1 image
            img = Image.open(image_path)
            img.thumbnail((300, 200))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(images_frame, image=img_tk, text="")
            img_label.image = img_tk  # Keep reference to avoid garbage collection
            img_label.pack(side='left', padx=10)
    except Exception as e:
        error_label = ctk.CTkLabel(reminder_frame, text="Image could not be loaded.", font=("Arial", 14), fg_color="red")
        error_label.pack(pady=10)

def go_forward():
    global reminder_index, reminders
    reminder_index += 1
    for widget in reminder_frame.winfo_children():
        # Ignore the label
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "":
            continue  # Skip this widget
        widget.destroy()
    apply_memory(reminders[reminder_index])

def go_backward():
    global reminder_index, reminders
    reminder_index -= 1
    for widget in reminder_frame.winfo_children():
        # Ignore the label
        if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "":
            continue  # Skip this widget
        widget.destroy()
    apply_memory(reminders[reminder_index])

reminder_frame = tk.Frame(frame0)
reminder_frame.configure(bg = dark_charcoal)
def reminder_window():
    global title_label, reminder_index, reminders
    reminder_frame.pack()

    conn = sqlite3.connect('employee.db')
    c = conn.cursor()

    c.execute("SELECT id FROM reminders WHERE sent = 1")
    reminders = c.fetchall()

    if reminders == None:
        if title_label != None:
            pass
        else:
            title_label = ctk.CTkLabel(reminder_frame, text="Memory Details", font=("Times New Roman", 35, "bold"), text_color = teal)
            title_label.pack(pady=20)
    elif len(reminders) == 1:
        apply_memory(reminders[0])
    else:
        reminder_index = -1
        apply_memory(reminders[reminder_index])

        forward_button = ctk.CTkButton(reminder_frame, image=forward_button_image_tk, text='', command=go_forward, width=50, height=50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        forward_button.pack(side = 'right', padx = 10, pady = 10)

        backward_button = ctk.CTkButton(reminder_frame, image=backward_button_image_tk, text='', command=go_backward, width=50, height=50)  # the lambda somehow gets the value of the id from when the button was created and when it is clicked it outputs it
        backward_button.pack(side = 'left', padx = 10, pady = 10)

opening()
state = check_opening()

if state == True:
    enter_main_screen()
    opening(True)
else:
    enter_home()
    opening(True)
    
window.mainloop()

check_reminders()