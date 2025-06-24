import os
import subprocess
from datetime import datetime
from tqdm import tqdm  # Progress bar

# Parameters: Set your directories here
iso_base_directory = "H:\\ps3"
output_directory = "F:\\decrypted isos"

def log_message(message, log_file_path):
    """
    Logs a message with a timestamp to both the console and a specified log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')

def main():
    """
    Main function to decrypt ISO files using their corresponding .dkey files.
    """
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except Exception as e:
            print(f"Failed to create output directory: {output_directory}")
            return

    log_file_path = os.path.join(output_directory, "decryption_log.txt")

    # Recursively find all ISO files in the base directory
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

        # Read key from the .dkey file
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

        # Skip already decrypted files
        if os.path.exists(decrypted_file_name):
            log_message(f"Decrypted file already exists for {iso_file_name}. Skipping...", log_file_path)
            continue

        log_message(f"Decrypting {iso_file} to {decrypted_file_name} with key from {os.path.basename(dkey_file)}...", log_file_path)

        # Path to the ps3dec executable
        ps3dec_path = "H:\\ps3\\ps3dec.exe"
        arguments = ["d", "key", decryption_key, iso_file, decrypted_file_name]
        try:
            with open(os.path.join(output_directory, "ps3dec_output.txt"), 'a') as stdout_file, \
                 open(os.path.join(output_directory, "ps3dec_error.txt"), 'a') as stderr_file:
                subprocess.run([ps3dec_path] + arguments, stdout=stdout_file, stderr=stderr_file, check=True)
        except subprocess.CalledProcessError as e:
            log_message(f"Error decrypting {iso_file_name}: {e}", log_file_path)

    print(f"All ISO files processed. Log file created at {log_file_path}.")

if __name__ == "__main__":
    main()