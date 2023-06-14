$filename = "C:\Reporting\tmp\user_list.txt"
$users = Get-Content -Path $filename
$sharePaths = @("Z:\", "Y:\", "X:\")
$outputFile = "user_files.txt"  # Change the output file name

$lines = @()

foreach ($user in $users) {
    $userProfile = "C:\Users\$user"

    if (Test-Path $userProfile) {
        $userPath = Join-Path -Path $userProfile -ChildPath "Documents"

        if (Test-Path $userPath) {
            $files = Get-ChildItem -Path $userPath -Recurse -File

            foreach ($file in $files) {
                $filePath = $file.FullName
                $fileSize = [Math]::Round(($file.Length / 1MB), 0)
                $fileOwner = (Get-Acl -Path $filePath).Owner.Replace("SELAB\", "")

                if ($fileSize -ge 100) {
                    $line = "{0},{1},{2}" -f $filePath, $fileSize, $fileOwner
                    $lines += $line
                }
            }
        }
        else {
            # No files found for user
        }
    }
    else {
        # User profile not found
    }
}

foreach ($sharePath in $sharePaths) {
    $shareFiles = Get-ChildItem -Path $sharePath -Recurse -File

    if ($shareFiles) {
        foreach ($file in $shareFiles) {
            $filePath = $file.FullName
            $fileSize = [Math]::Round(($file.Length / 1MB), 0)
            $fileOwner = (Get-Acl -Path $filePath).Owner.Replace("SELAB\", "")

            if ($fileSize -ge 100) {
                $line = "{0},{1},{2}" -f $filePath, $fileSize, $fileOwner
                $lines += $line
            }
        }
    }
    else {
        # No files found in the shared folder
    }
}

$lines | Where-Object { $_ -notmatch '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' -and $_ -notlike "*0," } |
    Out-File -FilePath $outputFile -Encoding UTF8  # Specify UTF-8 encoding
