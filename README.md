## Hammertrack
![image](https://github.com/kircktd/HSCR/assets/105011940/3a2c8513-68ae-42b8-a2ec-6f7e67fc576c)
![image](https://github.com/kircktd/HSCR/assets/105011940/d5384010-1323-4d09-9b5d-608f182087dd)

HSCS is a custom reporting is a set of Python scripts that are designed to run on a windows platform. HSCS utilizes the Hammerspace toolkit (HSTK), and extracts user and other systems stats from the underlying Hammerspace file system. The output files generated by these scripts are feed to Grafana via Prometheous and Windows Exporter.

<!-- ABOUT THE PROJECT -->
## About The Project
Hammertrack is a Ftrack listener that monitors changes to custom location fields in the Ftrack application. Changes to location settings
triggers updates to custom metadata on files and directories associated with specific tasks within Ftrack. This metadata can be used to drive data placement and location
using SmartObjectives on a Hammerspace Global Data Environment.

Currently, hammertrack.py watches for location fields to be added to or removed from Tasks in Ftrack. When 
it sees a location label in the custom field it adds them as Hammerspace labels to the root 
of the specified task folders on a Hammerspace file system. The label schema is configured in Ftrack to match the configuration in hammertrack.py,
and the label names are passed through directly as Hammerspace labels.

<p align="right">(<a href="#top">back to top</a>)</p>
