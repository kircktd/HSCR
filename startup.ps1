# List of Python scripts to launch
$python_scripts = @(
    "C:\Reporting\Scripts\repstats.py",
    "C:\Reporting\Scripts\userstats.py",
    "C:\Reporting\Scripts\userstats_aged.py",
    "C:\Reporting\Scripts\filelist_aged.py"
)
# Loop through the list and launch each script
foreach ($script in $python_scripts) {
    Start-Process python.exe -ArgumentList $script
}
#Defined paths Windows Exporter & Prometheus
$windowsExporterPath = "C:\Program Files\windows_exporter\windows_exporter-0.20.0-amd64.exe"
$prometheusPath = "C:\Reporting\Prometheus\prometheus-2.43.0.windows-amd64\prometheus.exe"

Start-Process -FilePath "C:\Program Files\Windows Exporter\we.exe"
Start-Process -FilePath $prometheusPath -ArgumentList "--config.file=C:\Reporting\Prometheus\prometheus-2.43.0.windows-amd64\prometheus.yml" -NoNewWindow
