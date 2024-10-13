$maindir = "H:\ps3"
$destinationdir = "F:\decrypted isos"
$ps3decPath = "C:\Path\To\Your\ps3dec.exe" # Update with the actual path to ps3dec.exe

# Check if destination directory exists, create if it doesn't
if (-not (Test-Path -Path $destinationdir)) {
    New-Item -ItemType Directory -Path $destinationdir
}

# Get all subdirectories in the main directory
$folders = Get-ChildItem -Path $maindir -Directory

# Process each folder
foreach ($folder in $folders) {
    $isoFilePath = Get-ChildItem -Path $folder.FullName -Filter *.iso -File -ErrorAction SilentlyContinue

    if ($isoFilePath) {
        $decryptedFileName = Join-Path -Path $destinationdir -ChildPath "$($folder.Name).dec"
        
        # Log the command being executed
        Write-Host "Decrypting $($isoFilePath.FullName) to $decryptedFileName..."
        
        # Execute the decryption command
        & $ps3decPath -o $decryptedFileName $isoFilePath.FullName
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Decryption successful: $decryptedFileName"
        } else {
            Write-Host "Decryption failed for $($isoFilePath.FullName) with exit code $LASTEXITCODE."
        }
    } else {
        Write-Host "Required files not found in $($folder.FullName). Skipping..."
    }
}

Write-Host "All folders processed."
