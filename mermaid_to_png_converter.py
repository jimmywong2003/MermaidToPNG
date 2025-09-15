#!/usr/bin/env python3
"""
Mermaid to PNG Converter
This script extracts mermaid diagrams from markdown files and converts them to PNG images.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

def extract_mermaid_code(markdown_file):
    """Extract mermaid code blocks from markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match mermaid code blocks
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches

def save_mermaid_to_file(mermaid_code, output_file):
    """Save mermaid code to a .mmd file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    return output_file

def convert_mermaid_to_png(mmd_file, output_png):
    """Convert mermaid file to PNG using mermaid-cli."""
    try:
        # Use npx to run mermaid-cli - different approach for Windows
        if os.name == 'nt':  # Windows
            result = subprocess.run([
                'npx.cmd', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
                '-i', mmd_file,
                '-o', output_png,
                '-t', 'default',
                '-b', 'transparent'
            ], capture_output=True, text=True, timeout=120)
        else:  # Unix/Linux/Mac
            result = subprocess.run([
                'npx', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
                '-i', mmd_file,
                '-o', output_png,
                '-t', 'default',
                '-b', 'transparent'
            ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print(f"✓ Successfully converted {mmd_file} to {output_png}")
            return True
        else:
            print(f"✗ Error converting {mmd_file}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout converting {mmd_file}")
        return False
    except Exception as e:
        print(f"✗ Error running mermaid-cli: {e}")
        print("Please ensure Node.js and npm are installed, then run: npm install -g @mermaid-js/mermaid-cli")
        return False

def process_markdown_file(markdown_file):
    """Process a markdown file and convert all mermaid diagrams to PNG."""
    print(f"Processing: {markdown_file}")
    
    # Extract mermaid code blocks
    mermaid_blocks = extract_mermaid_code(markdown_file)
    
    if not mermaid_blocks:
        print("No mermaid diagrams found in the file.")
        return
    
    print(f"Found {len(mermaid_blocks)} mermaid diagram(s)")
    
    # Create output directory for diagrams
    base_name = Path(markdown_file).stem
    output_dir = f"{base_name}_diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    success_count = 0
    for i, mermaid_code in enumerate(mermaid_blocks, 1):
        # Create filenames
        mmd_file = os.path.join(output_dir, f"diagram_{i}.mmd")
        png_file = os.path.join(output_dir, f"diagram_{i}.png")
        
        # Save mermaid code to file
        save_mermaid_to_file(mermaid_code, mmd_file)
        
        # Convert to PNG
        if convert_mermaid_to_png(mmd_file, png_file):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{len(mermaid_blocks)} diagrams converted successfully")
    print(f"Diagrams saved in: {output_dir}/")

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python mermaid_to_png_converter.py <markdown_file.md>")
        print("Example: python mermaid_to_png_converter.py example_document.md")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    
    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' not found.")
        sys.exit(1)
    
    if not markdown_file.endswith('.md'):
        print("Error: Please provide a markdown file (.md extension).")
        sys.exit(1)
    
    process_markdown_file(markdown_file)

if __name__ == "__main__":
    main()
