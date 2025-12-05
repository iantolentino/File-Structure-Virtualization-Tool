import os
import argparse
from pathlib import Path
import json
import sys

class FolderStructureGenerator:
    def __init__(self, exclude_hidden=True, max_depth=None, include_files=True):
        """
        Initialize the folder structure generator
        
        Args:
            exclude_hidden (bool): Whether to exclude hidden files/folders
            max_depth (int): Maximum depth to traverse (None for unlimited)
            include_files (bool): Whether to include files in the output
        """
        self.exclude_hidden = exclude_hidden
        self.max_depth = max_depth
        self.include_files = include_files
        
    def is_hidden(self, path):
        """Check if a file/folder is hidden (starts with .)"""
        return os.path.basename(path).startswith('.')
    
    def get_structure(self, root_path, current_depth=0):
        """
        Recursively get the folder structure
        
        Args:
            root_path (str): Root directory path
            current_depth (int): Current recursion depth
            
        Returns:
            dict: Folder structure as a dictionary
        """
        if self.max_depth is not None and current_depth >= self.max_depth:
            return {}
        
        structure = {
            "name": os.path.basename(root_path),
            "type": "directory",
            "path": root_path,
            "children": []
        }
        
        try:
            items = os.listdir(root_path)
            
            # Sort items: directories first, then files
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(root_path, x)), x.lower()))
            
            for item in items:
                item_path = os.path.join(root_path, item)
                
                # Skip hidden items if configured
                if self.exclude_hidden and self.is_hidden(item_path):
                    continue
                
                if os.path.isdir(item_path):
                    # Recursively process directory
                    child_structure = self.get_structure(item_path, current_depth + 1)
                    if child_structure:  # Only add if not empty
                        structure["children"].append(child_structure)
                elif self.include_files:
                    # Add file
                    structure["children"].append({
                        "name": item,
                        "type": "file",
                        "path": item_path,
                        "size": os.path.getsize(item_path) if os.path.exists(item_path) else 0
                    })
        except PermissionError:
            structure["children"].append({
                "name": "[Permission Denied]",
                "type": "error",
                "path": ""
            })
        except Exception as e:
            structure["children"].append({
                "name": f"[Error: {str(e)}]",
                "type": "error",
                "path": ""
            })
        
        return structure
    
    def print_structure(self, structure, prefix="", is_last=True, show_path=False):
        """
        Print folder structure in a tree format
        
        Args:
            structure (dict): Folder structure dictionary
            prefix (str): Prefix for current line
            is_last (bool): Whether this is the last item in its parent
            show_path (bool): Whether to show full paths
        """
        if structure["type"] == "error":
            print(f"{prefix}└── {structure['name']}")
            return
        
        # Determine the connector symbol
        connector = "└── " if is_last else "├── "
        
        # Display item
        display_name = structure["name"]
        if show_path and structure["type"] == "directory":
            display_name = f"{structure['name']} ({structure['path']})"
        
        print(f"{prefix}{connector}{display_name}")
        
        # Calculate new prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Process children
        if structure["type"] == "directory" and "children" in structure:
            for i, child in enumerate(structure["children"]):
                is_child_last = (i == len(structure["children"]) - 1)
                self.print_structure(child, new_prefix, is_child_last, show_path)
    
    def export_json(self, structure, output_file):
        """Export structure to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        print(f"\nStructure exported to: {output_file}")
    
    def export_txt(self, structure, output_file, show_path=False):
        """Export structure to text file"""
        original_stdout = sys.stdout
        with open(output_file, 'w', encoding='utf-8') as f:
            sys.stdout = f
            self.print_structure(structure, show_path=show_path)
            sys.stdout = original_stdout
        print(f"\nStructure exported to: {output_file}")
    
    def get_summary(self, structure):
        """Get summary statistics about the folder structure"""
        stats = {"directories": 0, "files": 0, "errors": 0}
        
        def count_items(node):
            if node["type"] == "directory":
                stats["directories"] += 1
                for child in node.get("children", []):
                    count_items(child)
            elif node["type"] == "file":
                stats["files"] += 1
            elif node["type"] == "error":
                stats["errors"] += 1
        
        count_items(structure)
        return stats

def main():
    parser = argparse.ArgumentParser(description="Generate folder structure visualization")
    parser.add_argument("folder", help="Path to the folder to analyze")
    parser.add_argument("-o", "--output", help="Output file (supports .txt, .json)")
    parser.add_argument("-p", "--show-path", action="store_true", 
                       help="Show full paths in output")
    parser.add_argument("-a", "--all", action="store_true", 
                       help="Include hidden files and folders")
    parser.add_argument("-d", "--depth", type=int, 
                       help="Maximum depth to traverse")
    parser.add_argument("-n", "--no-files", action="store_true",
                       help="Exclude files from output")
    parser.add_argument("-s", "--summary", action="store_true",
                       help="Show summary statistics")
    
    args = parser.parse_args()
    
    # Check if folder exists
    if not os.path.exists(args.folder):
        print(f"Error: Folder '{args.folder}' does not exist!")
        return
    
    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a folder!")
        return
    
    # Create generator
    generator = FolderStructureGenerator(
        exclude_hidden=not args.all,
        max_depth=args.depth,
        include_files=not args.no_files
    )
    
    # Get structure
    print(f"\nAnalyzing folder: {args.folder}")
    structure = generator.get_structure(args.folder)
    
    # Display structure
    print(f"\nFolder Structure:\n")
    generator.print_structure(structure, show_path=args.show_path)
    
    # Show summary if requested
    if args.summary:
        stats = generator.get_summary(structure)
        print(f"\nSummary:")
        print(f"  Directories: {stats['directories']}")
        print(f"  Files: {stats['files']}")
        if stats['errors'] > 0:
            print(f"  Errors: {stats['errors']}")
    
    # Export if output file specified
    if args.output:
        output_path = Path(args.output)
        if output_path.suffix.lower() == '.json':
            generator.export_json(structure, args.output)
        else:
            # Default to txt format
            if output_path.suffix.lower() != '.txt':
                args.output = f"{args.output}.txt"
            generator.export_txt(structure, args.output, args.show_path)

def interactive_mode():
    """Run in interactive mode if no command line arguments provided"""
    print("=== Folder Structure Generator ===\n")
    
    # Get folder path
    folder_path = input("Enter folder path (or drag and drop folder here): ").strip()
    
    if not folder_path:
        print("No folder provided. Exiting.")
        return
    
    # Remove quotes if path was drag-and-dropped
    folder_path = folder_path.strip('"\'')
    
    # Validate folder
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a folder!")
        return
    
    # Get options
    print("\nOptions:")
    print("1. Show hidden files/folders? (y/n): ", end="")
    show_hidden = input().strip().lower() == 'y'
    
    print("2. Maximum depth (press Enter for unlimited): ", end="")
    depth_input = input().strip()
    max_depth = int(depth_input) if depth_input else None
    
    print("3. Include files? (y/n): ", end="")
    include_files = input().strip().lower() != 'n'
    
    print("4. Show full paths? (y/n): ", end="")
    show_path = input().strip().lower() == 'y'
    
    print("5. Export to file? (y/n): ", end="")
    export = input().strip().lower() == 'y'
    
    output_file = None
    if export:
        print("   Enter output file name (with .txt or .json extension): ", end="")
        output_file = input().strip()
    
    # Create generator
    generator = FolderStructureGenerator(
        exclude_hidden=not show_hidden,
        max_depth=max_depth,
        include_files=include_files
    )
    
    # Get structure
    print(f"\n{'='*50}")
    print(f"Analyzing folder: {folder_path}")
    structure = generator.get_structure(folder_path)
    
    # Display structure
    print(f"\nFolder Structure:\n")
    generator.print_structure(structure, show_path=show_path)
    
    # Show summary
    stats = generator.get_summary(structure)
    print(f"\nSummary:")
    print(f"  Directories: {stats['directories']}")
    print(f"  Files: {stats['files']}")
    if stats['errors'] > 0:
        print(f"  Errors: {stats['errors']}")
    
    # Export if requested
    if export and output_file:
        output_path = Path(output_file)
        if output_path.suffix.lower() == '.json':
            generator.export_json(structure, output_file)
        else:
            generator.export_txt(structure, output_file, show_path)

if __name__ == "__main__":
    # Check if command line arguments were provided
    if len(sys.argv) > 1:
        main()
    else:
        interactive_mode()