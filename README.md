# Folder Structure Generator

## Overview

The Folder Structure Generator is a desktop application that visualizes directory hierarchies in a clear, tree-like format. Built with Python's Tkinter library, this tool provides an intuitive interface for exploring and documenting folder structures with configurable display options.

## Features

### Core Functionality
- **Directory Visualization**: Generate hierarchical views of folder structures
- **Recursive Scanning**: Automatically scans subdirectories to any depth
- **Multiple Display Formats**: Toggle between simple and detailed views 

### Customization Options
- **Hidden Files/Folders**: Option to include or exclude hidden items 
- **File Inclusion**: Toggle between folder-only or folder-and-file views
- **Path Display**: Show full file paths alongside names
- **Sorting**: Automatic alphabetical sorting with folders prioritized

### Export Capabilities
- **Text Export**: Save generated structures as plain text files
- **Clipboard Ready**: Copy formatted output directly from the interface
- **UTF-8 Encoding**: Proper handling of special characters in filenames

## Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python installations)

### Setup
1. Ensure Python is installed on your system
2. Save the Python script to a local directory
3. Run the application using:
   ```bash
   python folder_structure_generator.py
   ```

## Usage Guide

### Launching the Application
Execute the script to open the main interface. The window contains four main sections:

1. **Folder Selection**: Input field with browse button
2. **Options Panel**: Configuration checkboxes
3. **Control Buttons**: Generate, Save, and Clear functions
4. **Output Display**: Scrollable text area showing results

### Generating Structures
1. Click "Browse" to select a target directory
2. Configure display options as needed:
   - Include/exclude hidden items
   - Show/hide full paths
   - Include/exclude files
3. Click "Generate Structure" to create the visualization

### Exporting Results
1. Generate a folder structure
2. Click "Save as Text" to export
3. Choose filename and location
4. The structure saves as a UTF-8 encoded text file

## Technical Details

### Architecture
- **GUI Framework**: Tkinter for cross-platform compatibility
- **File Operations**: Python's os module for system interactions
- **Recursive Algorithm**: Depth-first traversal for structure generation

### Error Handling
- **Permission Errors**: Graceful handling of restricted directories
- **Invalid Paths**: User feedback for non-existent folders
- **Save Failures**: Detailed error messages for write operations

### Performance Considerations
- **Non-blocking UI**: Status updates during processing
- **Memory Efficient**: Stream-based file writing for exports
- **Progressive Display**: Real-time output during generation

## Application Interface

### Main Window Components
- **Title Bar**: "Folder Structure Generator"
- **Dimensions**: 800x600 pixels (resizable)
- **Layout**: Organized frames with logical grouping

### Control Elements
- **Folder Selection**: Text entry with browse dialog
- **Options Checkboxes**: Independent configuration toggles
- **Action Buttons**: Color-coded for function grouping
- **Status Bar**: Real-time operation feedback

### Output Area
- **Scrolled Text Widget**: Handles large directory structures
- **Monospaced Font**: Preserves alignment in tree views
- **Read-Only Display**: Prevents accidental modification

## Use Cases

### Development Projects
- Document repository structures
- Share project layouts with teams
- Verify file organization

### System Administration
- Audit directory permissions
- Map network drives
- Inventory file systems

### Documentation
- Create README file listings
- Generate attachment manifests
- Produce audit trail reports

## Limitations and Considerations

### Platform Compatibility
- Tested on Windows, macOS, and Linux
- Path separator differences handled automatically
- Permission models vary by operating system

### Performance
- Large directories may take time to process
- Very deep nesting could affect recursion limits
- Memory usage scales with directory size

### Security
- No network operations implemented
- Local file access only
- User must have appropriate permissions

## Troubleshooting

### Common Issues
- **Empty Output**: Verify folder path exists and is accessible
- **Missing Files**: Check "Include files" option is selected
- **Permission Errors**: Application runs with user privileges

### Error Messages
- "Please select a valid folder!" - Invalid or empty path specified
- "No content to save!" - Generate structure before exporting
- "Permission Denied" - Insufficient access rights to directory

## Development Information

### Code Structure
- **FolderStructureGUI Class**: Main application controller
- **Modular Methods**: Separate functions for each operation
- **Event-Driven Design**: Tkinter callback architecture

### Extensibility Points
- Additional export formats (JSON, XML)
- Filtering by file extension
- Search functionality within structures
- Custom styling and theming

## Support

For issues or questions:
1. Verify Python and Tkinter are properly installed
2. Check file permissions on target directories
3. Review the configuration options

## License and Attribution

This application uses standard Python libraries and requires no external dependencies. The code is provided for educational and practical use.

---

*Note: This application operates on local file systems only and does not transmit data over networks. Always ensure you have appropriate permissions before scanning directories.*
