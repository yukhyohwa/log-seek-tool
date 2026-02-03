import os
import csv
import sys
import time

# --- Configuration ---
# List of IDs to search for (can be modified here or passed via command line)
DEFAULT_SEARCH_IDS = [
    '78128243', 
    '90000730', 
    '90000729', 
    '90000733'
]

# Base directory for searching (current script directory)
SEARCH_BASE = os.path.dirname(os.path.abspath(__file__))

def find_target_csv():
    """ Automatically finds the newest or largest CSV file in the directory tree. """
    csv_files = []
    # Recursively search the current directory and its subdirectories
    for root, dirs, files in os.walk(SEARCH_BASE):
        for f in files:
            if f.lower().endswith('.csv'):
                full_path = os.path.join(root, f)
                # Store (path, modification_time, size)
                csv_files.append((full_path, os.path.getmtime(full_path), os.path.getsize(full_path)))
    
    if not csv_files:
        return None
    
    # Sort by modification time, newest first
    csv_files.sort(key=lambda x: x[1], reverse=True)
    return csv_files[0][0]

def analyze_log(csv_path, target_ids):
    print(f"[*] Analyzing file: {os.path.basename(csv_path)}")
    print(f"[*] Target IDs: {', '.join(target_ids)}")
    print("-" * 50)
    
    start_time = time.time()
    results = {tid: {} for tid in target_ids}
    
    try:
        # Use utf-8-sig to handle potential BOM
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            row_count = 0
            for row in reader:
                row_count += 1
                if row_count % 200000 == 0:
                    print(f"[#] Processed {row_count} rows...")
                
                # Iterate through each column to support substring matching (e.g., searching within JSON like 'a_rst')
                for col_idx, cell_value in enumerate(row):
                    if not cell_value:
                        continue
                        
                    for tid in target_ids:
                        if tid in cell_value:
                            # Record event name (assumed to be index 1) and column name
                            event_name = row[1] if len(row) > 1 else "Unknown"
                            col_name = header[col_idx] if col_idx < len(header) else f"Column_{col_idx}"
                            
                            key = (event_name, col_name)
                            results[tid][key] = results[tid].get(key, 0) + 1
                        
    except Exception as e:
        print(f"[!] Error during reading: {e}")
        return

    end_time = time.time()
    
    # Output report
    print("\n" + "="*20 + " Analysis Report " + "="*20)
    for tid, found_locations in results.items():
        print(f"\n> ID: {tid}")
        if not found_locations:
            print("  [!] ID not found in the file.")
        else:
            for (event, col), count in found_locations.items():
                print(f"  - Event: {event:20} | Column: {col:20} | Occurrences: {count}")
    
    print("\n" + "="*50)
    print(f"[*] Completed in {end_time - start_time:.2f} seconds. Total rows: {row_count}")

if __name__ == "__main__":
    # Support command line arguments for IDs
    search_ids = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_SEARCH_IDS
    
    target_csv = find_target_csv()
    
    if not target_csv:
        print("[!] Error: No CSV files found in the project or subdirectories (e.g., raw_data/).")
    else:
        analyze_log(target_csv, search_ids)
