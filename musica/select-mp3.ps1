param(
    [string]$MusicFolder = "$env:USERPROFILE\Music"
)

$files = Get-ChildItem -Path $MusicFolder -Filter *.mp3 | Sort-Object Name

if ($files.Count -eq 0) {
    Write-Host "No hay archivos mp3 en la carpeta $MusicFolder"
    pause
    exit 1
}

function Show-Menu {
    param([array]$Items)

    $selectedIndex = 0

    while ($true) {
        Clear-Host
        Write-Host ""
        Write-Host "ENTER para reproducir, ESC para salir."
        Write-Host "Biblioteca de Musica:`n" -ForegroundColor Yellow

        for ($i = 0; $i -lt $Items.Count; $i++) {
            if ($i -eq $selectedIndex) {
                Write-Host ("➤ " + $Items[$i].Name) -ForegroundColor Cyan
            } else {
                Write-Host ("  " + $Items[$i].Name)
            }
        }

        $key = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

        switch ($key.VirtualKeyCode) {
            38 { $selectedIndex = ($selectedIndex - 1 + $Items.Count) % $Items.Count }
            40 { $selectedIndex = ($selectedIndex + 1) % $Items.Count }
            13 { return $Items[$selectedIndex].FullName }
            27 { return $null }
        }
    }
}

$selectedFile = Show-Menu -Items $files

if ($selectedFile) {
    Clear-Host
    Write-Host "Reproduciendo:`n$selectedFile`n" -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "ffplay" -ArgumentList "-nodisp -autoexit -loglevel quiet `"$selectedFile`""
} else {
    Write-Host "No se seleccionó ninguna canción." -ForegroundColor DarkGray
}

pause
