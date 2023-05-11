
![image](https://github.com/kircktd/HSCR/assets/105011940/3a2c8513-68ae-42b8-a2ec-6f7e67fc576c)
![image](https://github.com/kircktd/HSCR/assets/105011940/d5384010-1323-4d09-9b5d-608f182087dd)


<!-- ABOUT THE PROJECT -->
## About The Project
HSCR is a set of python scripts that queries the underlying Hammerspace filesystems for user specific and system specific metrics. Initially the tool provides reporting on fileshare replication stats, and user capacity and file aging stats. The scripts are designed to run in the backround. The replication monitoring script runs every 5 minutes, and the two file capacity and file aging scripts run in the backround, but wake up only once per day at 3AM and 4AM. Each of these two capacity reporting scripts walk the filesystems and can be Hammerspace Anvil CPU intensive. In light of that it is recommended to only run these once per day during low periods of system utilization. The output files generated by these scripts are feed to Grafana via Prometheous and Windows Exporter.
<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [MS Windows]
* [Python](https://python.org/)
* [Hammerspace Toolkit](https://github.com/hammer-space/hstk)
* [Windows Exporter}(https://github.com/prometheus-community/windows_exporter)
<p align="right">(<a href="#top">back to top</a>)</p>
