# MESSAGE-IX Two-Region Energy System Model

A professional energy system modeling project using the MESSAGE-IX framework to simulate a 2-region energy system with industrial and residential demand patterns, featuring natural gas as the dominant source alongside wind and solar renewables.

## Project Overview

This project models an energy system with:
- **Two regions**: Industrial and residential zones
- **Demand patterns**: 
  - Industrial: Constant baseline demand
  - Residential: Peak demand in morning and evening
- **Energy sources**: Natural gas (dominant), wind, and solar
- **Variability modeling**: Weather-dependent renewable generation and demand fluctuations

## Features

- MESSAGE-IX integration for optimization modeling
- Realistic demand pattern simulation
- Renewable energy variability modeling
- Comprehensive data visualization
- Professional reporting and analysis

## Project Structure

```
Message_IX/
├── data/           # Input data files
├── models/         # MESSAGE-IX model definitions
├── scripts/        # Python analysis scripts
├── results/        # Output data and plots
├── docs/          # Documentation
└── README.md      # This file
```

## Requirements

- Python 3.8+
- MESSAGE-IX framework
- Pandas, NumPy, Matplotlib, Seaborn
- Jupyter Notebook (optional)

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run the main model: `python scripts/run_model.py`
3. Generate visualizations: `python scripts/visualize_results.py`

## Documentation

See `/docs/` for detailed methodology and model descriptions.

## License

MIT License - see LICENSE file for details.