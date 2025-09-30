# 🏌️ GolfSim

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flet](https://img.shields.io/badge/Flet-GUI_Framework-00BFA5?logo=flet)
![FastAPI](https://img.shields.io/badge/FastAPI-Web_Framework-009688?logo=fastapi)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?logo=opencv)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Web_Automation-43B02A?logo=selenium)

## 📖 About the Project
**GolfSim** is a golf simulator with shot analysis and statistics visualization.  
The system consists of a **desktop application** and a **mobile client**:

- The mobile app tracks the ball by color and detects the moment of impact.  
- The shot video is transmitted over the local network to the PC.  
- The desktop app analyzes ball speed, launch angle, and calculates distance using [FlightScope Trajectory](https://trajectory.flightscope.com/) (a stub implementation is included; you can integrate your own service or calculations).  
- Shot results are displayed in a sortable and filterable table.  

📱 Mobile app: [GolfSim Mobile](https://github.com/l-Spook-l/golfSim-mobile)  

⚠️ **Important:** The distance between the camera and the ball must be **50 cm** for accurate tracking.  

---

## 🚀 Features
- Ball tracking and impact analysis (launch angles and ball speed).  
- Automatic data transfer between devices via local network.  
- Shot history stored in a table (sorting and filters).  

### 🔜 Upcoming Features (in development)
- Putting mode.  
- Full 18-hole gameplay.  
- Player profile support.  

---

## 🖼️ Screenshots
### Main Menu:  
![Main Menu](docs/images/main_menu.png)  

### Driving Range Table:  
![Driving Range](docs/images/drive_range_table.png)  

### Color settings & active profile switch:  
![Color Settings](docs/gif/set_color.gif)  
![Switch Active Profile](docs/gif/change_active_set.gif)  

---

## 📦 Installation & Run
```bash
git clone https://github.com/l-Spook-l/golfsim-core.git
cd golfSim
pip install -r requirements.txt
python main.py
```

---

## Developers
- https://github.com/l-Spook-l

## Contact

If you have any questions or suggestions for improving the project, please contact serhii.mykhailovskyi.ua@gmail.com.
