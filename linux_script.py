import os
import subprocess
from datetime import datetime
from tqdm import tqdm  # Import tqdm for progress bar

# Parameters
iso_base_directory = "/mnt/ps3"
output_directory = "/mnt/decrypted_isos"

# Key map
key_map = {
    "Call of Duty - Black Ops (Europe) (En,Fr).iso": "3FE7CC8D21057316F51B2C655418FFBE",
    "Call of Duty - Black Ops II (Europe) (En,Fr).iso": "B4C42C52267A5219AA2BDF0D95717B32",
    "Call of Duty - Black Ops III (Europe) (En,Fr,De,Es,It,Pl,Ru).iso": "1CB30B753AC2B0763588DAA9EA29BB50",
    "Call of Duty - Ghosts (Europe) (En,Fr,De,Es,It).iso": "B7FF1C257D65D83268E59A3D659AA677",
    "Call of Duty - Modern Warfare 2 (Europe).iso": "4B0982BE00DD1765701CA1D3F492234F",
    "Call of Duty 3 (Europe).iso": "BEFBA4E304EA5A35DB8517E1EA3ACAB0",
    "Call of Duty 4 - Modern Warfare (Europe).iso": "8A7D3CC1F3DAF58FAF6D64C2BA4E06B0",
    "Castlevania - Lords of Shadow (Europe) (En,Fr,De,Es,It).iso": "E27DD767561CFEB1C35234B5FB1CD8DF",
    "Castlevania - Lords of Shadow 2 (Europe) (En,Fr,De,Es,It,Pt).iso": "524EC9C14EBF9907F82238C5135D680F",
    "Disney Epic Mickey 2 - The Power of Two (Europe) (En,Sv,No,Da,Pl,Cs,Ar,Tr).iso": "99D22BE8424022AD92BA4EBB63D73F46",
    "Jak and Daxter Trilogy, The (Europe) (En,Fr,De,Es,It,Pt,Ru).iso": "012BEA99A9FF0E98520A19FF1777FF71",
    "Metal Gear Rising - Revengeance (Europe) (En,Ja,Fr,De,Es,It,Pt).iso": "5E3C893016943F4AFB7D49E105E6A035",
    "Metal Gear Solid - HD Collection (Europe) (En,Fr,De,Es,It).iso": "10F203245D5715CDEC04D54561C9CEA8",
    "Metal Gear Solid 4 - Guns of the Patriots (Europe) (En,Fr,De,Es,It) (v02.00).iso": "1D7ECBDB6DB07261B235698E7C270CD4",
    "MotorStorm - Apocalypse (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko,Pl,Ru) (v02.00).iso": "9D72C9A54084164BC81D63431D7CEAB8",
    "MotorStorm - Complete Edition (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko).iso": "1D4D87BB19E172F4B2DE9485C090268F",
    "Resistance - Fall of Man (Europe, Australia) (En,Ja,Fr,De,Es,It,Nl,Pt,Ko).iso": "4CDF87A93177CB7EA9EA7DF48F6ACC65",
    "Resistance 2 (Europe) (En,Ja,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko).iso": "19D32E488F8253F4CEA8643641C6B13E",
    "Resistance 3 (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Pl,Ru).iso": "A185C7D27C5CD0F183026EAAAEAF186A",
}

def log_message(message, log_file_path):
    """
    Logs a message with a timestamp to both the console and a specified log file.

    Args:
        message (str): The message to log.
        log_file_path (str): The path to the log file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')

def main():
    """
    Main function to decrypt ISO files using specified keys and log the process.
    It checks for the existence of the output directory, processes each ISO file,
    and logs the decryption status.
    """
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except Exception as e:
            print(f"Failed to create output directory: {output_directory}")
            return

    log_file_path = os.path.join(output_directory, "decryption_log.txt")
    iso_files = [os.path.join(root, file)
                 for root, _, files in os.walk(iso_base_directory)
                 for file in files if file.endswith('.iso')]

    if not iso_files:
        print(f"No ISO files found in the directory: {iso_base_directory}")
        return

    for iso_file in tqdm(iso_files, desc="Decrypting ISOs", unit="file"):
        iso_file_name = os.path.basename(iso_file)
        if iso_file_name in key_map:
            decryption_key = key_map[iso_file_name]
            decrypted_file_name = os.path.join(output_directory, os.path.splitext(iso_file_name)[0] + ".iso")

            if os.path.exists(decrypted_file_name):
                log_message(f"Decrypted file already exists for {iso_file_name}. Skipping...", log_file_path)
                continue

            log_message(f"Decrypting {iso_file} to {decrypted_file_name} with key '{decryption_key}'...", log_file_path)

            ps3dec_path = "/mnt/ps3/ps3dec"  # Ensure this path is correct
            arguments = ["d", "key", decryption_key, iso_file, decrypted_file_name]
            try:
                with open(os.path.join(output_directory, "ps3dec_output.txt"), 'w') as stdout_file, \
                     open(os.path.join(output_directory, "ps3dec_error.txt"), 'w') as stderr_file:
                    subprocess.run([ps3dec_path] + arguments, stdout=stdout_file, stderr=stderr_file, check=True)
            except subprocess.CalledProcessError as e:
                log_message(f"Error decrypting {iso_file_name}: {e}", log_file_path)
        else:
            log_message(f"No key found for {iso_file_name}. Skipping...", log_file_path)

    print(f"All ISO files processed. Log file created at {log_file_path}.")

if __name__ == "__main__":
    main()
