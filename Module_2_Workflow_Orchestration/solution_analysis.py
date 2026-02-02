
"""
Module 2 Homework Solution Script
Calculates row counts and file sizes for NYC Taxi data (Yellow and Green) used in the quiz.
"""
import subprocess
import concurrent.futures

def get_row_count(service, year, month):
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{service}_tripdata_{year}-{month:02d}.csv.gz"
    cmd = f"curl -sL {url} | zcat | wc -l"
    print(f"Fetching {service} {year}-{month}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        # wc -l counts newlines. The file has a header.
        # So number of data rows = output - 1.
        # However, sometimes there might be an empty line at the end?
        # Usually standard CSVs: header + data rows.
        count = int(result.stdout.strip().split()[0])
        data_rows = count - 1
        print(f"Done {service} {year}-{month}: {data_rows}")
        return data_rows
    except Exception as e:
        print(f"Failed {service} {year}-{month}: {e}")
        return 0

def main():
    # Known values from previous run
    known_yellow_2020 = {
        4: 237993, 5: 348371, 6: 549760, 7: 800412,
        8: 1007284, 9: 1341012, 10: 1681131
    }
    
    known_green_2020 = {
        3: 223406, 4: 35612, 5: 57360, 6: 63109,
        7: 72257, 8: 81063, 9: 87987
    }
    
    tasks = []
    
    # Yellow 2020 missing
    yellow_missing = [1, 2, 3, 11, 12]
    for m in yellow_missing:
        tasks.append(('yellow', 2020, m))
        
    # Green 2020 missing
    green_missing = [1, 2, 10, 11, 12]
    for m in green_missing:
        tasks.append(('green', 2020, m))
        
    # Yellow 2021-03
    tasks.append(('yellow', 2021, 3))
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_args = {executor.submit(get_row_count, *args): args for args in tasks}
        for future in concurrent.futures.as_completed(future_to_args):
            args = future_to_args[future]
            try:
                count = future.result()
                results[args] = count
            except Exception as e:
                print(f"Exception for {args}: {e}")
                
    # Calculate Totals
    total_yellow_2020 = sum(known_yellow_2020.values())
    for m in yellow_missing:
        total_yellow_2020 += results.get(('yellow', 2020, m), 0)
        
    total_green_2020 = sum(known_green_2020.values())
    for m in green_missing:
        total_green_2020 += results.get(('green', 2020, m), 0)
        
    yellow_2021_03 = results.get(('yellow', 2021, 3), 0)
    
    print("\n--- Final Results ---")
    print(f"Q3: Total Yellow 2020 Rows: {total_yellow_2020:,}")
    print(f"Q4: Total Green 2020 Rows: {total_green_2020:,}")
    print(f"Q5: Yellow 2021-03 Rows: {yellow_2021_03:,}")

if __name__ == "__main__":
    main()
