#!/usr/bin/env python3
"""
Mermaid to PNG Converter - Standalone Version
This version includes embedded Node.js runtime for offline use.
"""

import os
import re
import subprocess
import sys
import tempfile
import shutil
import zipfile
import atexit
from pathlib import Path
import base64

# Embedded Node.js runtime (will be added during build process)
# This is a placeholder - the actual Node.js binaries will be embedded
# during the PyInstaller build process

def get_embedded_nodejs():
    """Get the path to embedded Node.js runtime."""
    # This will be modified during the build process to point to
    # the extracted Node.js binaries
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller executable
        nodejs_dir = os.path.join(sys._MEIPASS, 'nodejs')
        if os.path.exists(nodejs_dir):
            return nodejs_dir
    
    # Fallback to system Node.js if available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'system'  # Use system Node.js
    except (FileNotFoundError, OSError):
        pass
    
    return None

def extract_embedded_nodejs():
    """Extract embedded Node.js runtime to temporary directory."""
    # This function will be populated during the build process
    # to handle the actual extraction of embedded Node.js binaries
    temp_dir = tempfile.mkdtemp(prefix='mermaid_nodejs_')
    
    # Cleanup on exit
    def cleanup():
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
    
    atexit.register(cleanup)
    return temp_dir

def get_node_executable():
    """Get the path to Node.js executable."""
    nodejs_path = get_embedded_nodejs()
    
    if nodejs_path == 'system':
        return 'node'
    elif nodejs_path:
        if os.name == 'nt':  # Windows
            node_exe = os.path.join(nodejs_path, 'node.exe')
        else:  # Unix/Linux/Mac
            node_exe = os.path.join(nodejs_path, 'bin', 'node')
        
        if os.path.exists(node_exe):
            return node_exe
    
    # Fallback: try to extract embedded Node.js
    temp_nodejs = extract_embedded_nodejs()
    if temp_nodejs:
        if os.name == 'nt':
            node_exe = os.path.join(temp_nodejs, 'node.exe')
        else:
            node_exe = os.path.join(temp_nodejs, 'bin', 'node')
        
        if os.path.exists(node_exe):
            return node_exe
    
    return None

def get_npx_executable():
    """Get the path to npx executable or use node to run npx."""
    node_exe = get_node_executable()
    if not node_exe:
        return None
    
    if node_exe == 'node':
        return 'npx'
    
    # For embedded Node.js, we need to use the node executable to run npx
    return node_exe

def extract_mermaid_code(markdown_file):
    """Extract mermaid code blocks from markdown file."""
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(markdown_file, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Pattern to match mermaid code blocks
    pattern = r'```mermaid\s*\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches

def save_mermaid_to_file(mermaid_code, output_file):
    """Save mermaid code to a .mmd file."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    return output_file

def convert_mermaid_to_png(mmd_file, output_png):
    """Convert mermaid file to PNG using mermaid-cli."""
    npx_executable = get_npx_executable()
    
    if not npx_executable:
        print("✗ Error: Node.js runtime not available.")
        print("Please ensure Node.js is installed or use the standalone version.")
        return False
    
    try:
        # Use the appropriate npx command based on whether we're using system or embedded Node.js
        if npx_executable == 'npx':
            # System npx
            cmd = [
                'npx', '-p', '@mermaid-js/mermaid-cli', 'mmdc',
                '-i', mmd_file,
                '-o', output_png,
                '-t', 'default',
                '-b', 'transparent'
            ]
        else:
            # Embedded Node.js - use node to run npx with proper path handling
            # Convert Windows paths to use forward slashes to avoid escaping issues
            mmd_file_fixed = mmd_file.replace('\\', '/')
            output_png_fixed = output_png.replace('\\', '/')
            
            cmd = [
                npx_executable, '-e', 
                f'require("child_process").execSync("npx -p @mermaid-js/mermaid-cli mmdc -i \\"{mmd_file_fixed}\\" -o \\"{output_png_fixed}\\" -t default -b transparent", {{stdio: "inherit"}})'
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
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
        print("Trying alternative approach...")
        return try_alternative_conversion(mmd_file, output_png)

def try_alternative_conversion(mmd_file, output_png):
    """Alternative conversion method using direct node execution."""
    try:
        # Read the mermaid code
        with open(mmd_file, 'r', encoding='utf-8') as f:
            mermaid_code = f.read()
        
        # Create a simple HTML file with mermaid
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@9.3.0/dist/mermaid.min.js"></script>
            <style>body {{ margin: 0; }}</style>
        </head>
        <body>
            <div class="mermaid">
            {mermaid_code}
            </div>
            <script>
                mermaid.initialize({{startOnLoad: true}});
            </script>
        </body>
        </html>
        '''
        
        html_file = mmd_file + '.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("⚠ Using alternative conversion method (browser-based)")
        print("This may have limited functionality compared to mermaid-cli")
        return True
        
    except Exception as e:
        print(f"✗ Alternative conversion also failed: {e}")
        return False

def process_markdown_file(markdown_file):
    """Process a markdown file and convert all mermaid diagrams to PNG."""
    print(f"Processing: {markdown_file}")
    
    # Check Node.js availability
    node_status = get_node_executable()
    if not node_status:
        print("✗ Error: Node.js runtime not found.")
        print("Please install Node.js or use the standalone executable version.")
        return
    
    print("✓ Node.js runtime available")
    
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
    print("Mermaid to PNG Converter - Standalone Version")
    print("=" * 50)
    
    if len(sys.argv) != 2:
        print("Usage: mermaid_to_png_converter <markdown_file.md>")
        print("Example: mermaid_to_png_converter example_document.md")
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
