import os
import subprocess
from datetime import datetime
from tqdm import tqdm
import threading

iso_base_directory = r"C:\Users\tommi\Downloads"
output_directory = r"D:\emu\ps3"

def log_message(message, log_file_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')

def stream_reader(pipe, log_file):
    for line in iter(pipe.readline, ''):
        print(line, end='')      # Print to console
        log_file.write(line)     # Write to log file
    pipe.close()

def main():
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except Exception as e:
            print(f"Failed to create output directory: {output_directory}")
            return

    log_file_path = os.path.join(output_directory, "decryption_log.txt")
    outlog_path = os.path.join(output_directory, "ps3dec_output.txt")
    errlog_path = os.path.join(output_directory, "ps3dec_error.txt")

    iso_files = [os.path.join(root, file)
                 for root, _, files in os.walk(iso_base_directory)
                 for file in files if file.lower().endswith('.iso')]

    if not iso_files:
        print(f"No ISO files found in the directory: {iso_base_directory}")
        return

    for iso_file in tqdm(iso_files, desc="Decrypting ISOs", unit="file"):
        iso_file_name = os.path.basename(iso_file)
        iso_dir = os.path.dirname(iso_file)
        dkey_file = os.path.join(iso_dir, os.path.splitext(iso_file_name)[0] + ".dkey")

        if not os.path.exists(dkey_file):
            log_message(f"No .dkey file found for {iso_file_name}. Skipping...", log_file_path)
            continue

        try:
            with open(dkey_file, "r") as f:
                decryption_key = f.read().strip()
            if not decryption_key:
                log_message(f".dkey file is empty for {iso_file_name}. Skipping...", log_file_path)
                continue
        except Exception as e:
            log_message(f"Failed to read .dkey file for {iso_file_name}: {e}. Skipping...", log_file_path)
            continue

        decrypted_file_name = os.path.join(output_directory, os.path.splitext(iso_file_name)[0] + ".iso")

        if os.path.exists(decrypted_file_name):
            log_message(f"Decrypted file already exists for {iso_file_name}. Skipping...", log_file_path)
            continue

        log_message(f"Decrypting {iso_file} to {decrypted_file_name} with key from {os.path.basename(dkey_file)}...", log_file_path)

        ps3dec_path = r"C:\Users\tommi\Documents\GitHub\PS3-decrypt-script\ps3dec\ps3dec.exe"
        arguments = ["d", "key", decryption_key, iso_file, decrypted_file_name]
        try:
            with open(outlog_path, 'a', encoding='utf-8') as outlog_file, \
                 open(errlog_path, 'a', encoding='utf-8') as errlog_file:
                process = subprocess.Popen(
                    [ps3dec_path] + arguments,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )

                threads = []
                threads.append(threading.Thread(target=stream_reader, args=(process.stdout, outlog_file)))
                threads.append(threading.Thread(target=stream_reader, args=(process.stderr, errlog_file)))
                for t in threads:
                    t.start()
                process.wait()
                for t in threads:
                    t.join()
                if process.returncode != 0:
                    log_message(f"Error decrypting {iso_file_name}: ps3dec exited with code {process.returncode}", log_file_path)
        except Exception as e:
            log_message(f"Exception occurred while decrypting {iso_file_name}: {e}", log_file_path)

    print(f"All ISO files processed. Log file created at {log_file_path}.")

if __name__ == "__main__":
    main()