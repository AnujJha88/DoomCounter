

# Doom Counter App


## Project Description

The Doom Counter App is a sleek, minimalist desktop countdown timer built with `customtkinter`. Designed to keep you focused on upcoming deadlines, events, or even just for fun, it provides a persistent, highly visible countdown to any date and time you set. Its animated flipping digits offer a unique visual flair, and its ability to minimize into a compact, always-on-top bar ensures your "doom date" is never out of sight.

Whether you're counting down to a product launch, an exam, a holiday, or the eventual heat death of the universe, the Doom Counter keeps the ticking seconds prominently displayed.

## Features

  * **Flipping Digit Animations:** Smooth, engaging animations for each digit as time progresses.
  * **Customizable Doom Date:** Easily set your own target date and time using a user-friendly picker.
  * **Compact "Minimize" Mode:** Shrinks the app to a slim, unobtrusive bar that stays on top of other windows, perfect for keeping an eye on the countdown without cluttering your workspace.
  * **Persistent Date Storage:** Your chosen doom date is automatically saved to a file (`doom_date.txt`), ensuring it's remembered even after closing and reopening the application.
  * **Interactive Window:** Drag the application window from anywhere (main window or minimized bar) to reposition it on your screen.
  * **Intuitive Controls:** Simple buttons for setting the date, minimizing/restoring, and closing the application.

## Installation

