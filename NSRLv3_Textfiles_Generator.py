# Script Name: NSRLv3_Textfiles_Generator.py
# Script Version: 1.0
# Script Author: iSmellPowder
# Script last modification on: 20 September 2023

import sqlite3
import csv
import os
import time

def print_splash_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console screen

    splash = """
    ==========================================================================================================================
    |                        .__  _________              .__  .__ __________                .___                             |
    |                        |__|/   _____/ _____   ____ |  | |  |\______   \______  _  ____| _/___________                  |
    |                        |  |\_____  \ /     \_/ __ \|  | |  | |     ___/  _ \ \/ \/ / __ |/ __ \_  __ \                 |
    |                        |  |/        \  Y Y  \  ___/|  |_|  |_|    |  (  <_> )     / /_/ \  ___/|  | \/                 |
    |                        |__/_______  /__|_|  /\___  >____/____/____|   \____/ \/\_/\____ |\___  >__|                    |
    |                                   \/      \/     \/                                    \/    \/                        |
    |                                                                                                                        |
    |                                                NSRL RDS Text Files Generator                                           |
    |                                                       using RDS 3 dataset                                              |
    | https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl/nsrl-download/current-rds |
    |                                                                                                                        |
    ==========================================================================================================================

                                NOTE: Make a duplicate copy of the downloaded db before continuing
    """

    print(splash)

