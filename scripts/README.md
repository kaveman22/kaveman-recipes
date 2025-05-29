# Recipe Scripts

This directory contains utility scripts for managing the recipe collection.

## Available Scripts

### `convert_to_csv.py`

Converts a text file with recipe names and YouTube URLs into a CSV file.

Usage:
```
./convert_to_csv.py input_file.txt output_file.csv
```

### `convert_kaynspice_to_md.py`

Converts KaynSpice recipes from the CSV file to individual markdown files.

Usage:
```
./convert_kaynspice_to_md.py
```

This script reads from `_data/kaynspice_recipes.csv` and creates markdown files in the `_recipes/jamaican/` directory.

## Adding New Scripts

When adding new scripts:

1. Place the script in this directory
2. Make it executable with `chmod +x script_name.py`
3. Add documentation to this README file
4. Follow the existing patterns for input/output handling
