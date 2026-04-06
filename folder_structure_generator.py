import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

class FolderStructureGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Structure Generator")
        self.root.geometry("800x600") 
        
        # Variables
        self.folder_path = tk.StringVar()
        self.include_hidden = tk.BooleanVar(value=False)
        self.show_paths = tk.BooleanVar(value=False)
        self.include_files = tk.BooleanVar(value=True)
        
        # Default folders to skip for a cleaner DevOps/Full-Stack output
        self.ignore_list = {
            'venv', '.venv', 'node_modules', '__pycache__', 
            '.git', '.idea', '.vscode', 'dist', 'build'
        }
        
        self.create_widgets()

    def create_widgets(self):
        # Top frame for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill="x")
        
        # Folder selection
        tk.Label(control_frame, text="Folder:").grid(row=0, column=0, sticky="w")
        tk.Entry(control_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        # Options frame
        options_frame = tk.LabelFrame(self.root, text="Options & Filters", padx=10, pady=10)
        options_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Checkbutton(options_frame, text="Include hidden (.*)", 
                      variable=self.include_hidden).grid(row=0, column=0, sticky="w", padx=5)
        tk.Checkbutton(options_frame, text="Show full paths", 
                      variable=self.show_paths).grid(row=0, column=1, sticky="w", padx=5)
        tk.Checkbutton(options_frame, text="Include files", 
                      variable=self.include_files).grid(row=0, column=2, sticky="w", padx=5)
        
        tk.Label(options_frame, text=f"Auto-ignoring: {', '.join(list(self.ignore_list)[:5])}...", 
                 fg="gray").grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Generate Structure", 
                 command=self.generate_structure, bg="lightblue", width=20).pack(side="left", padx=5)
        tk.Button(button_frame, text="Save as Text", 
                 command=self.save_as_text, width=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", 
                 command=self.clear_output, bg="lightcoral", width=10).pack(side="left", padx=5)
        
        # Output area
        output_frame = tk.LabelFrame(self.root, text="Generated Tree", padx=10, pady=10)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap="none", font=("Consolas", 10))
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            
    def generate_structure(self):
        folder = self.folder_path.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return
            
        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Generating structure (filtering system folders)...")
        self.root.update()
        
        structure_text = self.get_folder_structure(folder, 0)
        self.output_text.insert(1.0, structure_text)
        self.status_bar.config(text=f"Done. Root: {os.path.basename(folder)}")
        
    def get_folder_structure(self, path, depth):
        indent = "    " * depth
        base_name = os.path.basename(path)
        
        # Initial check: if the root folder itself is in ignore list
        if depth > 0 and base_name in self.ignore_list:
            return ""

        result = f"{indent}{base_name}/\n"
        
        try:
            items = os.listdir(path)
            # Sort: Folders first, then files alphabetically
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            for item in items:
                item_path = os.path.join(path, item)
                
                # 1. Skip hidden files/folders if toggled off
                if not self.include_hidden.get() and item.startswith('.'):
                    continue
                
                # 2. Check if it's a directory
                if os.path.isdir(item_path):
                    # Skip heavy modules/system folders
                    if item in self.ignore_list:
                        result += f"{indent}    ├── {item}/ []\n"
                        continue
                    result += self.get_folder_structure(item_path, depth + 1)
                
                # 3. Handle files
                elif self.include_files.get():
                    display_name = item
                    if self.show_paths.get():
                        display_name = f"{item} ({item_path})"
                    result += f"{indent}    ├── {display_name}\n"
                    
        except PermissionError:
            result += f"{indent}    └── [Permission Denied]\n"
        except Exception as e:
            result += f"{indent}    └── [Error: {str(e)}]\n"
            
        return result
        
    def save_as_text(self):
        content = self.output_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "Nothing to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_bar.config(text=f"File saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")
                
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderStructureGUI(root)
    root.mainloop()
