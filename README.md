# Yogurt Production Optimizer

A Flask-based web application that uses genetic algorithms to optimize yogurt production scheduling across multiple production lines.

## Features

- **Genetic Algorithm Optimization**: Finds optimal production schedules to minimize total production time
- **Multi-line Production**: Schedules production across 5 different production lines with varying capacities
- **Cleaning Time Management**: Accounts for line cleaning time when switching between yogurt types
- **Interactive Gantt Chart**: Visualizes the production schedule with a color-coded Gantt chart
- **19 Yogurt Types**: Handles production planning for various yogurt flavors

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 9
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the Web Application

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

### Run Optimization Directly

```bash
python ga_optimization.py
```

This will run the genetic algorithm and generate a Gantt chart showing the optimized production schedule.

## Project Structure

- `app.py` - Flask web application
- `yp.py` - Production configuration and Gantt chart generation
- `ga_optimization.py` - Genetic algorithm implementation
- `templates/` - HTML templates for the web interface
  - `index.html` - Home page
  - `result.html` - Results display page

## Production Configuration

### Production Lines
- 5 production lines with capacities ranging from 0.5 to 0.6 units/minute
- Cleaning time: 20-30 minutes per line

### Yogurt Types
19 different yogurt types with varying production quantities (30-300 units):
- Classic, Fruit, Greek, Strawberry, Vanilla
- Chocolate, Honey, Blueberry, Raspberry, Mango
- Coconut, Lemon, Peach, Pineapple
- Green Tea, Matcha, Coffee, Almond, Hazelnut

### Time Constraint
- Total production must complete within 24 hours (1440 minutes)

## Algorithm Parameters

- Population Size: 30
- Generations: 300
- Mutation Rate: 0.2

## Technologies Used

- Python 3
- Flask - Web framework
- SimPy - Simulation framework
- NumPy - Numerical computing
- Matplotlib - Gantt chart visualization

## License

MIT License
