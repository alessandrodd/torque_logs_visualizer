# Torque Logs Visualizer
Quick and dirty interactive dashboard to analyze logs produced by the **Torque APP** ([Torque Lite](https://play.google.com/store/apps/details?id=org.prowl.torquefree)/[Torque Pro](https://play.google.com/store/apps/details?id=org.prowl.torque)).

Note: I'm not affiliated in any way to the Torque App or its developer.

## Demo
https://torquevisualizer.eu.pythonanywhere.com/

## Screenshot
![App screenshot](/screenshots/example.png?raw=true)

## Requirements
Python 3 (tested with Python 3.10)

## Installation
Clone the repository:
```
git clone https://github.com/alessandrodd/torque_logs_visualizer.git
cd torque_logs_visualizer
```
Install the required dependencies
```
pip install -r requirements.txt
```
Run the server
```
python main.py
```

Navigate with your browser to the showed address (by default http://127.0.0.1:8050)

## Usage
- Open your Torque App
- Tap on the gear icon on the lower left, then tap on "Settings"
- Tap on "Data Logging & Upload"
- Tap on "Select what to log" and select all the information you are interested in (e.g. speed, RPM etc.)
- Go back and make sure that the following options are enabled:
  - "Log when Torque is started"
  - "Only when OBD connected"
  - "Automatically log GPS"
  - "Rotate Logfiles"
- Restart the app, connect it to your OBD and start driving!
- One or more .csv files will be produced inside your torqueLogs directory in your phone's Internal Storage

## Known Issues
- Sometimes Torque produces the header multiple times inside the same CSV file. You will have to manually remove the doubles and just leave the initial one in the first line