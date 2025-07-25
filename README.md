# warehouse_bot
# 🏭 Warehouse Robot Simulation (Django + JavaScript)

This ongoing project simulates a warehouse bot using a Django backend and JavaScript frontend. The robot moves through a grid to collect items based on color, avoiding other items using A* pathfinding.

## 🚀 Features

- Grid-based warehouse simulation
- Django-powered backend simulation engine
- JavaScript canvas-based UI
- Color-based item selection (green, blue, yellow)
- Robot avoids unrelated items while finding a path
- Tailwind CSS styled interface

---

## 📦 Project Structure

```
warehouse_bot/
├── manage.py
├── Bot_InWarehouse/
│   └── settings.py
├── robot/
│   ├── views.py
│   ├── urls.py
│   ├── static/robot/
│   │   └── main.js
│   ├── templates/robot/
│   │   └── index.html
│   └── logic/
│       ├── simulator.py
│       ├── warehouse.py
│       ├── robot.py
│       └── pathfinding.py
```

---

## ⚙️ Setup Instructions

### 1. Install dependencies

```bash
pip install django
```

### 2. Create and run project

```bash
python -m django startproject warehouse_project
cd warehouse_project
python manage.py startapp robot
```

Set up the files as per the [Setup Guide](./README.md).

### 3. Run the server

```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at [yout url]

---

## 🖥️ Interface

- Choose a color: Green, Blue, Yellow
- The robot will calculate a path and move step-by-step
- Avoids blocked paths caused by other colored items
- Uses Tailwind CSS for styling

---

## 🧠 Logic & Behavior

- Items are located on grid cells by color
- Robot moves using A* to the nearest matching item
- Avoids other colored items during pathfinding
- Once an item is reached, it is “picked up” and removed

---

## 📌 To-Do / Extensions

- Add item drop-off zones
- Real-time path visualization
- Add sound or success animations
- WebSockets for live updates
- User login for tracking scores/tasks

---

## 📄 License

This project is licensed for demo purposes. Feel free to fork and build on it!
