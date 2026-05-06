import tkinter as tk  # Standard Python interface to the Tk GUI toolkit
from tkinter import scrolledtext, Menu, filedialog  # Scrollable text widget, Menu, and file dialogs from tkinter
import threading  # Support for threading (concurrent execution)
import x_create  # Custom module for creating files, folders, or objects
import x_extract  # Custom module for extracting data or files
import sys  # Provides access to system-specific parameters and functions
import os  # OS-dependent functionality (file system operations)
import subprocess  # Running new applications or processes
import time  # Time-related functions
import shutil  # High-level operations on files and directories (e.g., deletion)
from translations import get_translations  # Import the function from translations.py

# Function to find resource paths when bundled with PyInstaller
def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and PyInstaller. """
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class XISOToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("360 Utility Batch Create Extract v1.2")
        self.root.geometry("600x738")
        self.root.configure(bg="brown")

        self.translations = get_translations()

        # Set the icon for the Tkinter window (try PNG first, fall back silently)
        try:
            icon_path = self.resource_path('images/360.ico')
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # Create the main layout
        self.create_widgets()

        # Redirect standard output to the status window
        self.original_stdout = sys.stdout
        sys.stdout = self

        self.update_texts()

    def resource_path(self, relative_path):
        """ Return the absolute path to a resource. """
        import os
        import sys
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def update_texts(self):
        tr = self.translations["English"]
        self.root.title(tr["title"])
        self.title_label.config(text=tr["title"])
        self.author_label.config(text=tr["author"])
        self.extract_btn.config(text=tr["extract"])
        self.create_btn.config(text=tr["create"])
        self.extract_delete_btn.config(text=tr["extract_delete"])
        self.delete_source_folders_btn.config(text=tr["delete"])
        self.fix_iso_btn.config(text=tr["fix_iso"])
        self.isotogod_btn.config(text=tr["iso2god"])
        self.godtoiso_btn.config(text=tr["god2iso"])
        self.help_btn.config(text=tr["help"])
    
    def create_widgets(self):
        # Create menu bar
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        self.menubar = menubar

        # Title and author labels at the top
        self.title_label = tk.Label(self.root, text="360 Utility Batch Create Extract v1.2", font=("Helvetica", 16), fg="gold", bg="brown")
        self.title_label.pack(pady=10)

        self.author_label = tk.Label(self.root, text="BY: BLAHPR 2024", font=("Helvetica", 12), fg="gold", bg="brown")
        self.author_label.pack(pady=1)

        # Buttons arranged in the middle
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=10, fill=tk.X)

        # Define a font variable for bold text
        bold_font = ("Helvetica", 12, "bold")

        self.extract_btn = tk.Button(button_frame, text="Extract Game Folders from ISOS", command=self.extract_xiso, bg="lightblue", fg="blue", font=bold_font)
        self.extract_btn.pack(pady=5, fill=tk.X, padx=20)

        self.create_btn = tk.Button(button_frame, text="Create ISOS from Game Folders", command=self.create_xiso, bg="lightgreen", fg="green", font=bold_font)
        self.create_btn.pack(pady=5, fill=tk.X, padx=20)

        self.extract_delete_btn = tk.Button(button_frame, text="Extract and Delete ISO Files  !!! >PERMANENTLY< !!!", command=self.extract_delete_xiso, bg="#FF0000", fg="yellow", font=bold_font)
        self.extract_delete_btn.pack(pady=5, fill=tk.X, padx=20)

        # New button to delete source folders
        self.delete_source_folders_btn = tk.Button(button_frame, text="Delete Game Folders  !!! >PERMANENTLY< !!!", command=self.delete_source_folders, bg="#FF0000", fg="yellow", font=bold_font)
        self.delete_source_folders_btn.pack(pady=5, fill=tk.X, padx=20)

        # Buttons to run native Linux tools
        self.fix_iso_btn = tk.Button(button_frame, text="Fix ISO (abgx360)", command=self.run_fix_iso, bg="#00569D", fg="darkorange", font=bold_font)
        self.fix_iso_btn.pack(pady=5, fill=tk.X, padx=20)

        self.isotogod_btn = tk.Button(button_frame, text="ISO to GOD (GAMES ON DEMAND)", command=self.run_iso2god, bg="#00569D", fg="darkorange", font=bold_font)
        self.isotogod_btn.pack(pady=5, fill=tk.X, padx=20)

        self.godtoiso_btn = tk.Button(button_frame, text="GOD to ISO (GAMES ON DEMAND)", command=self.run_god2iso, bg="#00569D", fg="darkorange", font=bold_font)
        self.godtoiso_btn.pack(pady=5, fill=tk.X, padx=20)

        self.help_btn = tk.Button(button_frame, text=">Help / ReadMe<", command=self.show_help, bg="crimson", fg="white", font=bold_font)
        self.help_btn.pack(pady=5, fill=tk.X, padx=20)

        # Status window at the bottom
        status_frame = tk.Frame(self.root, bg="black")
        status_frame.pack(expand=True, fill=tk.BOTH, pady=10, padx=20)

        self.status_text = tk.Text(status_frame, bg="black", fg="white", wrap=tk.WORD)
        self.status_text.pack(expand=True, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)

        # Add help content display area
        self.help_text_area = tk.Text(self.root, bg="lightgrey", fg="black", wrap=tk.WORD, height=15)
        self.help_text_area.pack(pady=10, padx=10, fill=tk.BOTH)
        self.help_text_area.config(state=tk.DISABLED)

    def clear_status(self):
        """ Clear the status text window. """
        self.status_text.delete('1.0', tk.END)

    def create_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_create_xiso).start()

    def run_create_xiso(self):
        x_create.create_xiso_from_directories()

    def extract_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_extract_xiso, args=(False,)).start()

    def extract_delete_xiso(self):
        self.clear_status()
        threading.Thread(target=self.run_extract_xiso, args=(True,)).start()

    def run_extract_xiso(self, delete_after):
        x_extract.extract_xiso_from_files(delete_after)

    def update_status(self, message):
        """ Update the status text window with a message. """
        # Ensure the message does not repeat if already present
        if not self.status_text.get('1.0', tk.END).strip().endswith(message.strip()):
            self.status_text.insert(tk.END, message + "\n")          
            
    def write(self, message):
        self.status_text.insert(tk.END, message)
        self.status_text.see(tk.END)

    def flush(self):
        pass

    def show_help(self):
        # Create a new help window
        help_window = tk.Toplevel(self.root)
        help_window.title(">Help / ReadMe<")
        help_window.geometry("760x825")  # Set the size of the window
        help_window.configure(bg="brown")

        # Set the icon for the help window
        try:
            help_window.iconbitmap(self.resource_path('images/360.ico'))
        except Exception:
            pass

        # Create a text widget for displaying help content
        text_widget = tk.Text(help_window, bg="lightgrey", fg="black", wrap=tk.WORD, font=("Helvetica", 13, "bold"))
        text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Add scrollbars to the text widget
        scrollbar_y = tk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(help_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=scrollbar_x.set)

        # Insert the help text into the text widget
        content = self.translations["English"]["help_text"]

        # Insert the help text into the text widget
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only

    def run_fix_iso(self):
        self.clear_status()
        iso_file = filedialog.askopenfilename(
            title="Select ISO to fix with abgx360",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        if not iso_file:
            self.update_status("Cancelled.")
            return
        self.update_status(f"Fix ISO (abgx360)\nFile: {iso_file}\n\nRunning abgx360 AutoFix (level 3) + video padding fix...\n")
        threading.Thread(target=self.execute_fix_iso, args=(iso_file,)).start()

    def execute_fix_iso(self, iso_file):
        tool = self.resource_path('x_tool/abgx360')
        try:
            proc = subprocess.Popen(
                [tool, '--af3', '-p', '-s', '-o', '--', iso_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in proc.stdout:
                self.update_status(line.rstrip())
            proc.wait()
            if proc.returncode == 0:
                self.update_status("\nDone. ISO fixed successfully.")
            else:
                self.update_status(f"\nabgx360 exited with code {proc.returncode}.")
        except Exception as e:
            self.update_status(f"Failed to run abgx360: {e}")

    def run_iso2god(self):
        self.clear_status()
        iso_file = filedialog.askopenfilename(
            title="Select ISO file to convert to GOD",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        if not iso_file:
            self.update_status("Cancelled.")
            return
        output_dir = filedialog.askdirectory(title="Select output folder for GOD files")
        if not output_dir:
            self.update_status("Cancelled.")
            return
        self.update_status(f"ISO to GOD\nSource: {iso_file}\nOutput: {output_dir}\n\nConverting...")
        threading.Thread(target=self.execute_iso2god, args=(iso_file, output_dir)).start()

    def execute_iso2god(self, iso_file, output_dir):
        tool = self.resource_path('x_tool/iso2god')
        try:
            result = subprocess.run(
                [tool, iso_file, output_dir],
                capture_output=True, text=True
            )
            self.update_status(result.stdout)
            if result.returncode != 0:
                self.update_status(f"Error:\n{result.stderr}")
            else:
                self.update_status("\nDone. GOD files written to output folder.")
        except Exception as e:
            self.update_status(f"Failed to run iso2god: {e}")

    def run_god2iso(self):
        self.clear_status()
        god_file = filedialog.askopenfilename(
            title="Select GOD package file (the file without extension, not the .data folder)",
            filetypes=[("All files", "*.*")]
        )
        if not god_file:
            self.update_status("Cancelled.")
            return
        output_dir = filedialog.askdirectory(title="Select output folder for ISO")
        if not output_dir:
            self.update_status("Cancelled.")
            return
        self.update_status(f"GOD to ISO\nSource: {god_file}\nOutput: {output_dir}\n\nConverting...")
        threading.Thread(target=self.execute_god2iso, args=(god_file, output_dir)).start()

    def execute_god2iso(self, god_file, output_dir):
        tool = self.resource_path('x_tool/god2iso')
        try:
            result = subprocess.run(
                [tool, god_file, output_dir],
                capture_output=True, text=True
            )
            self.update_status(result.stdout)
            if result.returncode != 0:
                self.update_status(f"Error:\n{result.stderr}")
            else:
                self.update_status("\nDone. ISO written to output folder.")
        except Exception as e:
            self.update_status(f"Failed to run god2iso: {e}")

    def delete_source_folders(self):
        self.clear_status()
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))  # Get directory of the executable
        
        # Exclude specific folders
        excluded_folders = ["x_tool", "x_ISO"]
        
        # Flag to check if any folder was deleted
        deleted_any_folders = False
        
        for folder_name in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder_name)
            
            # Check if it's a directory and not in the excluded list
            if os.path.isdir(folder_path) and folder_name not in excluded_folders:
                # Check if the folder contains .xex or .xbe files
                contains_target_files = any(
                    filename.endswith(('.xex', '.xbe')) for filename in os.listdir(folder_path)
                )
                
                if contains_target_files:
                    try:
                        shutil.rmtree(folder_path)  # Remove the folder and all its contents
                        self.update_status(f"\nDELETING: \n{folder_name}\n")
                        self.update_status("DONE.")
                        deleted_any_folders = True
                    except Exception as e:
                        self.update_status(f"\nFailed to delete folder {folder_name}: {e}\n")
        
        # Check if no folders were deleted
        if not deleted_any_folders:
            self.update_status("\nNO GAME FOLDERS TO DELETE")
        else:
            self.update_status("DONE.")
    
def main():
    root = tk.Tk()
    app = XISOToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
