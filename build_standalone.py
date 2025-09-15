#!/usr/bin/env python3
"""
Build script for creating standalone Mermaid to PNG Converter executable.
This script handles downloading Node.js, installing dependencies, and packaging with PyInstaller.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import zipfile
import urllib.request
import platform
from pathlib import Path

def download_file(url, destination):
    """Download a file from URL to destination."""
    print(f"Downloading {url}...")
    try:
        with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract zip file to directory."""
    print(f"Extracting {zip_path} to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
        return False

def install_dependencies():
    """Install required Python dependencies."""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing PyInstaller: {e}")
        return False

def download_nodejs():
    """Download and extract Node.js for the current platform."""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Map architecture names
    if arch in ['x86_64', 'amd64']:
        arch = 'x64'
    elif arch in ['i386', 'i686', 'x86']:
        arch = 'x86'
    elif arch.startswith('arm'):
        arch = 'arm64' if '64' in arch else 'armv7l'
    
    node_versions = {
        'windows': {
            'x64': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-win-x64.zip',
            'x86': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-win-x86.zip'
        },
        'linux': {
            'x64': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-linux-x64.tar.xz',
            'arm64': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-linux-arm64.tar.xz'
        },
        'darwin': {
            'x64': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-darwin-x64.tar.gz',
            'arm64': 'https://nodejs.org/dist/v18.17.1/node-v18.17.1-darwin-arm64.tar.gz'
        }
    }
    
    if system not in node_versions:
        print(f"Unsupported system: {system}")
        return None
    
    if arch not in node_versions[system]:
        print(f"Unsupported architecture for {system}: {arch}")
        return None
    
    node_url = node_versions[system][arch]
    temp_dir = tempfile.mkdtemp(prefix='nodejs_build_')
    download_path = os.path.join(temp_dir, 'nodejs.zip')
    
    if not download_file(node_url, download_path):
        return None
    
    extract_dir = os.path.join(temp_dir, 'extracted')
    os.makedirs(extract_dir, exist_ok=True)
    
    if not extract_zip(download_path, extract_dir):
        return None
    
    # Find the extracted Node.js directory
    extracted_items = os.listdir(extract_dir)
    if len(extracted_items) == 1:
        nodejs_dir = os.path.join(extract_dir, extracted_items[0])
        return nodejs_dir
    else:
        print("Unexpected extraction structure")
        return None

def create_build_directory():
    """Create build directory structure."""
    build_dir = "build_standalone"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    os.makedirs(build_dir, exist_ok=True)
    
    # Copy main script
    shutil.copy2("mermaid_to_png_converter_standalone.py", os.path.join(build_dir, "mermaid_to_png_converter.py"))
    
    return build_dir

def build_with_pyinstaller(build_dir, nodejs_dir=None):
    """Build the executable using PyInstaller."""
    print("Building executable with PyInstaller...")
    
    # Create spec file or use command line
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "mermaid_to_png_converter",
        "--onefile",
        "--console",
        "--add-data", f"{build_dir}/mermaid_to_png_converter.py;.",
        os.path.join(build_dir, "mermaid_to_png_converter.py")
    ]
    
    if nodejs_dir:
        pyinstaller_cmd.extend([
            "--add-data", f"{nodejs_dir};nodejs"
        ])
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("✓ PyInstaller build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ PyInstaller build failed: {e}")
        return False

def create_install_script():
    """Create installation script for mermaid-cli."""
    install_script = """#!/bin/bash
# Installation script for mermaid-cli
echo "Installing mermaid-cli..."
npm install -g @mermaid-js/mermaid-cli
echo "Installation complete!"
"""
    
    with open("install_mermaid_cli.sh", "w") as f:
        f.write(install_script)
    
    # For Windows
    win_script = """@echo off
echo Installing mermaid-cli...
npm install -g @mermaid-js/mermaid-cli
echo Installation complete!
pause
"""
    
    with open("install_mermaid_cli.bat", "w") as f:
        f.write(win_script)

def main():
    """Main build function."""
    print("Mermaid to PNG Converter - Standalone Build Script")
    print("=" * 60)
    
    # Check if we're on a supported platform
    system = platform.system().lower()
    if system not in ['windows', 'linux', 'darwin']:
        print(f"Unsupported platform: {system}")
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Download Node.js
    print("\n1. Downloading Node.js...")
    nodejs_dir = download_nodejs()
    if not nodejs_dir:
        print("⚠ Could not download Node.js. Building without embedded Node.js.")
        print("The executable will require system Node.js to be installed.")
        nodejs_dir = None
    
    # Create build directory
    print("\n2. Preparing build files...")
    build_dir = create_build_directory()
    
    # Create installation script
    create_install_script()
    
    # Build with PyInstaller
    print("\n3. Building executable...")
    if not build_with_pyinstaller(build_dir, nodejs_dir):
        return False
    
    print("\n4. Finalizing...")
    # Move the executable to the root directory
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        executables = [f for f in os.listdir(dist_dir) if f.startswith("mermaid_to_png_converter")]
        if executables:
            exe_name = executables[0]
            src_path = os.path.join(dist_dir, exe_name)
            dest_path = exe_name
            shutil.move(src_path, dest_path)
            print(f"✓ Executable created: {dest_path}")
    
    print("\nBuild completed successfully!")
    print("\nNext steps:")
    print("1. Run the executable: ./mermaid_to_png_converter <markdown_file.md>")
    print("2. Or install mermaid-cli globally: npm install -g @mermaid-js/mermaid-cli")
    print("3. Test with: mermaid_to_png_converter example_document.md")
    
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
