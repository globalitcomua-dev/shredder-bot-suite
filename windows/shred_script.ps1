# WARNING: This script destroys data. USE WITH CAUTION.

$targetPaths = @(
    "C:\SensitiveData",
    "D:\SecretBackups"
)

foreach ($path in $targetPaths) {
    if (Test-Path $path) {
        Get-ChildItem -Path $path -Recurse -Force | ForEach-Object {
            try {
                $size = (Get-Item $_.FullName).Length
                $randomData = [byte[]]::new($size)
                (New-Object Random).NextBytes($randomData)
                [System.IO.File]::WriteAllBytes($_.FullName, $randomData)
                Remove-Item $_.FullName -Force
            } catch { continue }
        }
        Remove-Item $path -Recurse -Force
    }
}

# Optionally shutdown:
# Stop-Computer -Force
