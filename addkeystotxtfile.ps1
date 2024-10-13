# Define the main directory containing the .dkey files and the subfolders with ISO files
$dkeyDirectory = "H:\ps3"  # Directory where .dkey files are located
$isoBaseDirectory = "H:\ps3"  # Base directory containing subfolders with ISO files
$keyFilePath = Join-Path -Path (Get-Location) -ChildPath "keys.txt"

# Ensure keys.txt exists
if (-not (Test-Path -Path $keyFilePath)) {
    New-Item -ItemType File -Path $keyFilePath
}

# Get all .iso files in the subdirectories of the specified base directory
$isoFiles = Get-ChildItem -Path $isoBaseDirectory -Filter *.iso -File -Recurse

# Check if any ISO files were found
if ($isoFiles.Count -eq 0) {
    Write-Host "No ISO files found in the directory: $isoBaseDirectory"
} else {
    # Loop through each ISO file
    foreach ($isoFile in $isoFiles) {
        # Construct the corresponding .dkey file path
        $dkeyFilePath = Join-Path -Path $dkeyDirectory -ChildPath ([System.IO.Path]::GetFileNameWithoutExtension($isoFile.Name) + ".dkey")

        # Check if the .dkey file exists
        if (Test-Path -Path $dkeyFilePath) {
            # Read the key from the .dkey file
            $decryptionKey = Get-Content -Path $dkeyFilePath -ErrorAction SilentlyContinue
            
            # Create the entry for keys.txt
            $newEntry = "$($isoFile.Name) $decryptionKey"

            # Append the new entry to keys.txt
            Add-Content -Path $keyFilePath -Value $newEntry
            Write-Host "Entry added to keys.txt: $newEntry"
        } else {
            Write-Host "No corresponding .dkey file found for $($isoFile.Name). Skipping..."
        }
    }
}

Write-Host "All ISO files processed."