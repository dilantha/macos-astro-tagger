import os
import json
import subprocess
from pathlib import Path
import sys

def get_file_tags(path):
    """Get current tags of a file using mdls"""
    try:
        result = subprocess.run(
            ['mdls', '-raw', '-name', 'kMDItemUserTags', path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip() != '(null)':
            # Parse the output, removing parentheses and splitting
            tags = result.stdout.strip('()\n').split(',')
            return [tag.strip(' "') for tag in tags]
        return []
    except subprocess.SubprocessError:
        return []

def create_tag_if_not_exists(tag_name="Astro", tag_color="Purple"):
    """Create a tag in Finder if it doesn't exist."""
    apple_script = f'''
    tell application "Finder"
        try
            set tag_names to paragraphs of (do shell script "tag -l")
            if tag_names does not contain "{tag_name}" then
                make new tag at tag browser with properties {{name:"{tag_name}", color:"{tag_color}"}}
            end if
        end try
    end tell
    '''
    try:
        subprocess.run(['osascript', '-e', apple_script], check=True, capture_output=True, text=True)
        return True
    except subprocess.SubprocessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') else str(e)
        print(f"Error creating tag: {error_msg}", file=sys.stderr)
        return False

def add_macos_tag(path, tag_name="Astro"):
    """Add a tag to a file or directory using mdls and xattr."""
    absolute_path = os.path.abspath(path)
    
    # Check if tag already exists
    current_tags = get_file_tags(absolute_path)
    if tag_name in current_tags:
        print(f"Tag '{tag_name}' already exists on {path}")
        return True
    
    try:
        # Add the tag using the tag command
        subprocess.run(
            ['tag', '-a', tag_name, absolute_path],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.SubprocessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') else str(e)
        print(f"Error applying tag to {path}: {error_msg}", file=sys.stderr)
        return False

def is_astro_project(directory):
    """Check if a directory contains an Astro project."""
    # Check for astro.config.mjs/ts
    config_files = ['astro.config.mjs', 'astro.config.ts']
    has_config = any(Path(directory, config_file).exists() for config_file in config_files)
    
    # Check package.json for Astro dependencies
    package_json = Path(directory, 'package.json')
    if package_json.exists():
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                deps = package_data.get('dependencies', {})
                dev_deps = package_data.get('devDependencies', {})
                has_astro_dep = 'astro' in deps or 'astro' in dev_deps
                return has_astro_dep or has_config
        except json.JSONDecodeError:
            return has_config
    
    return has_config

def tag_first_level_astro_projects(web_root, tag_name="Astro", tag_color="Purple"):
    """
    Check immediate subdirectories of web_root for Astro projects and tag them.
    """
    tagged_count = 0
    web_root = os.path.abspath(web_root)
    
    # Create the tag first if it doesn't exist
    if not create_tag_if_not_exists(tag_name, tag_color):
        print("Warning: Failed to create tag, but will try to continue...")
    
    # Get immediate subdirectories
    try:
        subdirs = [d for d in os.listdir(web_root) 
                  if os.path.isdir(os.path.join(web_root, d))
                  and not d.startswith('.')]  # Skip hidden directories
    except OSError as e:
        print(f"Error accessing directory {web_root}: {e}", file=sys.stderr)
        return 0
    
    for subdir in subdirs:
        full_path = os.path.join(web_root, subdir)
        if is_astro_project(full_path):
            print(f"Found Astro project: {full_path}")
            if add_macos_tag(full_path, tag_name):
                tagged_count += 1
    
    return tagged_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python macos_astro_tagger.py <web_root> [tag_name] [tag_color]")
        print("\nAvailable colors: Red, Orange, Yellow, Green, Blue, Purple, Gray")
        sys.exit(1)
    
    web_root = sys.argv[1]
    tag_name = sys.argv[2] if len(sys.argv) > 2 else "Astro"
    tag_color = sys.argv[3] if len(sys.argv) > 3 else "Purple"
    
    if not Path(web_root).exists():
        print(f"Directory not found: {web_root}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Checking immediate subdirectories in: {web_root}")
    print(f"Will tag with: {tag_name} ({tag_color})")
    
    tagged = tag_first_level_astro_projects(web_root, tag_name, tag_color)
    print(f"\nCompleted! Tagged {tagged} project(s)")

if __name__ == "__main__":
    main()
