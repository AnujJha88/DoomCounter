import customtkinter as ctk
from datetime import datetime, timedelta
import os
from tkinter import messagebox
import math
import pystray  # For system tray icon
from PIL import Image, ImageDraw, ImageFont
import threading

class FlippingLabel(ctk.CTkFrame):
    """
    A custom widget that displays a flipping animation for a single digit.
    It simulates a card flipping from one digit to the next.
    """
    def __init__(self, master, width=60, height=80, font=('Consolas', 42, 'bold'), **kwargs):
        super().__init__(master, fg_color="transparent", width=width, height=height, **kwargs)
        
        self.width = width
        self.height = height
        self.font = font
        self.current_value = "0"
        self.next_value = "0"
        
        # The static top half of the current card
        self.top_half = ctk.CTkLabel(
            self, 
            text=self.current_value, 
            font=self.font,
            width=width,
            height=height//2,
            corner_radius=5,
            fg_color="#2b2b2b",
            text_color="#ff4d4d"
        )
        self.top_half.place(x=0, y=0)
        
        # The static bottom half of the current card
        self.bottom_half = ctk.CTkLabel(
            self, 
            text=self.current_value, 
            font=self.font,
            width=width,
            height=height//2,
            corner_radius=5,
            fg_color="#333333",
            text_color="#ff4d4d"
        )
        self.bottom_half.place(x=0, y=height//2)

        # The flipping card (initially hidden)
        # This card will flip from the current value's top half to the next value's top half
        self.top_flipping_card = ctk.CTkLabel(
            self,
            text=self.current_value,
            font=self.font,
            width=width,
            height=height // 2,
            corner_radius=5,
            fg_color="#2b2b2b",
            text_color="#ff4d4d"
        )
        # Place it initially off-screen or hidden until animation starts
        self.top_flipping_card.place(x=0, y=0)
        self.top_flipping_card.lower() # Place it behind top_half initially
        
        # Animation variables
        self.animation_step = 0 # Angle for the flip (0 to 180)
        self.animation_speed = 15 # Speed of the animation
        self.is_animating = False
        
    def set_value(self, new_value):
        """
        Sets the new value for the label and initiates the flip animation if different.
        """
        if new_value != self.current_value and not self.is_animating:
            self.next_value = new_value
            self.animate_flip()
        elif new_value == self.current_value and not self.is_animating:
            # If value is the same and not animating, ensure display is correct
            self.top_half.configure(text=self.current_value)
            self.bottom_half.configure(text=self.current_value)
            self.top_flipping_card.configure(text=self.current_value)
            self.top_flipping_card.lower() # Ensure it's hidden
    
    def animate_flip(self):
        """
        Prepares the labels for the flipping animation.
        """
        self.is_animating = True
        self.animation_step = 0
        
        # Set the static top half to the current value
        self.top_half.configure(text=self.current_value)
        # Set the static bottom half to the next value (will be revealed)
        self.bottom_half.configure(text=self.next_value)
        
        # The flipping card starts showing the current value's top half
        self.top_flipping_card.configure(text=self.current_value)
        self.top_flipping_card.place(x=0, y=0)
        self.top_flipping_card.lift() # Bring to front for animation
        
        self.animate()
    
    def animate(self):
        """
        Performs the frame-by-frame animation of the flipping card.
        """
        if self.animation_step <= 180: # Flip from 0 to 180 degrees
            angle = self.animation_step
            self.animation_step += self.animation_speed
            
            # Calculate perspective scale for the flipping card
            # Scale goes from 1 down to 0 and back to 1
            scale = math.cos(math.radians(angle))
            height = max(1, int((self.height / 2) * abs(scale)))
            
            if angle <= 90:
                # First half of the flip: top card flips down, revealing its back (which is the bottom_half of the next value)
                self.top_flipping_card.configure(text_color="#ff4d4d", fg_color="#2b2b2b") # Front side color
                self.top_flipping_card.configure(height=height)
                self.top_flipping_card.place_configure(y=0)
                self.top_flipping_card.lift()
            else:
                # Second half of the flip: top card continues flipping, now showing the next value's top half
                # It appears to come up from the bottom, but it's actually just the top_flipping_card changing its text
                self.top_flipping_card.configure(text=self.next_value)
                self.top_flipping_card.configure(text_color="#ff4d4d", fg_color="#2b2b2b") # Back side color
                self.top_flipping_card.configure(height=height)
                self.top_flipping_card.place_configure(y=self.height - height) # Adjust y to simulate flipping up
                self.top_flipping_card.lift()

            self.after(20, self.animate) # Continue animation
        else:
            # Animation complete
            self.current_value = self.next_value
            self.top_half.configure(text=self.current_value)
            self.bottom_half.configure(text=self.current_value)
            self.top_flipping_card.lower() # Hide the flipping card
            self.is_animating = False

class DoomCounter(ctk.CTk):
    """
    Main application class for the Doom Counter.
    Displays a countdown to a specified date and time.
    """
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Doom Counter")
        self.attributes("-topmost", True)  # Keep window on top
        self.overrideredirect(True)  # Remove window decorations (title bar, borders)
        
        # Window state
        self.is_hidden = False
        self.normal_geometry = "500x300+100+100"  # Store the normal window size
        self.hidden_geometry = "200x50+100+100"   # Store the minimized window size
        
        # Set theme and colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Custom colors
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ff4d4d"
        self.accent_color = "#ff1a1a"
        self.text_color = "#ffffff"
        self.button_bg = "#2b2b2b"
        
        # Configure window background color
        self.geometry(self.normal_geometry)
        self.configure(fg_color=self.bg_color)
        
        # Create minimized frame (initially hidden)
        self.minimized_frame = ctk.CTkFrame(self, fg_color=self.accent_color, width=200, height=50)
        self.minimized_frame.pack_propagate(False)
        
        # Container for minimized content
        self.minimized_content = ctk.CTkFrame(self.minimized_frame, fg_color="transparent")
        self.minimized_content.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left side - Title
        self.minimized_title = ctk.CTkLabel(
            self.minimized_content, 
            text="DOOM:",
            text_color=self.text_color,
            font=('Arial', 12, 'bold'),
            anchor='w'
        )
        self.minimized_title.pack(side='left', padx=(5,0))
        
        # Middle - Countdown display
        self.minimized_time = ctk.CTkLabel(
            self.minimized_content,
            text="00d 00:00:00",
            text_color=self.text_color,
            font=('Consolas', 12, 'bold'),
            width=120
        )
        self.minimized_time.pack(side='left', padx=5, fill='x', expand=True)
        
        # Right side - Restore button
        self.restore_btn = ctk.CTkButton(
            self.minimized_content,
            text="RESTORE",
            command=self.toggle_hide_show,
            fg_color="#2b2b2b",  # Dark gray background
            hover_color="#3a3a3a",  # Slightly lighter on hover
            text_color="#ffffff",  # White text
            border_color="#4a4a4a",  # Border color
            border_width=1,  # Thin border
            width=70,
            height=28,  # Slightly smaller height
            corner_radius=4,  # Slightly rounded corners
            font=('Arial', 9, 'bold')
        )
        self.restore_btn.pack(side='right', padx=(0,5), pady=2)
        
        # Main container frame (for normal view)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Load or set doom date
        self.doom_date_str = "2025-06-01 00:00:00" # Default doom date
        self.load_or_set_doom_date()
        
        # Date display frame
        self.date_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.date_frame.pack(fill='x', pady=(0, 10))
        
        self.date_label = ctk.CTkLabel(
            self.date_frame, 
            text="DOOM DATE: ",
            text_color=self.text_color,
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        self.date_label.pack(side='left')
        
        self.date_display = ctk.CTkLabel(
            self.date_frame, 
            text=self.doom_date_str,
            text_color=self.fg_color,
            font=('Arial', 10, 'bold'),
            anchor='w'
        )
        self.date_display.pack(side='left', fill='x', expand=True)
        
        # Countdown display frame
        self.countdown_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.countdown_frame.pack(fill='both', expand=True, pady=10)
        
        # Container for the flipping card frames
        self.card_container = ctk.CTkFrame(self.countdown_frame, fg_color="transparent")
        self.card_container.pack(expand=True)
        
        # Initialize flipping card labels for Days, Hours, Minutes, Seconds
        self.days_label = FlippingLabel(self.card_container, width=80, height=100)
        self.days_label.pack(side='left', padx=5)
        
        self.hours_label = FlippingLabel(self.card_container, width=80, height=100)
        self.hours_label.pack(side='left', padx=5)
        
        self.minutes_label = FlippingLabel(self.card_container, width=80, height=100)
        self.minutes_label.pack(side='left', padx=5)
        
        self.seconds_label = FlippingLabel(self.card_container, width=80, height=100)
        self.seconds_label.pack(side='left', padx=5)
        
        # Time unit labels (DAYS, HOURS, etc.)
        units_frame = ctk.CTkFrame(self.countdown_frame, fg_color="transparent")
        units_frame.pack(fill='x', pady=(5, 0))
        
        unit_font = ('Arial', 10, 'bold')
        ctk.CTkLabel(units_frame, text="DAYS", font=unit_font, text_color=self.text_color).pack(side='left', padx=28, expand=True)
        ctk.CTkLabel(units_frame, text="HOURS", font=unit_font, text_color=self.text_color).pack(side='left', padx=28, expand=True)
        ctk.CTkLabel(units_frame, text="MINUTES", font=unit_font, text_color=self.text_color).pack(side='left', padx=15, expand=True)
        ctk.CTkLabel(units_frame, text="SECONDS", font=unit_font, text_color=self.text_color).pack(side='left', padx=15, expand=True)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        # Buttons
        self.set_date_btn = ctk.CTkButton(
            self.button_frame,
            text="SET DATE",
            command=self.show_date_picker,
            fg_color=self.button_bg,
            hover_color=self.accent_color,
            width=100,
            height=30,
            corner_radius=5,
            font=('Arial', 10, 'bold')
        )
        self.set_date_btn.pack(side='left', padx=5)
        
        self.hide_btn = ctk.CTkButton(
            self.button_frame,
            text="MINIMIZE",
            command=self.toggle_hide_show,
            fg_color=self.button_bg,
            hover_color=self.accent_color,
            width=100,
            height=30,
            corner_radius=5,
            font=('Arial', 10, 'bold')
        )
        self.hide_btn.pack(side='left', padx=5)
        
        self.close_btn = ctk.CTkButton(
            self.button_frame,
            text="X",
            command=self.destroy,
            fg_color="#ff4d4d",
            hover_color="#ff1a1a",
            width=30,
            height=30,
            corner_radius=15,
            font=('Arial', 12, 'bold')
        )
        self.close_btn.pack(side='right')
        
        # Event bindings for dragging and closing
        self.bind("<Escape>", lambda e: self.destroy()) # Close on Escape key
        self.bind("<ButtonPress-1>", self.on_press_drag) # Start drag on left mouse button press
        self.bind("<B1-Motion>", self.on_drag) # Continue drag on mouse motion with left button held
        
        # Start the countdown update loop
        self.update_countdown()
    
    def load_or_set_doom_date(self):
        """
        Loads the doom date from a file or sets a default if not found/invalid.
        """
        try:
            # Try to load from file
            if os.path.exists('doom_date.txt'):
                with open('doom_date.txt', 'r') as f:
                    self.doom_date_str = f.read().strip()
            self.doom_date = datetime.strptime(self.doom_date_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, FileNotFoundError):
            # Default to 7 days from now if error
            self.doom_date = datetime.now() + timedelta(days=7)
            self.doom_date_str = self.doom_date.strftime("%Y-%m-%d %H:%M:%S")
    
    def save_doom_date(self):
        """
        Saves the current doom date to a file.
        """
        with open('doom_date.txt', 'w') as f:
            f.write(self.doom_date_str)
    
    def show_date_picker(self):
        """
        Displays a Toplevel window for setting the doom date and time.
        """
        date_picker = ctk.CTkToplevel(self)
        date_picker.title("Set Doom Date")
        date_picker.attributes("-topmost", True)
        date_picker.resizable(False, False)
        date_picker.grab_set() # Make this window modal
        
        # Center the date picker window
        window_width = 350
        window_height = 220
        x = (self.winfo_screenwidth() - window_width) // 2
        y = (self.winfo_screenheight() - window_height) // 2
        date_picker.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Date Entry
        date_frame = ctk.CTkFrame(date_picker, fg_color="transparent")
        date_frame.pack(pady=(20, 10), padx=20, fill='x')
        
        ctk.CTkLabel(date_frame, text="DATE (YYYY-MM-DD):").pack(anchor='w')
        date_entry = ctk.CTkEntry(date_frame, width=300, height=35, font=('Arial', 12))
        date_entry.pack(pady=(5, 10))
        date_entry.insert(0, self.doom_date.strftime("%Y-%m-%d"))
        
        # Time Entry
        time_frame = ctk.CTkFrame(date_picker, fg_color="transparent")
        time_frame.pack(pady=(0, 20), padx=20, fill='x')
        
        ctk.CTkLabel(time_frame, text="TIME (HH:MM:SS):").pack(anchor='w')
        time_entry = ctk.CTkEntry(time_frame, width=300, height=35, font=('Arial', 12))
        time_entry.pack(pady=(5, 10))
        time_entry.insert(0, self.doom_date.strftime("%H:%M:%S"))
        
        # Buttons
        btn_frame = ctk.CTkFrame(date_picker, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        def set_date():
            """Callback function to set the doom date from the entry fields."""
            self.set_doom_date(f"{date_entry.get()} {time_entry.get()}")
            date_picker.destroy()
        
        ctk.CTkButton(
            btn_frame,
            text="SET DATE",
            command=set_date,
            width=120,
            height=35,
            corner_radius=5,
            font=('Arial', 12, 'bold')
        ).pack(side='left', padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="CANCEL",
            command=date_picker.destroy,
            width=120,
            height=35,
            corner_radius=5,
            fg_color="#444444",
            hover_color="#333333",
            font=('Arial', 12, 'bold')
        ).pack(side='left')
        
        date_entry.focus()
        date_entry.select_range(0, 'end')
        date_entry.bind('<Return>', lambda e: set_date())
        time_entry.bind('<Return>', lambda e: set_date())
    
    def set_doom_date(self, date_time_str):
        """
        Sets the doom date based on the provided string and handles validation.
        """
        try:
            new_date = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            if new_date <= datetime.now():
                # Using messagebox for confirmation as it's a Toplevel window
                if not messagebox.askyesno("Warning", "The selected date is in the past. Continue?"):
                    return
            
            self.doom_date = new_date
            self.doom_date_str = date_time_str
            self.date_display.configure(text=date_time_str)
            self.save_doom_date()
            
            # Force update the display to reflect new date immediately
            self.update_display()
            
        except ValueError as e:
            messagebox.showerror("Error", "Invalid date/time format.\nPlease use YYYY-MM-DD HH:MM:SS\nExample: 2025-12-25 23:59:59")
    
    def toggle_hide_show(self, event=None):
        """Toggle between showing and hiding the window"""
        if self.is_hidden:
            # Restore the window
            self.overrideredirect(True)
            self.main_frame.pack(fill='both', expand=True, padx=20, pady=15)
            self.minimized_frame.pack_forget()
            self.geometry(self.normal_geometry)
            self.is_hidden = False
        else:
            # Save current position and minimize
            x, y = self.winfo_x(), self.winfo_y()
            self.normal_geometry = self.geometry()  # Save current size/position
            self.hidden_geometry = f"200x50+{x}+{y}"
            
            # Show minimized frame
            self.main_frame.pack_forget()
            self.minimized_frame.pack(fill='both', expand=True)
            self.overrideredirect(False)  # Show title bar when minimized
            self.geometry(self.hidden_geometry)
            self.is_hidden = True
            self.lift()
            
    def update_display(self):
        """
        Calculates the time left and updates the flipping labels.
        """
        try:
            now = datetime.now()
            time_left = self.doom_date - now
            
            # Format time left as days, hours, minutes, seconds
            if time_left.total_seconds() <= 0:
                time_str = "DOOMSDAY!"
            else:
                days = time_left.days
                seconds = time_left.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                time_str = f"{days:02d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Update minimized window display
            if self.is_hidden:
                self.minimized_time.configure(text=time_str)
            
            # If countdown is over
            if time_left.total_seconds() <= 0:
                self.days_label.set_value("00")
                self.hours_label.set_value("00")
                self.minutes_label.set_value("00")
                self.seconds_label.set_value("00")
                return
            
            # Calculate time components
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Update cards with animation
            # Ensure two digits for each value
            self.days_label.set_value(f"{days:02d}")
            self.hours_label.set_value(f"{hours:02d}")
            self.minutes_label.set_value(f"{minutes:02d}")
            self.seconds_label.set_value(f"{seconds:02d}")
            
        except Exception as e:
            print(f"Error updating display: {e}")
    
    def update_countdown(self):
        """
        Schedules the update_display function to run every second.
        """
        self.update_display()
        self.after(1000, self.update_countdown) # Call itself after 1 second
    
    def on_press_drag(self, event):
        """
        Stores the initial mouse position when a drag starts.
        """
        # Bind to the entire window for dragging
        self._drag_start_x = event.x_root - self.winfo_x()
        self._drag_start_y = event.y_root - self.winfo_y()
    
    def on_drag(self, event):
        """
        Moves the window as the mouse is dragged.
        """
        if hasattr(self, '_drag_start_x') and hasattr(self, '_drag_start_y'):
            x = event.x_root - self._drag_start_x
            y = event.y_root - self._drag_start_y
            self.geometry(f"+{x}+{y}")
            # Update hidden position if we're in hidden state to maintain relative position
            if self.is_hidden:
                self.hidden_geometry = f"200x50+{x}+{y}"

if __name__ == "__main__":
    app = DoomCounter()
    app.mainloop()
