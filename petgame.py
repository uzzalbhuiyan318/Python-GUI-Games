from tkinter import HIDDEN, NORMAL, Tk, Canvas


def start_move(event):
    # Store the initial position when the mouse is pressed
    c.data = {'x': event.x, 'y': event.y}

    # Trigger rose creation with a delay from the starting point of the event
    root.after(500, lambda: create_rose_with_transition(event))  # Delay for 500ms


def move_pet(event):
    # Calculate the distance moved and update the position of the pet
    dx = event.x - c.data['x']
    dy = event.y - c.data['y']

    # Move the entire pet (all components)
    for part in pet_parts:
        c.move(part, dx, dy)

    # Update the initial position
    c.data['x'] = event.x
    c.data['y'] = event.y


def stop_move(event):
    # After releasing the mouse, we don't need to create a rose
    c.data = None


def toggle_eyes():
    current_color = c.itemcget(eye_left, 'fill')
    new_color = c.body_color if current_color == 'white' else 'white'
    current_state = c.itemcget(pupil_left, 'state')
    new_state = NORMAL if current_state == HIDDEN else HIDDEN
    c.itemconfigure(pupil_left, state=new_state)
    c.itemconfigure(pupil_right, state=new_state)
    c.itemconfigure(eye_left, fill=new_color)
    c.itemconfigure(eye_right, fill=new_color)


def blink():
    toggle_eyes()
    root.after(250, toggle_eyes)
    root.after(3000, blink)


def create_rose_with_transition(event):
    # Get the position where the mouse event started
    nose_x = event.x
    nose_y = event.y

    # Initialize stem and rose parts
    stem = c.create_line(nose_x, nose_y + 50, nose_x, nose_y + 50, width=3, fill='green')  # Start small
    rose = c.create_oval(nose_x, nose_y, nose_x, nose_y, outline='red', fill='red')  # Tiny red dot
    c.rose_parts.append([stem, rose])

    # Animate the transition
    def grow_rose(step=0):
        if step <= 20:  # Limit growth steps
            # Gradually grow the stem
            c.coords(stem, nose_x, nose_y + 50 - step * 2.5, nose_x, nose_y + 50)
            # Gradually enlarge the rose
            c.coords(rose, nose_x - step, nose_y - step, nose_x + step, nose_y + step)
            root.after(20, lambda: grow_rose(step + 1))  # Recursively grow the rose

    grow_rose()


def center_pet():
    # Center the pet on the canvas
    canvas_width = c.winfo_width()
    canvas_height = c.winfo_height()

    # Calculate the offset to center the pet
    pet_bbox = c.bbox(body)
    pet_width = pet_bbox[2] - pet_bbox[0]
    pet_height = pet_bbox[3] - pet_bbox[1]

    dx = (canvas_width - pet_width) // 2 - pet_bbox[0]
    dy = (canvas_height - pet_height) // 2 - pet_bbox[1]

    # Move the entire pet to the center
    for part in pet_parts:
        c.move(part, dx, dy)


def resize_canvas(event):
    # Adjust the pet's position when the canvas size changes
    center_pet()


root = Tk()
root.title("Interactive Pet with a Rose")

# Set up the window size and behavior
root.geometry("800x600")
root.resizable(True, True)  # Allow resizing in both directions
root.configure(bg='#2F4F4F')  # Dark Slate Gray background for a professional look

# Create the canvas and configure it to fill the window
c = Canvas(root, bg='#2F4F4F', highlightthickness=0)
c.body_color = '#1F8A70'

# Body
body = c.create_oval(35, 20, 365, 350, outline=c.body_color, fill=c.body_color)

# Ears
ear_left = c.create_polygon(75, 80, 75, 10, 165, 70, outline=c.body_color, fill='#F3C5C5')
ear_right = c.create_polygon(255, 45, 325, 10, 320, 70, outline=c.body_color, fill='#F3C5C5')

# Feet
foot_left = c.create_oval(65, 320, 145, 360, outline=c.body_color, fill='#F3C5C5')
foot_right = c.create_oval(250, 320, 330, 360, outline=c.body_color, fill='#F3C5C5')

# Eyes and Pupils
eye_left = c.create_oval(130, 110, 160, 170, outline='#F2D7D5', fill='white')
pupil_left = c.create_oval(140, 145, 150, 155, outline='black', fill='black')
eye_right = c.create_oval(230, 110, 260, 170, outline='#F2D7D5', fill='white')
pupil_right = c.create_oval(240, 145, 250, 155, outline='black', fill='black')

# Mouth
mouth_normal = c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
mouth_happy = c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
mouth_sad = c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)

# Tongue
tongue_main = c.create_rectangle(170, 250, 230, 290, outline='red', fill='red', state=HIDDEN)
tongue_tip = c.create_oval(170, 285, 230, 300, outline='red', fill='red', state=HIDDEN)

# Cheeks
cheek_left = c.create_oval(70, 180, 120, 230, outline='pink', fill='pink', state=HIDDEN)
cheek_right = c.create_oval(280, 180, 330, 230, outline='pink', fill='pink', state=HIDDEN)

# Add all parts of the pet to a list for easy manipulation
pet_parts = [body, ear_left, ear_right, foot_left, foot_right, 
             eye_left, pupil_left, eye_right, pupil_right, 
             mouth_normal, mouth_happy, mouth_sad, 
             tongue_main, tongue_tip, cheek_left, cheek_right]

# Track roses and pet interaction state
c.rose_parts = []

# Pack the canvas to fill the window
c.pack(fill="both", expand=True)

# Update the window and center the pet
root.update_idletasks()  # Ensure canvas dimensions are updated
center_pet()  # Place the pet at the center

# Bind window resize event to adjust canvas size
root.bind("<Configure>", resize_canvas)

# Event binding for mouse interactions
c.bind('<ButtonPress-1>', start_move)  # Start moving when left mouse is pressed
c.bind('<B1-Motion>', move_pet)  # Move the pet while dragging
c.bind('<ButtonRelease-1>', stop_move)  # Stop moving when mouse button is released

# Start animations
root.after(1000, blink)

root.mainloop()
