#!/usr/bin/env python3
"""
Version management script for Lacework Compliance Reporter
Usage: python bump_version.py [major|minor|patch]
"""

import re
import sys
import subprocess
from pathlib import Path

def update_package_json(version):
    """Update version in electron/package.json"""
    package_file = Path("electron/package.json")
    if package_file.exists():
        content = package_file.read_text()
        content = re.sub(r'"version":\s*"[^"]*"', f'"version": "{version}"', content)
        package_file.write_text(content)
        print(f"✅ Updated electron/package.json to version {version}")

def update_readme(version):
    """Update version in README.md"""
    readme_file = Path("README.md")
    if readme_file.exists():
        content = readme_file.read_text()
        # Update version in title
        content = re.sub(r'v\d+\.\d+\.\d+', f'v{version}', content)
        # Update version at bottom
        content = re.sub(r'\*\*Version\*\*:\s*\d+\.\d+\.\d+', f'**Version**: {version}', content)
        readme_file.write_text(content)
        print(f"✅ Updated README.md to version {version}")

def update_streamlit_app(version):
    """Update version in streamlit_app.py if it exists"""
    app_file = Path("streamlit_app.py")
    if app_file.exists():
        content = app_file.read_text()
        # Update any version references in the app
        content = re.sub(r'v\d+\.\d+\.\d+', f'v{version}', content)
        # Update hardcoded version in the Information section
        content = re.sub(r'\*\*Version:\*\* \d+\.\d+\.\d+', f'**Version:** {version}', content)
        app_file.write_text(content)
        print(f"✅ Updated streamlit_app.py to version {version}")

def update_electron_html(version):
    """Update version in electron/index.html loading screen"""
    html_file = Path("electron/index.html")
    if html_file.exists():
        content = html_file.read_text()
        # Update version in the loading screen
        content = re.sub(r'v\d+\.\d+\.\d+', f'v{version}', content)
        html_file.write_text(content)
        print(f"✅ Updated electron/index.html to version {version}")

def update_last_updated_date():
    """Update last updated date in README.md and streamlit_app.py"""
    from datetime import datetime
    
    # Get current date in DD/MM/YYYY format
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Update README.md
    readme_file = Path("README.md")
    if readme_file.exists():
        content = readme_file.read_text()
        # Update last updated date
        content = re.sub(r'\*\*Last Updated\*\*: \d{2}/\d{2}/\d{4}', f'**Last Updated**: {current_date}', content)
        readme_file.write_text(content)
        print(f"✅ Updated README.md last updated date to {current_date}")
    
    # Update streamlit_app.py
    app_file = Path("streamlit_app.py")
    if app_file.exists():
        content = app_file.read_text()
        # Update last updated date
        content = re.sub(r'\*\*Last Updated:\*\* \d{2}/\d{2}/\d{4}', f'**Last Updated:** {current_date}', content)
        app_file.write_text(content)
        print(f"✅ Updated streamlit_app.py last updated date to {current_date}")

def create_git_tag(version):
    """Create and push Git tag for the new version"""
    try:
        tag_name = f"v{version}"
        
        # Check if tag already exists
        result = subprocess.run(['git', 'tag', '-l', tag_name], capture_output=True, text=True)
        if tag_name in result.stdout:
            print(f"⚠️  Tag {tag_name} already exists. Skipping tag creation.")
            return False
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        print(f"✅ Added all changes to Git")
        
        # Commit changes
        commit_message = f"Bump version to {version}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"✅ Committed version bump to {version}")
        
        # Create tag
        subprocess.run(['git', 'tag', tag_name], check=True)
        print(f"✅ Created Git tag {tag_name}")
        
        # Push changes and tag
        subprocess.run(['git', 'push'], check=True)
        subprocess.run(['git', 'push', 'origin', tag_name], check=True)
        print(f"✅ Pushed changes and tag {tag_name} to GitHub")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        print("💡 Make sure you have Git configured and have push access to the repository")
        return False
    except FileNotFoundError:
        print("❌ Git not found. Make sure Git is installed and in your PATH")
        return False

def parse_version(version_string):
    """Parse version string into components"""
    parts = version_string.split('.')
    if len(parts) != 3:
        raise ValueError("Version must be in format X.Y.Z")
    return [int(x) for x in parts]

def bump_version(current_version, bump_type):
    """Bump version based on type"""
    major, minor, patch = parse_version(current_version)
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError("Bump type must be major, minor, or patch")
    
    return f"{major}.{minor}.{patch}"

def get_current_version():
    """Get current version from package.json"""
    package_file = Path("electron/package.json")
    if package_file.exists():
        content = package_file.read_text()
        match = re.search(r'"version":\s*"([^"]*)"', content)
        if match:
            return match.group(1)
    return "2.0.6"  # Default fallback

def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py [major|minor|patch]")
        print("Examples:")
        print("  python bump_version.py patch  # 2.0.6 -> 2.0.7")
        print("  python bump_version.py minor  # 2.0.6 -> 2.1.0")
        print("  python bump_version.py major  # 2.0.6 -> 3.0.0")
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    if bump_type not in ['major', 'minor', 'patch']:
        print("Error: Bump type must be major, minor, or patch")
        sys.exit(1)
    
    current_version = get_current_version()
    new_version = bump_version(current_version, bump_type)
    
    print(f"🔄 Bumping version from {current_version} to {new_version}")
    
    # Update all files
    update_package_json(new_version)
    update_readme(new_version)
    update_streamlit_app(new_version)
    update_electron_html(new_version)
    update_last_updated_date()
    
    print(f"\n✅ Version bumped to {new_version}")
    
    # Create Git tag and trigger release
    print("\n🚀 Creating Git tag and triggering GitHub Actions release...")
    if create_git_tag(new_version):
        print(f"\n🎉 Success! Release {new_version} has been triggered.")
        print("📋 Check GitHub Actions to monitor the build and release process.")
        print("🔗 The release will appear in the Releases section once complete.")
    else:
        print(f"\n⚠️  Version bumped to {new_version} but Git tag creation failed.")
        print("💡 You can manually create the tag with:")
        print(f"   git tag v{new_version}")
        print(f"   git push origin v{new_version}")

if __name__ == "__main__":
    main() 