def generate_NSRLFile(rds_file):
    print("##### Generating NSRLFile.txt #####")
    start_time = time.time()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Generating NSRLFile.txt started on: {current_time}")

    try:
        print("Connecting to the SQLite database...")
        # Connect to the SQLite database
        conn = sqlite3.connect(rds_file)
        cursor = conn.cursor()

        # Increase cache size to 16GB in KB units
        print("Setting cache size...")
        cursor.execute("PRAGMA cache_size = 16000000")

        # DROP TABLE IF EXISTS EXPORT;
        print("Dropping table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS EXPORT")

        # CREATE TABLE EXPORT AS SELECT ...
        print("Creating EXPORT table...")
        cursor.execute("""
            CREATE TABLE EXPORT AS 
            SELECT sha1, md5, crc32, file_name, file_size, package_id
            FROM FILE
        """)

        # Update file_name column in EXPORT table
        print("Updating file_name column...")
        cursor.execute("""
            UPDATE EXPORT SET file_name = REPLACE(file_name, '"', '')
        """)

        # Export data to a CSV file
        print("Exporting data to output.txt...")
        with open('output.txt', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Set headers to off manually
            cursor.execute("SELECT sha1, md5, crc32, file_name, file_size, package_id, 0, '' FROM EXPORT ORDER BY sha1")
            
            rows = cursor.fetchall()
            total_rows = len(rows)
            for i, row in enumerate(rows):
                # Ensure that each element in the row is encoded properly
                row = [elem.encode('utf-8').decode('unicode_escape') if isinstance(elem, str) else elem for elem in row]
                csv_writer.writerow(row)
                # Print progress
                print(f"Exporting row {i+1}/{total_rows}...", end='\r')

        print("\nCleaning up output.txt...")
        with open('output.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            data = data.replace('""', '"')
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(data)

        # Create NSRLFile-header.txt
        print("Creating NSRLFile-header.txt...")
        with open('NSRLFile-header.txt', 'w') as header_file:
            header_file.write('"SHA-1","MD5","CRC32","FileName","FileSize","ProductCode","OpSystemCode","SpecialCode"\n')

        # Concatenate output.txt and NSRLFile-header.txt into NSRLFile.txt
        print("Concatenating files...")
        with open('NSRLFile-header.txt', 'r', encoding='utf-8') as header_file, \
            open('output.txt', 'r', encoding='utf-8') as output_file, \
            open('NSRLFile.txt', 'w', encoding='utf-8') as final_file:
            final_file.write(header_file.read())
            final_file.write(output_file.read())

        print("Files concatenated successfully.")

        # Remove temporary files
        print("Cleaning up temporary files...")
        os.remove('output.txt')
        os.remove('NSRLFile-header.txt')
    
        print("##### NSRLFile.txt created successfully #####")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            end_time = time.time()
            duration = end_time - start_time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nGenerating NSRLFile.txt ended on: {current_time}. Duration: {duration}")
            print("Connection to the SQLite database closed.")

def generate_NSRLMfg(rds_file):
    print("##### Generating NSRLMfg.txt #####")
    start_time = time.time()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Generating NSRLMfg.txt started on: {current_time}")

    try:
        print("Connecting to the SQLite database...")
        # Connect to the SQLite database
        conn = sqlite3.connect(rds_file)
        cursor = conn.cursor()

        # Increase cache size to 100MB
        print("Setting cache size...")
        cursor.execute("PRAGMA cache_size = 100000")

        # DROP TABLE IF EXISTS EXPORT;
        print("Dropping table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS EXPORT")

        # CREATE TABLE EXPORT AS SELECT ...
        print("Creating EXPORT table...")
        cursor.execute("""
            CREATE TABLE EXPORT AS 
            SELECT manufacturer_id, name FROM MFG
        """)

        # Update name column in EXPORT table
        print("Updating name column...")
        cursor.execute("""
            UPDATE EXPORT SET name = REPLACE(name, '"', '')
        """)

        # Export data to a CSV file
        print("Exporting data to output.txt...")
        with open('output.txt', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Set headers to off manually
            cursor.execute("SELECT manufacturer_id, '\"' || name || '\"' FROM EXPORT ORDER BY manufacturer_id")
            
            rows = cursor.fetchall()
            total_rows = len(rows)
            for i, row in enumerate(rows):
                csv_writer.writerow(row)
                # Print progress
                print(f"Exporting row {i+1}/{total_rows}...", end='\r')

        print("\nCleaning up output.txt...")
        with open('output.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            data = data.replace('""', '"')
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(data)

        # Create NSRLMfg-header.txt
        print("Creating NSRLMfg-header.txt...")
        with open('NSRLMfg-header.txt', 'w') as header_file:
            header_file.write('"MfgCode","MfgName"\n')

        # Concatenate output.txt and NSRLMfg-header.txt into NSRLMfg.txt
        print("Concatenating files...")
        with open('NSRLMfg-header.txt', 'r', encoding='utf-8') as header_file, \
            open('output.txt', 'r', encoding='utf-8') as output_file, \
            open('NSRLMfg.txt', 'w', encoding='utf-8') as final_file:
            final_file.write(header_file.read())
            final_file.write(output_file.read())

        print("Files concatenated successfully.")

        # Remove temporary files
        print("Cleaning up temporary files...")
        os.remove('output.txt')
        os.remove('NSRLMfg-header.txt')

        print("##### NSRLMfg.txt created successfully #####")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            end_time = time.time()
            duration = end_time - start_time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nGenerating NSRLMfg.txt ended on: {current_time}. Duration: {duration}")
            print("Connection to the SQLite database closed.")

def generate_NSRLOS(rds_file):
    print("##### Generating NSRLOS.txt #####")
    start_time = time.time()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Generating NSRLOS.txt started on: {current_time}")

    try:
        print("Connecting to the SQLite database...")
        # Connect to the SQLite database
        conn = sqlite3.connect(rds_file)
        cursor = conn.cursor()

        # Increase cache size to 100MB
        print("Setting cache size...")
        cursor.execute("PRAGMA cache_size = 100000")

        # DROP TABLE IF EXISTS EXPORT;
        print("Dropping table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS EXPORT")

        # CREATE TABLE EXPORT AS SELECT ...
        print("Creating EXPORT table...")
        cursor.execute("""
            CREATE TABLE EXPORT AS 
            SELECT operating_system_id, name, version, manufacturer_id FROM OS
        """)

        # Update name and version columns in EXPORT table
        print("Updating name and version columns...")
        cursor.execute("""
            UPDATE EXPORT SET name = REPLACE(name, '"', ''), version = REPLACE(version, '"', '')
        """)

        # Export data to a CSV file
        print("Exporting data to output.txt...")
        with open('output.txt', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Set headers to off manually
            cursor.execute("SELECT operating_system_id, '\"' || name || '\"', '\"' || version || '\"', manufacturer_id FROM EXPORT ORDER BY operating_system_id")
            
            rows = cursor.fetchall()
            total_rows = len(rows)
            for i, row in enumerate(rows):
                csv_writer.writerow(row)
                # Print progress
                print(f"Exporting row {i+1}/{total_rows}...", end='\r')

        print("\nCleaning up output.txt...")
        with open('output.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            data = data.replace('""', '"')
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(data)

        # Create NSRLOS-header.txt
        print("Creating NSRLOS-header.txt...")
        with open('NSRLOS-header.txt', 'w') as header_file:
            header_file.write('"OpSystemCode","OpSystemName","OpSystemVersion","MfgCode"\n')

        # Concatenate output.txt and NSRLOS-header.txt into NSRLOS.txt
        print("Concatenating files...")
        with open('NSRLOS-header.txt', 'r', encoding='utf-8') as header_file, \
            open('output.txt', 'r', encoding='utf-8') as output_file, \
            open('NSRLOS.txt', 'w', encoding='utf-8') as final_file:
            final_file.write(header_file.read())
            final_file.write(output_file.read())

        print("Files concatenated successfully.")

        # Remove temporary files
        print("Cleaning up temporary files...")
        os.remove('output.txt')
        os.remove('NSRLOS-header.txt')

        print("##### NSRLOS.txt created successfully #####")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            end_time = time.time()
            duration = end_time - start_time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nGenerating NSRLOS.txt ended on: {current_time}. Duration: {duration}")
            print("Connection to the SQLite database closed.")

def generate_NSRLProd(rds_file):
    print("##### Generating NSRLProd.txt #####")
    start_time = time.time()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Generating NSRLProd.txt started on: {current_time}")

    try:
        print("Connecting to the SQLite database...")
        # Connect to the SQLite database
        conn = sqlite3.connect(rds_file)
        cursor = conn.cursor()

        # DROP TABLE IF EXISTS EXPORT;
        print("Dropping table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS EXPORT")

        # CREATE TABLE EXPORT AS SELECT ...
        print("Creating EXPORT table...")
        cursor.execute("""
            CREATE TABLE EXPORT AS 
            SELECT package_id, name, version, operating_system_id, manufacturer_id, language, application_type
            FROM PKG
        """)

        # Update name and version columns in EXPORT table
        print("Updating name and version columns...")
        cursor.execute("""
            UPDATE EXPORT SET name = REPLACE(name, '"', ''), version = REPLACE(version, '"', '')
        """)

        # Export data to a CSV file
        print("Exporting data to output.txt...")
        with open('output.txt', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Set headers to off manually
            cursor.execute("""
                SELECT package_id, '"' || name || '"', '"' || version || '"', 
                operating_system_id, manufacturer_id, '"' || language || '"', 
                '"' || application_type || '"'
                FROM EXPORT ORDER BY package_id
            """)
            
            rows = cursor.fetchall()
            total_rows = len(rows)
            for i, row in enumerate(rows):
                csv_writer.writerow(row)
                # Print progress
                print(f"Exporting row {i+1}/{total_rows}...", end='\r')

        print("\nCleaning up output.txt...")
        with open('output.txt', 'r', encoding='utf-8') as file:
            data = file.read()
            data = data.replace('""', '"')
        with open('output.txt', 'w', encoding='utf-8') as file:
            file.write(data)

        # Create NSRLProd-header.txt
        print("Creating NSRLProd-header.txt...")
        with open('NSRLProd-header.txt', 'w') as header_file:
            header_file.write('"ProductCode","ProductName","ProductVersion","OpSystemCode","MfgCode","Language","ApplicationType"\n')

        # Concatenate output.txt and NSRLProd-header.txt into NSRLProd.txt
        print("Concatenating files...")
        with open('NSRLProd-header.txt', 'r', encoding='utf-8') as header_file, \
            open('output.txt', 'r', encoding='utf-8') as output_file, \
            open('NSRLProd.txt', 'w', encoding='utf-8') as final_file:
            final_file.write(header_file.read())
            final_file.write(output_file.read())

        print("Files concatenated successfully.")

        # Remove temporary files
        print("Cleaning up temporary files...")
        os.remove('output.txt')
        os.remove('NSRLProd-header.txt')

        print("##### NSRLProd.txt created successfully #####")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
            end_time = time.time()
            duration = end_time - start_time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nGenerating NSRLProd.txt ended on: {current_time}. Duration: {duration}")
            print("Connection to the SQLite database closed.")

def generate_all_text_files(rds_file):
    generate_NSRLMfg(rds_file)
    generate_NSRLOS(rds_file)
    generate_NSRLProd(rds_file)
    generate_NSRLFile(rds_file)

def get_user_file_path():
    while True:
        file_path = input("Drag and drop your RDS v3 file here (e.g. C:/Downloads/RDS_yyyy.mm.1.db): ")
        if os.path.isfile(file_path):
            return file_path
        else:
            print(f"The file '{file_path}' does not exist. Please try again.")
        
    return file_path

def display_menu():
    print("")
    print("Options:")
    print("1. Generate NSRLFile.txt (~60mins)")
    print("2. Generate NSRLMfg.txt (< 1min)")
    print("3. Generate NSRLOS.txt (< 1min)")
    print("4. Generate NSRLProd.txt (< 1min)")
    print("5. All Text Files (NSRLMfg > NSRLOS > NSRLProd > NSRLFile)")
    print("0. Exit")
    print("")

def get_user_choice():
    choice = input("Enter your choice (0-5): ")
    print("")
    return choice

################# Main Function #################

print_splash_screen()

while True:
    rds_file_path = get_user_file_path()
    display_menu()
    user_choice = get_user_choice()

    if user_choice == '1':
        generate_NSRLFile(rds_file_path)
        break
    elif user_choice == '2':
        generate_NSRLMfg(rds_file_path)
        break
    elif user_choice == '3':
        generate_NSRLOS(rds_file_path)
        break
    elif user_choice == '4':
        generate_NSRLProd(rds_file_path)
        break
    elif user_choice == '5':
        generate_all_text_files(rds_file_path)
        break
    elif user_choice == '0':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")