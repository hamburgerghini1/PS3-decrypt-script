param (
    [string]$isoBaseDirectory = "H:\ps3",
    [string]$outputDirectory = "F:\decrypted isos"
)

$keyMap = @{
    "Call of Duty - Black Ops (Europe) (En,Fr).iso" = "3FE7CC8D21057316F51B2C655418FFBE"
    "Call of Duty - Black Ops II (Europe) (En,Fr).iso" = "B4C42C52267A5219AA2BDF0D95717B32"
    "Call of Duty - Black Ops III (Europe) (En,Fr,De,Es,It,Pl,Ru).iso" = "1CB30B753AC2B0763588DAA9EA29BB50"
    "Call of Duty - Ghosts (Europe) (En,Fr,De,Es,It).iso" = "B7FF1C257D65D83268E59A3D659AA677"
    "Call of Duty - Modern Warfare 2 (Europe).iso" = "4B0982BE00DD1765701CA1D3F492234F"
    "Call of Duty 3 (Europe).iso" = "BEFBA4E304EA5A35DB8517E1EA3ACAB0"
    "Call of Duty 4 - Modern Warfare (Europe).iso" = "8A7D3CC1F3DAF58FAF6D64C2BA4E06B0"
    "Castlevania - Lords of Shadow (Europe) (En,Fr,De,Es,It).iso" = "E27DD767561CFEB1C35234B5FB1CD8DF"
    "Castlevania - Lords of Shadow 2 (Europe) (En,Fr,De,Es,It,Pt).iso" = "524EC9C14EBF9907F82238C5135D680F"
    "Disney Epic Mickey 2 - The Power of Two (Europe) (En,Sv,No,Da,Pl,Cs,Ar,Tr).iso" = "99D22BE8424022AD92BA4EBB63D73F46"
    "Jak and Daxter Trilogy, The (Europe) (En,Fr,De,Es,It,Pt,Ru).iso" = "012BEA99A9FF0E98520A19FF1777FF71"
    "Metal Gear Rising - Revengeance (Europe) (En,Ja,Fr,De,Es,It,Pt).iso" = "5E3C893016943F4AFB7D49E105E6A035"
    "Metal Gear Solid - HD Collection (Europe) (En,Fr,De,Es,It).iso" = "10F203245D5715CDEC04D54561C9CEA8"
    "Metal Gear Solid 4 - Guns of the Patriots (Europe) (En,Fr,De,Es,It) (v02.00).iso" = "1D7ECBDB6DB07261B235698E7C270CD4"
    "MotorStorm - Apocalypse (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko,Pl,Ru) (v02.00).iso" = "9D72C9A54084164BC81D63431D7CEAB8"
    "MotorStorm - Complete Edition (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko).iso" = "1D4D87BB19E172F4B2DE9485C090268F"
    "Resistance - Fall of Man (Europe, Australia) (En,Ja,Fr,De,Es,It,Nl,Pt,Ko).iso" = "4CDF87A93177CB7EA9EA7DF48F6ACC65"
    "Resistance 2 (Europe) (En,Ja,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Ko).iso" = "19D32E488F8253F4CEA8643641C6B13E"
    "Resistance 3 (Europe) (En,Fr,De,Es,It,Nl,Pt,Sv,No,Da,Fi,Pl,Ru).iso" = "A185C7D27C5CD0F183026EAAAEAF186A"
}

function Log-Message {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Write-Host $logEntry
    Add-Content -Path $logFilePath -Value $logEntry
}

$isoFiles = Get-ChildItem -Path $isoBaseDirectory -Filter *.iso -File -Recurse

if ($isoFiles.Count -eq 0) {
    Write-Host "No ISO files found in the directory: $isoBaseDirectory"
} else {
    if (-not (Test-Path -Path $outputDirectory)) {
        try {
            New-Item -ItemType Directory -Path $outputDirectory | Out-Null
        } catch {
            Write-Host "Failed to create output directory: $outputDirectory"
            exit
        }
    }

    $logFilePath = Join-Path -Path $outputDirectory -ChildPath "decryption_log.txt"

    foreach ($isoFile in $isoFiles) {
        if ($keyMap.ContainsKey($isoFile.Name)) {
            $decryptionKey = $keyMap[$isoFile.Name]
            $decryptedFileName = Join-Path -Path $outputDirectory -ChildPath "$($isoFile.BaseName).iso"

            if (Test-Path -Path $decryptedFileName) {
                Log-Message "Decrypted file already exists for $($isoFile.Name). Skipping..."
                continue
            }

            $logMessage = "Decrypting $($isoFile.FullName) to $decryptedFileName with key '$decryptionKey'..."
            Log-Message $logMessage

            $ps3decPath = "H:\ps3\ps3dec.exe"
            $arguments = @("d", "key", $decryptionKey, "in", $isoFile.FullName, $decryptedFileName)

            try {
                Start-Process -FilePath $ps3decPath `
                    -ArgumentList $arguments `
                    -Wait `
                    -NoNewWindow `
                    -RedirectStandardOutput "$outputDirectory\ps3dec_output.txt" `
                    -RedirectStandardError "$outputDirectory\ps3dec_error.txt"
            } catch {
                Log-Message "Error decrypting $($isoFile.Name): $_"
            }
        } else {
            $noKeyMessage = "No key found for $($isoFile.Name). Skipping..."
            Log-Message $noKeyMessage
        }
    }
}

Write-Host "All ISO files processed. Log file created at $logFilePath."