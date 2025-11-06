# MESSAGE-IX Two-Region Energy System Model

A comprehensive energy system modeling framework implementing MESSAGE-IX for long-term energy planning analysis. This project provides scenario-based modeling capabilities for energy system transitions from 2025 to 2050, incorporating realistic technology costs, environmental constraints, and renewable energy integration with storage solutions.

## Abstract

This energy system model analyzes the transition pathways for a two-region electricity system under different technology deployment scenarios. The model incorporates real-world technology cost projections from NREL ATB 2024, learning curve effects, and environmental targets aligned with climate goals. Two primary scenarios are evaluated: a baseline transition and an accelerated pathway incorporating lithium-ion battery storage for enhanced renewable integration.

## Key Capabilities

- **Multi-year Projections**: 26-year analysis period (2025-2050) with annual time steps
- **Demand Growth Modeling**: 2.3% annual electricity demand growth with regional differentiation
- **Technology Portfolio**: Natural gas combined cycle, onshore wind, utility-scale solar PV, lithium-ion battery storage
- **Economic Analysis**: Levelized cost of energy (LCOE) calculations with learning curve cost reductions
- **Environmental Assessment**: CO2 emissions tracking with decarbonization target evaluation
- **Scenario Comparison**: Baseline vs battery storage integration pathways
- **Interactive Analytics**: Web-based dashboard for comprehensive results visualization

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