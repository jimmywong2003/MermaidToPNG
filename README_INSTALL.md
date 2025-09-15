# MermaidToPNG - Installation Package

This package contains the standalone Mermaid to PNG Converter executable that works without requiring Node.js or Python installation.

## Package Contents

- `mermaid_to_png_converter.exe` - Main executable (38.5MB)
- `example_document.md` - Sample file with various Mermaid diagrams
- `quick_start.bat` - Windows helper script
- This README file

## System Requirements

- **Windows 10** or later (64-bit)
- **No Node.js required** - Embedded in executable
- **No Python required** - Standalone application
- **Disk Space**: ~200MB recommended

## Quick Installation

### Option 1: Simple Extraction
1. Extract the ZIP file to your desired location
2. Double-click `quick_start.bat` to get started
3. Or run manually: `mermaid_to_png_converter.exe example_document.md`

### Option 2: Manual Setup
1. Extract the files to a folder of your choice
2. Add the folder to your system PATH (optional)
3. Use from command line or file explorer

## Usage

### Basic Command
```cmd
mermaid_to_png_converter.exe <markdown_file.md>
```

### Examples
```cmd
# Convert example file
mermaid_to_png_converter.exe example_document.md

# Convert your own file
mermaid_to_png_converter.exe your_document.md

# Convert all markdown files in current directory
for %f in (*.md) do mermaid_to_png_converter.exe "%f"
```

### Expected Output
```
Mermaid to PNG Converter - Standalone Version
==================================================
Processing: example_document.md
✓ Node.js runtime available
Found 7 mermaid diagram(s)
✓ Successfully converted example_document_diagrams/diagram_1.mmd to example_document_diagrams/diagram_1.png
...
Conversion complete: 7/7 diagrams converted successfully
Diagrams saved in: example_document_diagrams/
```

## File Structure After Conversion

```
your_document.md
your_document_diagrams/
├── diagram_1.mmd      # Extracted Mermaid code
├── diagram_1.png      # Generated PNG image
├── diagram_2.mmd
├── diagram_2.png
└── ... (more diagrams)
```

## Supported Diagram Types

- ✅ Flowcharts (`graph TD`, `graph LR`)
- ✅ Sequence diagrams (`sequenceDiagram`)
- ✅ Class diagrams (`classDiagram`)
- ✅ State diagrams (`stateDiagram`)
- ✅ Gantt charts (`gantt`)
- ✅ Pie charts (`pie`)
- ✅ Requirement diagrams (`requirementDiagram`)

## Performance

- **Execution Time**: 2-10 seconds per diagram
- **Memory Usage**: ~100-200MB
- **Offline Operation**: Works completely offline

## Troubleshooting

### Common Issues

1. **"Access Denied" errors**
   - Run Command Prompt as Administrator
   - Or move the executable to a folder with write permissions

2. **Timeout errors**
   - Complex diagrams may take longer (2-minute timeout per diagram)

3. **Blank PNG files**
   - Check your Mermaid syntax using online editors

4. **Antivirus warnings**
   - Some antivirus software may flag the embedded Node.js
   - Add exception for this executable if needed

### Debug Mode

For advanced troubleshooting, you can:
- Check the generated `.mmd` files to verify Mermaid code extraction
- Run with system Node.js if available for comparison

## Uninstallation

Simply delete the folder containing the executable and related files. No registry changes or system modifications are made.

## Technical Details

- **Embedded Node.js**: v18.17.1
- **mermaid-cli**: Latest version
- **Python**: Not required (standalone build)
- **Architecture**: Windows x64

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure you have the latest version
3. Verify your Mermaid syntax is valid

## License

This software is provided under the MIT License. The embedded Node.js runtime is subject to Node.js licensing terms.

---

**Note**: This is a standalone executable that includes an embedded Node.js runtime, making it larger than typical applications but completely self-contained and portable.
