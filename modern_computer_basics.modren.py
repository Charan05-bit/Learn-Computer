import tkinter as tk
from tkinter import ttk, font, filedialog
from tkinter import messagebox
import os

class ComputerBasicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Basics Tutorial")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Practice session variables
        self.practice_active = False
        self.current_practice_step = 0
        self.practice_file_path = ""
        self.practice_completed_steps = set()
        
        # Theme variables
        self.dark_mode = False
        self.themes = {
            'light': {
                'bg': '#f5f5f5',
                'text_bg': '#ffffff',
                'text_fg': '#333333',
                'button_bg': '#4a7a8c',
                'button_fg': 'white',
                'button_active': '#3a6a7c',
                'highlight': '#e1f5fe',
                'header_bg': '#4a7a8c',
                'header_fg': 'white',
                'success': '#4caf50',
                'warning': '#ff9800'
            },
            'dark': {
                'bg': '#2d2d2d',
                'text_bg': '#3d3d3d',
                'text_fg': '#e0e0e0',
                'button_bg': '#5a8a9c',
                'button_fg': 'white',
                'button_active': '#4a7a8c',
                'highlight': '#1a3a4a',
                'header_bg': '#3a5a6c',
                'header_fg': 'white',
                'success': '#388e3c',
                'warning': '#f57c00'
            }
        }
        
        # Fonts
        self.title_font = font.Font(family='Segoe UI', size=24, weight='bold')
        self.subtitle_font = font.Font(family='Segoe UI', size=12)
        self.button_font = font.Font(family='Segoe UI', size=12)
        self.text_font = font.Font(family='Segoe UI', size=13)
        self.practice_font = font.Font(family='Segoe UI', size=12, weight='bold')
        
        # Create UI elements
        self.create_widgets()
        self.apply_theme()
        
        # Show welcome message
        self.show_welcome_message()
    
    def create_widgets(self):
        # Create main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header frame
        self.header_frame = tk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(
            self.header_frame,
            text="Computer Basics Tutorial",
            font=self.title_font
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        self.theme_button = tk.Button(
            self.header_frame,
            text="☀️",
            command=self.toggle_theme,
            font=("Segoe UI", 14),
            bd=0,
            relief=tk.FLAT
        )
        self.theme_button.pack(side=tk.RIGHT, padx=5)
        
        # Subtitle label
        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Learn essential computer skills",
            font=self.subtitle_font
        )
        self.subtitle_label.pack(side=tk.LEFT, padx=10)
        
        # Content frame
        self.content_frame = tk.Frame(self.main_container)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Left panel for buttons
        self.left_panel = tk.Frame(self.content_frame, width=200)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.left_panel.pack_propagate(False)
        
        # Right panel for content
        self.right_panel = tk.Frame(self.content_frame)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create buttons
        self.create_buttons()
        
        # Create text display
        self.create_text_display()
        
        # Create practice panel (initially hidden)
        self.create_practice_panel()
    
    def create_practice_panel(self):
        # Practice container
        self.practice_container = tk.Frame(self.right_panel)
        
        # Practice instructions
        self.practice_instructions = tk.Label(
            self.practice_container,
            font=self.practice_font,
            wraplength=600,
            justify=tk.LEFT
        )
        self.practice_instructions.pack(fill=tk.X, pady=(0, 10))
        
        # Practice editor frame
        self.editor_frame = tk.Frame(self.practice_container)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text editor
        self.practice_editor = tk.Text(
            self.editor_frame,
            wrap=tk.WORD,
            font=self.text_font,
            padx=10,
            pady=10,
            undo=True
        )
        self.practice_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Editor scrollbar
        editor_scroll = ttk.Scrollbar(self.editor_frame)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.practice_editor.config(yscrollcommand=editor_scroll.set)
        editor_scroll.config(command=self.practice_editor.yview)
        
        # Bind keyboard shortcuts for practice
        self.practice_editor.bind('<Control-s>', lambda e: self.check_practice_step('save'))
        self.practice_editor.bind('<Control-c>', lambda e: self.check_practice_step('copy'))
        self.practice_editor.bind('<Control-v>', lambda e: self.check_practice_step('paste'))
        self.practice_editor.bind('<Control-z>', lambda e: self.check_practice_step('undo'))
        
        # Practice controls frame
        self.controls_frame = tk.Frame(self.practice_container)
        self.controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Save button
        self.save_button = tk.Button(
            self.controls_frame,
            text="Save File (Ctrl+S)",
            command=lambda: self.check_practice_step('save'),
            font=self.button_font,
            width=15
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # New file button
        self.new_file_button = tk.Button(
            self.controls_frame,
            text="New File",
            command=self.start_practice_session,
            font=self.button_font,
            width=10
        )
        self.new_file_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.practice_status = tk.Label(
            self.controls_frame,
            text="",
            font=self.text_font
        )
        self.practice_status.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        
        # Progress bar
        self.practice_progress = ttk.Progressbar(
            self.controls_frame,
            orient=tk.HORIZONTAL,
            mode='determinate',
            length=100
        )
        self.practice_progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_buttons(self):
        # Button container
        self.button_container = tk.Frame(self.left_panel)
        self.button_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Lesson buttons
        lessons = [
            ("🖱️ Using Mouse & Keyboard", self.show_mouse_keyboard),
            ("📁 Create a Folder", self.show_create_folder),
            ("📝 Create Text File", self.show_create_text_file),
            ("⌨️ Shortcut Keys", self.show_shortcut_keys),
            ("📖 Terminology", self.show_terminology),
            ("❓ Getting Help", self.show_getting_help),
            ("💻 Practice Session", self.start_practice_session)
        ]
        
        for text, command in lessons:
            btn = tk.Button(
                self.button_container,
                text=text,
                command=command,
                font=self.button_font,
                anchor=tk.W,
                bd=0,
                relief=tk.FLAT,
                padx=15
            )
            btn.pack(fill=tk.X, pady=3, ipady=8)
            self.style_button(btn)
        
        # Exit button
        exit_btn = tk.Button(
            self.button_container,
            text="🚪 Exit",
            command=self.root.quit,
            font=self.button_font,
            anchor=tk.W,
            bd=0,
            relief=tk.FLAT,
            padx=15
        )
        exit_btn.pack(fill=tk.X, pady=(20, 5), ipady=8)
        self.style_button(exit_btn, True)
    
    def style_button(self, button, is_exit=False):
        theme = self.themes['dark'] if self.dark_mode else self.themes['light']
        bg = '#8c4a4a' if is_exit else theme['button_bg']
        active_bg = '#7c3a3a' if is_exit else theme['button_active']
        
        button.config(
            bg=bg,
            fg=theme['button_fg'],
            activebackground=active_bg,
            activeforeground=theme['button_fg']
        )
        
        # Bind hover effects
        button.bind("<Enter>", lambda e, b=button: b.config(bg=active_bg))
        button.bind("<Leave>", lambda e, b=button, bg=bg: b.config(bg=bg))
    
    def create_text_display(self):
        # Text container with shadow effect
        self.text_container = tk.Frame(
            self.right_panel,
            bd=0,
            relief=tk.FLAT,
            bg='#aaaaaa'
        )
        self.text_container.pack(fill=tk.BOTH, expand=True, padx=(0, 5), pady=(0, 5))
        
        # Actual text frame
        self.text_frame = tk.Frame(
            self.text_container,
            bd=0,
            relief=tk.FLAT
        )
        self.text_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 0), pady=(5, 0))
        
        # Text widget
        self.text_display = tk.Text(
            self.text_frame,
            wrap=tk.WORD,
            font=self.text_font,
            padx=20,
            pady=20,
            spacing1=8,
            spacing3=4,
            bd=0,
            highlightthickness=0
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.text_display)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_display.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_display.yview)
        
        # Disable text editing
        self.text_display.config(state=tk.DISABLED)
    
    def apply_theme(self):
        theme = self.themes['dark'] if self.dark_mode else self.themes['light']
        
        # Update theme button
        self.theme_button.config(text="🌙" if self.dark_mode else "☀️")
        
        # Apply colors
        self.root.config(bg=theme['bg'])
        self.main_container.config(bg=theme['bg'])
        self.header_frame.config(bg=theme['header_bg'])
        self.title_label.config(bg=theme['header_bg'], fg=theme['header_fg'])
        self.subtitle_label.config(bg=theme['header_bg'], fg=theme['header_fg'])
        self.theme_button.config(
            bg=theme['header_bg'],
            fg=theme['header_fg'],
            activebackground=theme['header_bg'],
            activeforeground=theme['header_fg']
        )
        self.content_frame.config(bg=theme['bg'])
        self.left_panel.config(bg=theme['bg'])
        self.right_panel.config(bg=theme['bg'])
        self.button_container.config(bg=theme['bg'])
        self.text_container.config(bg=theme['bg'])
        self.text_frame.config(bg=theme['text_bg'])
        self.text_display.config(
            bg=theme['text_bg'],
            fg=theme['text_fg'],
            insertbackground=theme['text_fg']
        )
        
        # Practice panel colors
        if hasattr(self, 'practice_container'):
            self.practice_container.config(bg=theme['bg'])
            self.practice_instructions.config(bg=theme['bg'], fg=theme['text_fg'])
            self.editor_frame.config(bg=theme['bg'])
            self.practice_editor.config(
                bg=theme['text_bg'],
                fg=theme['text_fg'],
                insertbackground=theme['text_fg']
            )
            self.controls_frame.config(bg=theme['bg'])
            self.practice_status.config(bg=theme['bg'], fg=theme['text_fg'])
        
        # Style all buttons
        for child in self.button_container.winfo_children():
            if isinstance(child, tk.Button):
                is_exit = child['text'].startswith("🚪")
                self.style_button(child, is_exit)
        
        # Style practice buttons if they exist
        if hasattr(self, 'save_button'):
            self.save_button.config(
                bg=theme['button_bg'],
                fg=theme['button_fg'],
                activebackground=theme['button_active']
            )
            self.new_file_button.config(
                bg=theme['button_bg'],
                fg=theme['button_fg'],
                activebackground=theme['button_active']
            )
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def clear_text(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)
    
    def insert_text(self, text, tags=None):
        self.text_display.config(state=tk.NORMAL)
        if tags:
            self.text_display.insert(tk.END, text, tags)
        else:
            self.text_display.insert(tk.END, text)
        self.text_display.config(state=tk.DISABLED)
        self.text_display.see(tk.END)
    
    def start_practice_session(self):
        """Start a new file handling practice session"""
        self.practice_active = True
        self.current_practice_step = 1
        self.practice_completed_steps = set()
        self.practice_file_path = ""
        
        # Hide regular text display and show practice panel
        self.text_container.pack_forget()
        self.practice_container.pack(fill=tk.BOTH, expand=True, padx=(0, 5), pady=(0, 5))
        
        # Clear the editor
        self.practice_editor.delete(1.0, tk.END)
        
        # Set up practice session
        self.update_practice_instructions()
        self.update_practice_progress()
        self.practice_status.config(text="Practice session started!")
        
        # Focus the editor
        self.practice_editor.focus_set()
    
    def update_practice_instructions(self):
        """Update the instructions based on current step"""
        steps = [
            "1. Type some text in the editor above",
            "2. Use Ctrl+C to copy some text",
            "3. Use Ctrl+V to paste the copied text",
            "4. Use Ctrl+Z to undo your last change",
            "5. Save your file using Ctrl+S or the Save button"
        ]
        
        instructions = "💻 PRACTICE SESSION: File Handling\n\n"
        instructions += "Complete these steps to practice file handling:\n\n"
        
        for i, step in enumerate(steps, 1):
            if i in self.practice_completed_steps:
                instructions += f"✓ {step}\n"
            elif i == self.current_practice_step:
                instructions += f"→ {step} (Current step)\n"
            else:
                instructions += f"○ {step}\n"
        
        self.practice_instructions.config(text=instructions)
    
    def update_practice_progress(self):
        """Update the progress bar"""
        total_steps = 5
        completed = len(self.practice_completed_steps)
        progress = (completed / total_steps) * 100
        self.practice_progress['value'] = progress
    
    def check_practice_step(self, action):
        """Check if user performed the correct practice step"""
        if not self.practice_active:
            return
        
        theme = self.themes['dark'] if self.dark_mode else self.themes['light']
        
        if action == 'save' and self.current_practice_step == 5:
            # Save file step
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w') as f:
                        f.write(self.practice_editor.get(1.0, tk.END))
                    self.practice_file_path = file_path
                    self.complete_practice_step()
                    self.practice_status.config(
                        text=f"File saved successfully: {os.path.basename(file_path)}",
                        fg=theme['success']
                    )
                except Exception as e:
                    self.practice_status.config(
                        text=f"Error saving file: {str(e)}",
                        fg=theme['warning']
                    )
            else:
                self.practice_status.config(
                    text="Please select a location to save your file",
                    fg=theme['warning']
                )
        elif action == 'copy' and self.current_practice_step == 2:
            if self.practice_editor.tag_ranges(tk.SEL):
                self.complete_practice_step()
                self.practice_status.config(
                    text="Text copied! Now try pasting it with Ctrl+V",
                    fg=theme['success']
                )
            else:
                self.practice_status.config(
                    text="First select some text to copy",
                    fg=theme['warning']
                )
        elif action == 'paste' and self.current_practice_step == 3:
            try:
                self.practice_editor.update()
                self.complete_practice_step()
                self.practice_status.config(
                    text="Text pasted! Now try undoing with Ctrl+Z",
                    fg=theme['success']
                )
            except:
                self.practice_status.config(
                    text="First copy some text to paste",
                    fg=theme['warning']
                )
        elif action == 'undo' and self.current_practice_step == 4:
            try:
                self.practice_editor.edit_undo()
                self.complete_practice_step()
                self.practice_status.config(
                    text="Change undone! Now save your file with Ctrl+S",
                    fg=theme['success']
                )
            except:
                self.practice_status.config(
                    text="Nothing to undo yet",
                    fg=theme['warning']
                )
        elif self.current_practice_step == 1 and self.practice_editor.get(1.0, "end-1c"):
            # First step - just typing something
            self.complete_practice_step()
            self.practice_status.config(
                text="Great! Now try copying some text with Ctrl+C",
                fg=theme['success']
            )
    
    def complete_practice_step(self):
        """Mark the current step as completed and move to next"""
        self.practice_completed_steps.add(self.current_practice_step)
        self.current_practice_step += 1
        
        if self.current_practice_step > 5:
            self.practice_completed()
        else:
            self.update_practice_instructions()
            self.update_practice_progress()
    
    def practice_completed(self):
        """Called when all practice steps are completed"""
        theme = self.themes['dark'] if self.dark_mode else self.themes['light']
        
        self.practice_status.config(
            text="🎉 Congratulations! You completed all practice steps!",
            fg=theme['success']
        )
        self.update_practice_progress()
        
        # Show completion message
        messagebox.showinfo(
            "Practice Completed",
            "Great job! You've practiced:\n"
            "- Creating and editing a text file\n"
            "- Using keyboard shortcuts (Ctrl+C, Ctrl+V, Ctrl+Z, Ctrl+S)\n"
            "- Saving a file to your computer\n\n"
            "You can start a new practice session anytime."
        )
        
        self.practice_active = False
    
    def show_welcome_message(self):
        self.clear_text()
        welcome_text = """🌟 Welcome to Computer Basics Tutorial! 🌟

This modern application will guide you through the fundamental skills needed to use a computer effectively.

🔹 What you'll learn:
  - How to use the mouse and keyboard efficiently
  - Organizing your files with folders
  - Creating and editing text documents
  - Time-saving keyboard shortcuts
  - Important computer terminology
  - Where to find help when you need it

💡 New Feature: Interactive Practice Session!
  - Try the "Practice Session" to get hands-on experience
  - Create, edit and save files right in the app
  - Practice using keyboard shortcuts with guidance

Click on any lesson button to begin your learning journey!
"""
        self.insert_text(welcome_text)
    
    def show_mouse_keyboard(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """🖱️ ⌨️ Using Mouse and Keyboard - Lesson 1

The mouse and keyboard are your primary tools for interacting with the computer.

=== MOUSE BASICS ===

• Moving: Slide the mouse to move the pointer on screen
• Left Click: Press once to select items
• Double Click: Press quickly twice to open items
• Right Click: Press to see context menus
• Scrolling: Use the wheel to navigate pages

=== KEYBOARD BASICS ===

• Typing: Letters and numbers for text input
• Enter: Confirm actions or create new lines
• Spacebar: Add spaces between words
• Backspace/Delete: Remove text
• Arrow Keys: Navigate without mouse
• Function Keys: Special actions (F1-F12)

🔹 Practice Exercises:
1. Open Notepad and type a short sentence
2. Use the mouse to select part of your text
3. Try copying (Ctrl+C) and pasting (Ctrl+V) the text
4. Save your file (Ctrl+S) to your desktop

💡 Try these in the Practice Session!
"""
        self.insert_text(lesson_text)
    
    def show_create_folder(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """📁 Creating Folders - Lesson 2

Folders help you organize files logically on your computer.

=== METHOD 1: DESKTOP ===
1. Right-click on an empty desktop area
2. Hover over "New" in the menu
3. Click "Folder"
4. Type a descriptive name
5. Press Enter to confirm

=== METHOD 2: FILE EXPLORER ===
1. Open File Explorer (Win+E)
2. Navigate to the desired location
3. Click "New Folder" in the toolbar
4. Name your folder and press Enter

💡 Pro Tips:
• Use clear, specific names (e.g., "Tax Documents 2023")
• Create subfolders for better organization
• Color-code folders for visual sorting (right-click > Properties)

🔹 Practice Exercise:
1. Create a folder called "Learning" on your desktop
2. Inside it, create subfolders: "Documents", "Images", "Projects"
3. Try renaming a folder (right-click > Rename)
"""
        self.insert_text(lesson_text)
    
    def show_create_text_file(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """📝 Creating Text Files - Lesson 3

Text files are simple documents for notes, lists, and information.

=== METHOD 1: NOTEPAD ===
1. Press Win key and type "Notepad"
2. Open the Notepad application
3. Type your content
4. Click File > Save (or Ctrl+S)
5. Choose location and filename
6. Click Save

=== METHOD 2: RIGHT-CLICK ===
1. Right-click in a folder or desktop
2. Select New > Text Document
3. Name the file (e.g., "Shopping List.txt")
4. Double-click to open and edit

🛠️ Advanced Tips:
• Change file extension if needed (.txt, .csv, etc.)
• Use WordPad for formatted text
• Try Markdown for structured notes

🔹 Practice Exercise:
1. Try creating a text file in the Practice Session
2. List 3 computer skills you want to learn
3. Save it in your "Learning" folder
4. Try opening it again to edit
"""
        self.insert_text(lesson_text)
    
    def show_shortcut_keys(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """⌨️ Essential Shortcut Keys - Lesson 4

Keyboard shortcuts save time and make you more efficient.

=== UNIVERSAL SHORTCUTS ===
• Ctrl+C: Copy
• Ctrl+X: Cut
• Ctrl+V: Paste
• Ctrl+Z: Undo
• Ctrl+Y: Redo
• Ctrl+A: Select all
• Ctrl+S: Save
• Ctrl+P: Print

=== WINDOWS SPECIFIC ===
• Win+E: Open File Explorer
• Win+D: Show desktop
• Alt+Tab: Switch apps
• Win+L: Lock computer
• Win+V: Clipboard history

=== TEXT EDITING ===
• Ctrl+B: Bold
• Ctrl+I: Italic
• Ctrl+U: Underline
• Ctrl+F: Find
• Ctrl+H: Replace

📊 Productivity Boost:
Practice these shortcuts in the Practice Session:
1. Ctrl+C to copy text
2. Ctrl+V to paste text
3. Ctrl+Z to undo changes
4. Ctrl+S to save your work
"""
        self.insert_text(lesson_text)
    
    def show_terminology(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """📖 Computer Terminology - Lesson 5

Understanding these terms will help you learn faster.

=== HARDWARE ===
• CPU: The "brain" of your computer
• RAM: Temporary memory for running programs
• SSD/HDD: Permanent storage devices
• GPU: Handles graphics processing

=== SOFTWARE ===
• OS: Operating System (Windows, macOS)
• App/Program: Software tools
• Browser: For accessing the internet
• Driver: Lets hardware and software communicate

=== INTERFACE ===
• Desktop: Main workspace
• Taskbar: Bottom app launcher
• Window: App container
• Icon: Visual representation

🌐 Internet Terms:
• URL: Website address
• Browser: Chrome, Edge, Firefox
• Download/Upload: Transferring files
• Cloud: Online storage

🔹 Knowledge Check:
1. What do you call the bar at the bottom of the screen?
2. What's the difference between RAM and storage?
3. Name three web browsers
"""
        self.insert_text(lesson_text)
    
    def show_getting_help(self):
        self.hide_practice_panel()
        self.clear_text()
        lesson_text = """❓ Getting Help - Lesson 6

Never feel stuck - help is always available!

=== BUILT-IN HELP ===
1. F1 key in most applications
2. Windows: Start > "Get Help"
3. App-specific help menus

=== ONLINE RESOURCES ===
• Microsoft Support: support.microsoft.com
• YouTube tutorials (search specific tasks)
• Reddit communities (r/techsupport)
• Stack Overflow for technical questions

🆘 Asking Effective Questions:
1. Describe what you're trying to do
2. Include exact error messages
3. Note what you've already tried
4. Provide system details if relevant

🔹 Practice Exercise:
1. Press F1 in File Explorer
2. Search online for "how to change desktop background"
3. Bookmark helpful tech support sites
"""
        self.insert_text(lesson_text)
    
    def hide_practice_panel(self):
        """Hide the practice panel and show normal content"""
        if self.practice_container.winfo_ismapped():
            self.practice_container.pack_forget()
            self.text_container.pack(fill=tk.BOTH, expand=True, padx=(0, 5), pady=(0, 5))
            self.practice_active = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ComputerBasicsApp(root)
    root.mainloop()