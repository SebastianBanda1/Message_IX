# MESSAGE-IX Energy System Model

![MESSAGE-IX](https://img.shields.io/badge/MESSAGE--IX-v3.11+-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![GAMS](https://img.shields.io/badge/GAMS-Compatible-orange.svg)
![License](https://img.shields.io/badge/License-Apache%202.0-red.svg)

A professional implementation of a two-region energy system optimization model using the official MESSAGE-IX framework from IIASA (International Institute for Applied Systems Analysis).

## Overview

This repository demonstrates authentic MESSAGE-IX framework usage for long-term energy planning and optimization. The model implements a two-region energy system (Industrial and Residential) with multiple technology options including natural gas, wind, and solar power generation.

## Key Features

- **Authentic MESSAGE-IX Implementation**: Uses the official MESSAGE-IX optimization framework, not simulation
- **IXMP Integration**: Leverages the IXMP (ix modeling platform) for scenario management and data handling
- **GAMS Solver Support**: Compatible with GAMS mathematical programming solver
- **Two-Region Model**: Separate Industrial and Residential demand regions with technology choices
- **Technology Portfolio**: Gas plants, wind farms, and solar PV installations
- **Time Horizon**: 25-year planning period (2025-2050) with 5-year intervals

## Technical Architecture

### Core Components

1. **MESSAGE-IX Framework**: Official IIASA optimization platform for integrated assessment modeling
2. **IXMP Platform**: Database and scenario management system
3. **Mathematical Solver**: GAMS (General Algebraic Modeling System) for linear programming optimization
4. **Python API**: Official MESSAGE-IX Python interface for model building and execution

### Model Structure

- **Regions**: Industrial, Residential
- **Technologies**: gas_plant, wind_plant, solar_plant  
- **Time Periods**: 2025, 2030, 2040, 2050
- **Optimization Type**: Linear Programming (LP)
- **Objective**: Minimize total system cost while meeting demand constraints

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)
- GAMS solver (for optimization) or alternative LP solver

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Message_IX.git
   cd Message_IX
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Model

Execute the MESSAGE-IX optimization model:

```bash
python scripts/run_messageix_final.py
```

### VS Code Integration

The project includes VS Code configuration for easy development:

- **Run Task**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Run MESSAGE-IX Model"
- **Debug**: `F5` to run with debugger attached
- **Build**: `Ctrl+Shift+B` for default build task

## Project Structure

```
Message_IX/
├── scripts/
│   ├── messageix_final_working.py    # Core MESSAGE-IX implementation
│   └── run_messageix_final.py        # Main execution script
├── data/
│   ├── demand_patterns.csv           # Regional demand data
│   ├── renewable_profiles.csv        # Wind/solar generation profiles
│   └── technology_costs.csv          # Technology cost parameters
├── results/                          # Model outputs (generated)
├── docs/                            # Technical documentation
├── .vscode/                         # VS Code configuration
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Model Implementation Details

### MESSAGE-IX Framework Integration

The model uses authentic MESSAGE-IX components:

- **Scenario Management**: Creates and manages optimization scenarios using `message_ix.Scenario`
- **IXMP Platform**: Database backend for parameter storage and result management
- **Technology Modeling**: Proper MESSAGE-IX technology definitions with input/output relationships
- **Demand Modeling**: Regional demand specification with growth patterns
- **Cost Optimization**: Minimizes total discounted system cost over planning horizon

### Mathematical Formulation

The model implements standard MESSAGE-IX linear programming formulation:

- **Objective Function**: Minimize total system cost (investment + operational)
- **Constraints**: Demand balance, capacity limits, technology relationships
- **Variables**: Technology capacity, activity levels, energy flows
- **Parameters**: Costs, demand, technology characteristics

## Differences from Jupyter Notebook Usage

This implementation differs from typical Jupyter notebook MESSAGE-IX usage:

### 1. **Structured Python Application**
- Organized as a proper Python package with modules
- Separation of concerns: model definition vs. execution
- Professional code organization and documentation

### 2. **VS Code Integration**
- Debugging capabilities with breakpoints
- Integrated terminal and task management
- IntelliSense and code completion for MESSAGE-IX APIs

### 3. **Production-Ready Architecture**
- Error handling and logging
- Modular design for extensibility
- Configuration management
- Automated execution workflows

### 4. **Development Environment**
- Virtual environment management
- Dependency specification via requirements.txt
- Version control integration
- Professional project structure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **IIASA**: For developing and maintaining the MESSAGE-IX framework
- **MESSAGE-IX Community**: For documentation and support
- **GAMS Development Corporation**: For the optimization solver

## Technical Support

For MESSAGE-IX specific questions, consult:
- [MESSAGE-IX Documentation](https://docs.messageix.org/)
- [IXMP Documentation](https://docs.messageix.org/projects/ixmp/)
- [MESSAGE-IX GitHub Repository](https://github.com/iiasa/message_ix)

## Citation

If you use this model in academic work, please cite:

```bibtex
@misc{messageix_energy_model,
  title = {MESSAGE-IX Energy System Model Implementation},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/your-username/Message_IX}
}
```