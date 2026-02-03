# Log ID Finder Tool

A utility for quickly locating specific IDs within massive log files (CSV format) to identify their corresponding Event and Column.

## Directory Structure
- `id_finder.py`: Core analysis script (Logic).
- `run_finder.bat`: Windows shortcut script for one-click execution.
- `raw_data/`: Directory to store source CSV log files (Data).
- `sql_templates/`: SQL templates for extracting logs from the data warehouse (Tools).
- `README.md`: Documentation.

## Usage
1. Place your exported CSV log files into the **`raw_data/`** directory.
2. **Method A**: Double-click **`run_finder.bat`** to execute with default IDs.
3. **Method B**: Use CLI to specify custom IDs:
   ```bash
   python id_finder.py [ID1] [ID2] ...
   ```

## Key Features
- **Auto-Discovery**: Automatically scans for the newest and largest CSV file in the directory and subdirectories.
- **Smart Mapping**: Automatically parses headers to map IDs to their Event Name and Column Name.
- **High Performance**: Optimized for multi-GB log files using row-by-row streaming.
- **Project Structure**: Clean separation between code, data, and SQL templates.
- **Safe Versioning**: `.gitignore` is pre-configured to exclude large data files.
