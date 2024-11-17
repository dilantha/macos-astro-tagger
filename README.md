# macOS Astro Project Tagger

A command-line tool that automatically detects and tags Astro.js projects in your development directories using macOS Finder tags. This makes it easy to visually identify and filter your Astro projects in Finder.

## Features

- Automatically detects Astro projects by checking:
  - presence of `astro.config.mjs` or `astro.config.ts`
  - Astro dependencies in `package.json`
- Creates and applies macOS Finder tags
- Scans immediate subdirectories only (no deep recursion)
- Skips hidden directories
- Prevents duplicate tags
- Customizable tag name and color

## Requirements

- macOS (tested on Monterey and newer)
- Python 3.6+
- [tag](https://github.com/jdberry/tag) command line tool

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/macos-astro-tagger.git
cd macos-astro-tagger
```

2. Install the required `tag` command line tool:
```bash
brew install tag
```

3. Make the script executable (optional):
```bash
chmod +x astro_tagger.py
```

## Usage

Basic usage to tag all Astro projects in a directory:
```bash
python astro_tagger.py /path/to/your/projects
```

By default, this will:
- Create a purple "Astro" tag if it doesn't exist
- Scan all immediate subdirectories in the specified path
- Tag any Astro projects found with the "Astro" tag

### Custom Tag Name and Color

You can specify a custom tag name and color:
```bash
python astro_tagger.py /path/to/projects "My Astro" Blue
```

Available colors:
- Red
- Orange
- Yellow
- Green
- Blue
- Purple
- Gray

### Examples

Tag all projects in your web development directory:
```bash
python astro_tagger.py ~/www
```

Use a custom tag for client projects:
```bash
python astro_tagger.py ~/clients "Client Astro" Orange
```

## How It Works

The script:
1. Creates the specified tag in Finder if it doesn't exist
2. Scans the immediate subdirectories of the specified path
3. Identifies Astro projects by checking for:
   - `astro.config.mjs` or `astro.config.ts`
   - Astro dependencies in `package.json`
4. Checks for existing tags to prevent duplicates
5. Applies the tag to detected Astro projects

## Known Limitations

- Only works on macOS due to reliance on Finder tags
- Requires the `tag` command line tool
- Only scans immediate subdirectories (not recursive)
- May require Finder permissions to manage tags

## Troubleshooting

### Tag Creation Failed

If you see "Warning: Failed to create tag", try:
1. Open Finder
2. Create the tag manually (Finder > Settings > Tags)
3. Run the script again

### Permission Issues

If you encounter permission errors:
1. Make sure the script has access to the directories you're scanning
2. Check System Settings > Privacy & Security > Files and Folders
3. Ensure Terminal/your IDE has proper permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by [Dilantha Nanayakkara](https://github.com/dilantha)
