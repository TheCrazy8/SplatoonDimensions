"""
BrightOS Launcher
This launcher will:  
1. Check for and install/update BrightOS to the latest version from GitHub
2. Install any missing dependencies
3. Create all necessary directories for BrightOS
4. Run BrightOS. py
"""
import os
import sys
import subprocess
import json
import urllib.request
import urllib.error
import zipfile
import shutil
from pathlib import Path
import tempfile

# GitHub repository configuration
GITHUB_REPO_OWNER = "TheCrazy8"
GITHUB_REPO_NAME = "Blaze-Official"
GITHUB_REPO = f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"


def get_user_dir():
    """Get the user's home directory"""
    return os.path.expanduser("~")


def get_brightos_dir():
    """Get the BrightOS installation directory"""
    userdir = get_user_dir()
    if sys.platform == "win32":  
        return os.path.join(userdir, "AppData", "Local", "BrightOS")
    else:
        # For other platforms, use a hidden directory in home
        return os.path.join(userdir, ".brightos")


def get_github_token():
    """Get GitHub token from environment variable or config file"""
    # Try environment variable first
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('VITE_GITHUB_TOKEN')
    if token:
        return token
    
    # Try reading from config file
    try:
        token_file = os.path.join(get_brightos_dir(), '.github_token')
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                token = f.read().strip()
                if token:
                    return token
    except Exception:
        pass
    
    return None

def create_authenticated_request(url):
    """Create a URL request with GitHub authentication if available"""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'BrightOS-Launcher')
    
    # Add authentication if token is available
    token = get_github_token()
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    
    return req


