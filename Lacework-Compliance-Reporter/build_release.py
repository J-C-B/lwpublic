#!/usr/bin/env python3
"""
Build script for Lacework Compliance Reporter
Usage: python build_release.py [patch|minor|major] [--no-bump]
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=False, text=True)
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        return False

def main():
    # Parse arguments
    bump_type = None
    no_bump = False
    
    for arg in sys.argv[1:]:
        if arg == '--no-bump':
            no_bump = True
        elif arg in ['patch', 'minor', 'major']:
            bump_type = arg
        else:
            print("Usage: python build_release.py [patch|minor|major] [--no-bump]")
            print("Examples:")
            print("  python build_release.py patch     # Bump patch version and build")
            print("  python build_release.py minor     # Bump minor version and build")
            print("  python build_release.py --no-bump # Build without version bump")
            sys.exit(1)
    
    print("🔒 Lacework Compliance Reporter - Build Script")
    print("=" * 50)
    
    # Step 1: Bump version (if requested)
    if not no_bump and bump_type:
        print(f"🔄 Bumping version ({bump_type})...")
        if not run_command(f"python bump_version.py {bump_type}"):
            print("❌ Version bump failed")
            sys.exit(1)
    
    # Step 2: Check if we're in the right directory
    if not Path("electron").exists():
        print("❌ electron directory not found. Please run from project root.")
        sys.exit(1)
    
    # Step 3: Build the Electron app
    print("📦 Building Electron app...")
    if not run_command("npm run dist:all", cwd="electron"):
        print("❌ Build failed")
        sys.exit(1)
    
    # Step 4: Show results
    dist_dir = Path("dist")
    if dist_dir.exists():
        print("\n✅ Build completed successfully!")
        print("📁 Generated files:")
        
        # Show macOS builds
        mac_files = list(dist_dir.glob("*.dmg"))
        if mac_files:
            print("   🍎 macOS:")
            for file in mac_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"      📦 {file.name} ({size_mb:.1f} MB)")
        
        # Show Windows builds
        win_files = list(dist_dir.glob("*.exe"))
        if win_files:
            print("   🪟 Windows:")
            for file in win_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"      📦 {file.name} ({size_mb:.1f} MB)")
        
        # Show Linux builds (if any)
        linux_files = list(dist_dir.glob("*.AppImage"))
        if linux_files:
            print("   🐧 Linux:")
            for file in linux_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"      📦 {file.name} ({size_mb:.1f} MB)")
        
        print(f"\n🎉 Ready for distribution!")
        print(f"📂 Build files are in: {dist_dir.absolute()}")
    else:
        print("❌ Build directory not found")
        sys.exit(1)

if __name__ == "__main__":
    main() 