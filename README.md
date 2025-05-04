# Cloth Simulation v0.2

A sophisticated cloth simulation built using Pygame, demonstrating realistic cloth physics and rendering techniques. The simulation includes features such as dynamic tearing and user interaction for grabbing and cutting the cloth.

## Features

- **Realistic Cloth Physics**: Simulates the behavior of cloth using particle and spring models with verlet integration
- **Dynamic Tearing**: Cloth can tear under stress and weight, creating realistic rips and tears
- **User Interaction**: Allows users to grab and manipulate the cloth, as well as cut it using mouse interactions
- **Multiple Cloth Types**: Supports different cloth shapes including standard cloth and strip patterns
- **Modular Design**: Organized into multiple modules for easy maintenance and extensibility

## Project Structure

```
cloth-simulation
├── src
│   ├── main.py                # Entry point of the application
│   ├── cloth/                 # Core cloth simulation components
│   │   ├── __init__.py
│   │   ├── particle.py        # Defines the Particle class
│   │   ├── spring.py          # Defines the Spring class
│   │   └── cloth_system.py    # Manages the overall cloth simulation
│   ├── graphics/              # Rendering and visualization
│   │   ├── __init__.py
│   │   └── renderer.py        # Handles rendering of the simulation
│   ├── physics/              # Physics calculations and constraints
│   │   ├── __init__.py
│   │   └── constraints.py     # Physics constraints implementation
│   ├── interaction/          # User interaction handling
│   │   ├── __init__.py
│   │   └── input_handler.py   # Manages user input and interactions
│   └── ui/                   # User interface components
│       ├── __init__.py
│       ├── button.py         # Defines the Button class
│       └── interface.py      # Manages the user interface
├── assets/                   # Static assets and resources
├── requirements.txt          # Project dependencies
├── LICENSE                   # MIT License
└── README.md                # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/colingalbraith/Cloth-Simulation-.git
   cd cloth-simulation
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the simulation:
   ```bash
   python src/main.py
   ```

## Usage

### Controls
- **Grab Tool**: Click and drag to grab and manipulate the cloth
- **Cut Tool**: Click to cut the cloth at the mouse position
- **Reset**: Press 'R' to reset the simulation
- **Pause/Resume**: Press 'Space' to toggle simulation

### Cloth Types
- **Standard Cloth**: Creates a rectangular cloth (30x25 grid)
- **Strip**: Creates a long strip of cloth (60x10 grid)

### UI Elements
- Use the buttons at the bottom of the screen to:
  - Switch between different cloth types
  - Toggle between grab and cut tools
- The simulation runs at 800x800 resolution

## Physics Parameters

The simulation uses the following key parameters:
- Gravity: 0.15 (gentle fall)
- Spring Strength: 0.2 (stronger connections)
- Damping: 0.99 (reduced oscillation)
- Spring Breaking Thresholds:
  - Structural: 5.0
  - Shear: 4.0
  - Bend: 3.0

## Development

### Code Style
This project follows PEP 8 style guidelines. To ensure code quality:
1. Use meaningful variable and function names
2. Include docstrings for all functions and classes
3. Keep functions focused and modular
4. Write unit tests for critical components

### Running Tests
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Pygame community for the excellent game development library
- Contributors and users of this project
