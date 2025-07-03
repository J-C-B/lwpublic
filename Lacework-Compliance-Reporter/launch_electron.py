#!/usr/bin/env python3
"""
Launcher script for Lacework Compliance Reporter Electron App
This script ensures the Python environment is properly set up before launching Electron.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_environment():
    """Check if Python environment is properly set up."""
    try:
        import streamlit
        print("✅ Streamlit is available")
        return True
    except ImportError:
        print("❌ Streamlit not found. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def check_node_environment():
    """Check if Node.js environment is properly set up."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js from https://nodejs.org/")
        return False

def check_npm_dependencies():
    """Check if npm dependencies are installed."""
    electron_dir = Path("electron")
    node_modules = electron_dir / "node_modules"
    
    if node_modules.exists():
        print("✅ npm dependencies are installed")
        return True
    else:
        print("❌ npm dependencies not found. Installing...")
        try:
            subprocess.run(['npm', 'install'], cwd=electron_dir, check=True)
            print("✅ npm dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install npm dependencies")
            return False

def launch_electron():
    """Launch the Electron app."""
    print("🚀 Launching Lacework Compliance Reporter...")
    
    electron_dir = Path("electron")
    if not electron_dir.exists():
        print("❌ Electron directory not found")
        return False
    
    try:
        # Change to electron directory and start the app
        subprocess.run(['npm', 'start'], cwd=electron_dir, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch Electron app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return True

def main():
    """Main launcher function."""
    print("🔒 Lacework Compliance Reporter - Electron Launcher")
    print("=" * 50)
    
    # Check all prerequisites
    checks = [
        check_python_environment(),
        check_node_environment(),
        check_npm_dependencies()
    ]
    
    if all(checks):
        print("\n✅ All checks passed!")
        return launch_electron()
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 