To get the Doom Counter App up and running on your system, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone git@github.com:AnujJha88/DoomCounter.git
    cd doom-counter-app
    ```

   

2.  **Install dependencies:**
    This project relies on `customtkinter`. Ensure you have Python installed (version 3.7 or newer recommended), then install the required library:

    ```bash
    pip install customtkinter
    ```

3.  **Run the application:**

    ```bash
    python main.py
    ```

    The application window should appear on your screen.

## How to Use

1.  **Initial Setup:** On first run, the app will default to a pre-set doom date (e.g., June 1, 2025).
2.  **Set Your Doom Date:**
      * Click the **"SET DATE"** button.
      * A new window will appear prompting for a date and time.
      * Enter the date in `YYYY-MM-DD` format (e.g., `2025-12-25`).
      * Enter the time in `HH:MM:SS` format (e.g., `23:59:59`).
      * Click Enter to confirm.
      * If you enter a date in the past, a warning will appear, but you can choose to proceed.
3.  **Minimize the App:**
    If the counter feels too distracting you can minimize it for the time being by:
      * Click the **"MINIMIZE"** button.
      * The main window will shrink to a compact, horizontal bar, typically appearing in the top-right corner of your screen. This bar remains always on top.
4.  **Restore the App:**
      * **Double-click** anywhere on the minimized bar.
      * Alternatively, click the **"RESTORE"** button that appears on the minimized bar.
      * The application will return to its full size.
5.  **Move the Window:**
      * Click and drag any part of the main application window (or the minimized bar) to reposition it on your screen.
6.  **Close the App:**
      * Click the **"X"** button in the top-right corner.
      * Alternatively, press the `Esc` key on your keyboard.

## Customization

The core appearance (colors, fonts, sizes) is defined within the `main.py` file. If you're comfortable with Python, you can modify:

  * **Colors:** Adjust `self.bg_color`, `self.fg_color`, `self.accent_color`, `self.text_color`, `self.button_bg` in the `DoomCounter` class.
  * **Fonts:** Change the `font` tuples assigned to labels (e.g., `('Consolas', 38, 'bold')`). Be mindful that large font sizes might cause display issues if the widget width is insufficient.
  * **Widget Sizes:** Modify the `width` and `height` parameters for `FlippingLabel` and `DigitFlipper` instances.

## Running on System Startup

To ensure your Doom Counter App launches automatically when your computer starts, follow the instructions for your specific operating system:

-----

### For Windows:

#### Method 1: Using the Startup Folder (Easiest for current user)

This method automatically launches the application for the currently logged-in user.

1.  Press `Win + R` on your keyboard to open the Run dialog.
2.  Type `shell:startup` and press `Enter`. This will open the Startup folder in File Explorer.
3.  Create a shortcut to your `main.py` file in this folder:
      * Right-click anywhere in the Startup folder, select "New" \> "Shortcut".
      * In the "Type the location of the item:" field, browse to the location of your `main.py` file (e.g., `C:\Users\YourUser\Documents\doom-counter-app\main.py`).
      * Click "Next", give your shortcut a descriptive name (e.g., "Doom Counter"), and click "Finish".

#### Method 2: Using Task Scheduler (More Robust & Flexible)

Task Scheduler allows for more control, such as running the application even if a user isn't logged in, or running it silently.

1.  Search for "Task Scheduler" in the Start menu and open it.
2.  In the right-hand "Actions" pane, click "Create Basic Task...".
3.  Follow the wizard, providing the following information:
      * **Name:** Give it a descriptive name (e.g., "Run Doom Counter on Startup").
      * **Trigger:** Choose "When the computer starts" (runs when the OS boots, before any user logs in) or "When I log on" (runs after you log in).
      * **Action:** Select "Start a program".
      * **Program/script:** Enter `pythonw.exe`. This executable runs Python scripts without displaying a console window.
          * *(If `pythonw.exe` is not in your system's PATH, you'll need to provide its full path, e.g., `C:\Python\Python39\pythonw.exe`.)*
      * **Add arguments (optional):** Enter the full path to your `main.py` file. **Crucially, enclose the path in double quotes if it contains spaces.**
          * Example: `"C:\Users\YourUser\Documents\doom-counter-app\main.py"`
      * **Start in (optional):** Enter the directory where your `main.py` file is located.
          * Example: `C:\Users\YourUser\Documents\doom-counter-app\`
4.  Click "Finish". For advanced options (like "Run whether user is logged on or not"), right-click the newly created task and go to "Properties".

-----

### For macOS:

#### Using Login Items

This method integrates the application into your macOS login process.

1.  Go to `System Settings` (for macOS Ventura and newer) or `System Preferences` (for older macOS versions).

2.  Click on `General` (or `Users & Groups` on older versions).

3.  Select `Login Items`.

4.  Click the `+` button at the bottom of the window.

5.  Navigate to your `main.py` file and select it.

      * **Note:** Sometimes, directly adding a `.py` file might not work as expected. If the application doesn't launch, you might need to create a small shell script to execute it:
        1.  Open a text editor (like TextEdit or VS Code) and create a new file.
        2.  Paste the following content into the file:
            ```bash
            #!/bin/bash
            /usr/local/bin/python3 /path/to/your/main.py &
            ```
            *(Replace `/usr/local/bin/python3` with the actual path to your Python executable, and `/path/to/your/main.py` with the full path to your script. The `&` runs it in the background.)*
        3.  Save the file with a `.sh` extension (e.g., `run_doom_counter.sh`) in a convenient location (e.g., in the `doom-counter-app` directory).
        4.  Open Terminal and make the script executable by running:
            ```bash
            chmod +x /path/to/your/run_doom_counter.sh
            ```
        5.  Now, add this `run_doom_counter.sh` file (the shell script) to your Login Items using the steps above.

-----

### For Linux:

#### Method 1: Using `cron` (Simple, User-Specific Startup)

`cron` is a time-based job scheduler in Unix-like operating systems. `@reboot` ensures the command runs once after each reboot.

1.  Open your terminal.
2.  Type `crontab -e` to edit your user's cron jobs. This will open a text editor (usually `vi` or `nano`).
3.  Add the following line to the end of the file:
    ```cron
    @reboot /usr/bin/python3 /path/to/your/main.py &
    ```
    *(Replace `/usr/bin/python3` with your actual Python executable path if different, and `/path/to/your/main.py` with the full path to your script. The `&` at the end runs the script in the background.)*
4.  Save and exit the crontab editor (for `nano`, press `Ctrl+X`, then `Y` to confirm, then `Enter`).

#### Method 2: Using `systemd` (Robust, System-Wide, Recommended for Modern Linux)

`systemd` is the standard system and service manager for many modern Linux distributions (like Ubuntu, Fedora, Debian, etc.). It provides a more robust way to manage startup services.

1.  Create a service file for your application. Open a terminal and use your preferred text editor to create a new file (e.g., `doomcounter.service`) in the `/etc/systemd/system/` directory:
    ```bash
    sudo nano /etc/systemd/system/doomcounter.service
    ```
2.  Paste the following content into the file:
    ```ini
    [Unit]
    Description=Doom Counter Application
    After=network.target graphical.target # Ensures network and graphical environment are up before starting

    [Service]
    ExecStart=/usr/bin/python3 /path/to/your/main.py
    WorkingDirectory=/path/to/your/
    StandardOutput=inherit  # Directs script's standard output to systemd journal
    StandardError=inherit   # Directs script's standard error to systemd journal
    Restart=always          # Automatically restarts the service if it crashes
    User=<your_username>    # Replace with your actual username
    # Group=<your_group>    # Optional: Uncomment and replace if you want to run it under a specific group

    [Install]
    WantedBy=multi-user.target # Ensures the service is started with the multi-user runlevel
    ```
    *(**Important:** Replace `/usr/bin/python3`, `/path/to/your/main.py`, `/path/to/your/` (the directory containing `main.py`), and `<your_username>` with your actual paths and username.)*
3.  Save and close the file.
4.  Reload `systemd` to recognize the new service:
    ```bash
    sudo systemctl daemon-reload
    ```
5.  Enable the service to start on boot:
    ```bash
    sudo systemctl enable doomcounter.service
    ```
6.  **(Optional, for immediate testing):** Start the service now without rebooting:
    ```bash
    sudo systemctl start doomcounter.service
    ```
7.  Check the service's status and logs:
    ```bash
    sudo systemctl status doomcounter.service
    journalctl -u doomcounter.service -f
    ```

-----

**General Important Notes for Startup Configuration:**

  * **Replace Placeholders:** Always ensure you replace all placeholder paths (e.g., `/path/to/your/main.py`, `/path/to/your/`, `/usr/bin/python3`) and your actual username (`<your_username>`) in the instructions above with the correct values for your system.
  * **Python Executable Path:** The path to your Python executable might vary depending on your installation (e.g., `python`, `python3`, `/usr/bin/python3`, `/usr/local/bin/python3`, or a path from your virtual environment if you're using one). You can usually find it by typing `which python` or `which python3` in your terminal.
  * **Permissions:** On Linux and macOS, ensure your script (`main.py`) and any shell scripts you create have execute permissions if required (`chmod +x script.sh`).

## Troubleshooting

  * **Application doesn't start or crashes:**
      * Check your Python installation and ensure `customtkinter` is installed correctly.
      * Verify that all file paths in your startup configuration (shortcuts, scripts, service files) are absolutely correct and point to the right files/directories.
      * If using `systemd` or `cron` on Linux, check the logs for errors. For `systemd`, use `journalctl -u your-service-name.service`.
  * **Window is not always on top:** Ensure the `self.attributes("-topmost", True)` line in `DoomCounter.__init__` is present and active. Some desktop environments might override this.

## Contributing

Contributions are welcome\! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE.md).

*(Consider creating a `LICENSE.md` file in your repository with the full text of the MIT License.)*

## Contact

If you have any questions or feedback, feel free to reach out:

  * **Your Name/Handle:** [Your Name or GitHub Handle]
  * **Email:** [Your Email Address (Optional)]

-----