def create_directories():
    """Create all necessary directories for BrightOS"""
    brightos_dir = get_brightos_dir()
    
    directories = [
        brightos_dir,
        os.path.join(brightos_dir, "Plugins"),
        os.path.join(brightos_dir, "Scripts"),
        os.path.join(brightos_dir, "install")
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Directory created/verified: {directory}")
        except Exception as e:
            print(f"✗ Error creating directory {directory}: {e}")
            return False
    
    # Create Importlist.txt if it doesn't exist
    importlist_path = os.path.join(brightos_dir, "Importlist.txt")
    if not os.path.exists(importlist_path):
        try:
            with open(importlist_path, 'w') as f:
                f.write("# BrightOS Import List\n")
            print(f"✓ Created:  {importlist_path}")
        except Exception as e:
            print(f"✗ Error creating Importlist.txt: {e}")
    
    return True


def check_rate_limit():
    """Check GitHub API rate limit status"""
    try:
        req = create_authenticated_request('https://api.github.com/rate_limit')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            core = data['resources']['core']
            
            remaining = core['remaining']
            limit = core['limit']
            
            if remaining < 10: 
                from datetime import datetime
                reset_time = datetime.fromtimestamp(core['reset'])
                print(f"⚠ GitHub API rate limit low: {remaining}/{limit}")
                print(f"  Resets at: {reset_time. strftime('%I:%M %p')}")
                
                if limit == 60:
                    print("\n💡 Tip: Add a GitHub token to increase rate limit from 60 to 5,000/hour")
                    print("   1. Get token:  https://github.com/settings/tokens")
                    print("   2. Save to:  " + os.path.join(get_brightos_dir(), '.github_token'))
            else:
                auth_status = "authenticated" if limit > 60 else "unauthenticated"
                print(f"✓ GitHub API rate limit:  {remaining}/{limit} ({auth_status})")
            
            return remaining > 0
    except Exception: 
        # If we can't check, assume we're okay
        return True


def get_latest_release_from_atom():
    """Get the latest release information from GitHub Atom feed (no rate limit)"""
    import xml.etree.ElementTree as ET
    
    atom_url = f"https://github.com/{GITHUB_REPO}/releases.atom"
    
    try:
        req = urllib.request.Request(atom_url)
        req.add_header('User-Agent', 'BrightOS-Launcher')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            atom_data = response.read().decode('utf-8')
            
        # Parse the Atom feed
        root = ET.fromstring(atom_data)
        
        # Atom namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        # Get the first entry (latest release)
        entries = root.findall('atom:entry', ns)
        if not entries:
            return None
        
        latest_entry = entries[0]
        
        # Extract tag name from the link
        link = latest_entry.find('atom:link', ns)
        if link is not None:
            href = link.get('href', '')
            # Extract tag from URL like https://github.com/{owner}/{repo}/releases/tag/{tag}
            if '/releases/tag/' in href:
                tag_name = href.split('/releases/tag/')[-1]
                # Skip launcher releases (we only want BrightOS releases)
                if not tag_name.startswith('launcher-'):
                    return {'tag_name': tag_name, 'from_atom': True}
        
        # Try next entry if first was a launcher release
        for entry in entries[1:]:
            link = entry.find('atom:link', ns)
            if link is not None:
                href = link.get('href', '')
                if '/releases/tag/' in href:
                    tag_name = href.split('/releases/tag/')[-1]
                    if not tag_name.startswith('launcher-'):
                        return {'tag_name': tag_name, 'from_atom': True}
        
        return None
            
    except Exception as e:
        print(f"⚠ Could not fetch from Atom feed: {e}")
        return None


def get_latest_release_info():
    """Get the latest release information from GitHub with authentication"""
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    
    try:  
        print("Checking for latest BrightOS version...")
        req = create_authenticated_request(api_url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json. loads(response.read().decode())
            return data
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No releases found.  Using repository main branch.")
            return None
        elif e.code == 403:
            print("⚠ GitHub API rate limit exceeded, trying alternative method...")
            
            # Try Atom feed as fallback (doesn't count against rate limit)
            atom_result = get_latest_release_from_atom()
            if atom_result:
                print(f"✓ Found latest release from feed: {atom_result['tag_name']}")
                return atom_result
            
            # If Atom feed also fails, show tips
            print("\n💡 Tip: Add a GitHub Personal Access Token for faster updates")
            print("   1. Go to:  https://github.com/settings/tokens")
            print("   2. Click 'Generate new token (classic)'")
            print("   3. Select only 'public_repo' scope")
            print("   4. Copy the token (starts with ghp_)")
            print("   5. Save it to: " + os.path.join(get_brightos_dir(), '.github_token'))
            print("\n  Falling back to main branch...")
            return None
        else:  
            print(f"⚠ Error checking for updates: HTTP {e.code}")
            return None
            
    except urllib.error.URLError as e:
        print(f"⚠ Network error: {e}")
        return None
        
    except Exception as e: 
        print(f"⚠ Error checking for updates: {e}")
        return None


def download_file(url, dest_path):
    """Download a file from a URL to a destination path"""
    try:
        print(f"Downloading from {url}...")
        req = create_authenticated_request(url)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        print(f"✓ Downloaded to {dest_path}")
        return True
    except Exception as e: 
        print(f"✗ Error downloading:  {e}")
        return False


def download_files_from_release_assets(release_info, install_dir):
    """Download Python files from release assets"""
    FILES_TO_DOWNLOAD = ['BrightOS.py', 'requirements.txt', 'build.py']
    
    # Get assets from release
    assets = release_info.get('assets', [])
    if not assets:
        return False
    
    # Create a mapping of asset names to download URLs
    asset_map = {asset['name']: asset['browser_download_url'] for asset in assets}
    
    # Download each required file
    success_count = 0
    for file_name in FILES_TO_DOWNLOAD:
        if file_name in asset_map:
            dest_path = os.path.join(install_dir, file_name)
            if download_file(asset_map[file_name], dest_path):
                success_count += 1
        else:
            print(f"⚠ Asset not found in release: {file_name}")
    
    # Check if we got the essential files (at least BrightOS.py)
    if success_count > 0 and os.path.exists(os.path.join(install_dir, 'BrightOS.py')):
        # Save version info
        tag_name = release_info.get('tag_name', 'unknown')
        version_file = os.path.join(install_dir, "version.txt")
        with open(version_file, 'w') as f:
            f.write(tag_name)
        print(f"✓ Installed version: {tag_name}")
        return True
    
    return False


def download_and_extract_release(install_dir):
    """Download and extract the latest BrightOS release"""
    # Files to copy from the repository
    FILES_TO_COPY = ['BrightOS.py', 'requirements.txt', 'build.py']
    
    # Try to get the latest release
    release_info = get_latest_release_info()
    
    if release_info:
        # First, try to download files from release assets
        tag_name = release_info.get('tag_name', 'latest')
        print(f"Found version: {tag_name}")
        
        # Only try assets if this is from the API (not Atom feed)
        if not release_info.get('from_atom', False):
            print("Attempting to download from release assets...")
            
            if download_files_from_release_assets(release_info, install_dir):
                print("✓ Successfully downloaded files from release assets")
                return True
            
            print("⚠ Release assets not available, downloading release archive...")
        else:
            print("Downloading release archive...")
        
        # Use public archive URL (doesn't require authentication)
        # Format: https://github.com/owner/repo/archive/refs/tags/{tag}.zip
        zipball_url = f"https://github.com/{GITHUB_REPO}/archive/refs/tags/{tag_name}.zip"
    else:
        # Fallback to main branch
        zipball_url = f"https://github.com/{GITHUB_REPO}/archive/refs/heads/main.zip"
        tag_name = "main"
        print("Using main branch")
    
    # Download the zip file
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "brightos.zip")
        
        if not download_file(zipball_url, zip_path):
            return False
        
        # Extract the zip file
        print("Extracting files...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted directory (GitHub zips have a top-level directory)
            extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
            if not extracted_dirs:
                print("✗ No directory found in zip file")
                return False
            
            source_dir = os.path.join(temp_dir, extracted_dirs[0])
            
            # Copy necessary files to install directory
            for file_name in FILES_TO_COPY:
                source_file = os.path.join(source_dir, file_name)
                if os.path.exists(source_file):
                    dest_file = os.path.join(install_dir, file_name)
                    shutil.copy2(source_file, dest_file)
                    print(f"✓ Copied:  {file_name}")
                else:
                    print(f"⚠ File not found: {file_name}")
            
            # Copy favicon. ico if it exists
            favicon_source = os.path.join(source_dir, 'docs', 'public', 'favicon.ico')
            if os.path.exists(favicon_source):
                favicon_dest = os.path.join(install_dir, 'favicon.ico')
                shutil. copy2(favicon_source, favicon_dest)
                print(f"✓ Copied:  favicon.ico")
            
            # Save version info
            version_file = os.path.join(install_dir, "version.txt")
            with open(version_file, 'w') as f:
                f. write(tag_name)
            print(f"✓ Installed version: {tag_name}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error extracting files: {e}")
            return False


def install_dependencies(install_dir):
    """Install Python dependencies from requirements.txt"""
    requirements_path = os.path.join(install_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("⚠ requirements.txt not found, skipping dependency installation")
        return True
    
    print("\nInstalling dependencies...")
    try:
        # Use pip to install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", requirements_path,
            "--upgrade"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def run_brightos(install_dir):
    """Run BrightOS.py from the install directory (e.g., AppData/Local/BrightOS/install)"""
    brightos_path = os.path.join(install_dir, "BrightOS.py")
    
    if not os.path.exists(brightos_path):
        print(f"✗ BrightOS.py not found at {brightos_path}")
        return False
    
    print("\nStarting BrightOS...")
    try:
        # Run BrightOS.py with Python from the install directory
        subprocess.run([sys.executable, brightos_path], cwd=install_dir)
        return True
    except Exception as e:  
        print(f"✗ Error running BrightOS: {e}")
        return False


def check_for_updates(install_dir):
    """Check if an update is available"""
    version_file = os.path.join(install_dir, "version.txt")
    
    if not os.path.exists(version_file):
        return True  # No version file means we should install
    
    # Read current version
    with open(version_file, 'r') as f:
        current_version = f.read().strip()
    
    # Get latest version
    release_info = get_latest_release_info()
    if release_info:
        latest_version = release_info.get('tag_name', 'unknown')
        if latest_version != current_version:  
            print(f"Update available: {current_version} → {latest_version}")
            return True
        else:
            print(f"Already up to date: {current_version}")
            return False
    
    # If we can't check (rate limited or network error), assume no update needed
    print("✓ Continuing with existing installation")
    return False


def check_directories_exist():
    """Check if all necessary directories exist"""
    brightos_dir = get_brightos_dir()
    
    directories = [
        brightos_dir,
        os.path.join(brightos_dir, "Plugins"),
        os.path.join(brightos_dir, "Scripts"),
        os.path.join(brightos_dir, "install")
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            return False
    
    # Check if Importlist.txt exists
    importlist_path = os.path.join(brightos_dir, "Importlist.txt")
    if not os.path.exists(importlist_path):
        return False
    
    return True


def check_dependencies_installed(install_dir):
    """Check if dependencies are installed by checking pip list"""
    requirements_path = os.path.join(install_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        return True  # No requirements file, assume OK
    
    try:
        # Read requirements
        with open(requirements_path, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not requirements:
            return True
        
        # Get list of installed packages
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return False
        
        installed_packages = result.stdout.lower()
        
        # Packages to skip (build-only dependencies)
        BUILD_ONLY_PACKAGES = {'pyinstaller'}
        
        # Check each requirement
        for req in requirements:
            # Extract package name (before any version specifier)
            package_name = req.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0]. strip().lower()
            
            # Skip build-only dependencies
            if package_name in BUILD_ONLY_PACKAGES: 
                continue
            
            # Normalize package name (pip list may use underscores or dashes)
            package_with_dash = package_name
            package_with_underscore = package_name.replace('-', '_')
            
            # Check if package is in the installed list (either form)
            if package_with_dash not in installed_packages and package_with_underscore not in installed_packages:
                return False
        
        return True
    except Exception as e:
        # If we can't check, assume dependencies need to be installed
        return False


def main():
    """Main launcher function"""
    brightos_dir = get_brightos_dir()
    install_dir = os.path.join(brightos_dir, "install")
    brightos_path = os.path.join(install_dir, "BrightOS.py")
    
    # Check rate limit status
    check_rate_limit()
    print()
    
    # Quick checks to see if we can just launch directly
    directories_ok = check_directories_exist()
    brightos_installed = os.path.exists(brightos_path)
    
    # If everything is in place, check for updates but don't show full setup
    if directories_ok and brightos_installed:
        # Quick mode - just check for updates and dependencies
        needs_update = check_for_updates(install_dir)
        deps_ok = check_dependencies_installed(install_dir)
        
        if not needs_update and deps_ok:
            # Everything is ready, just launch
            print("Starting BrightOS...")
            run_brightos(install_dir)
            return 0
        else:
            # Need to do some updates
            print("=" * 50)
            print("BrightOS Launcher - Update Required")
            print("=" * 50)
            print()
            
            if needs_update:
                print("Updating BrightOS...")
                if not download_and_extract_release(install_dir):
                    print("⚠ Update failed, using existing installation")
                print()
            
            if not deps_ok:
                print("Installing missing dependencies...")
                if not install_dependencies(install_dir):
                    print("⚠ Dependency installation had issues, but continuing...")
                print()
            
            print("Starting BrightOS...")
            print("=" * 50)
            print()
            run_brightos(install_dir)
            return 0
    
    # Full setup mode - first time or missing components
    print("=" * 50)
    print("BrightOS Launcher - First Time Setup")
    print("=" * 50)
    print()
    
    # Step 1: Create directories
    if not directories_ok:
        print("Step 1: Creating directories...")
        if not create_directories():
            print("\n✗ Failed to create directories")
            input("Press Enter to exit...")
            return 1
        print()
    
    # Step 2: Check for updates and install/update BrightOS
    needs_install = not os.path.exists(brightos_path)
    
    if needs_install:
        print("Step 2: Installing BrightOS...")
        if not download_and_extract_release(install_dir):
            print("\n✗ Failed to install BrightOS")
            input("Press Enter to exit...")
            return 1
        print()
    
    # Step 3: Install dependencies
    print("Step 3: Installing dependencies...")
    if not install_dependencies(install_dir):
        print("\n⚠ Dependency installation had issues, but continuing...")
    print()
    
    # Step 4: Run BrightOS
    print("Step 4: Starting BrightOS...")
    print("=" * 50)
    print()
    
    run_brightos(install_dir)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt: 
        print("\n\nLauncher interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
