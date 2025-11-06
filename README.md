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

## Repository Structure

```
Message_IX/
├── .github/               # Repository configuration and templates
├── .vscode/               # VS Code workspace configuration
├── data/                  # Generated datasets and input parameters
│   ├── demand_patterns_baseline_2025_2050.csv
│   ├── demand_patterns_battery_storage_2025_2050.csv
│   ├── renewable_profiles.csv
│   ├── technology_costs_baseline.csv
│   └── technology_costs_battery_storage.csv
├── docs/                  # Technical documentation
│   ├── COMPLETE_PROJECT_GUIDE.md
│   └── technical_documentation.md
├── models/                # MESSAGE-IX model files (reserved)
├── results/               # Analysis outputs and visualizations
│   ├── comprehensive_dashboard_2050.html
│   ├── scenario_comparison_2050.json
│   └── *.png             # Static visualization outputs
├── scripts/               # Core analysis modules
│   ├── run_model.py       # Main energy system model
│   ├── advanced_dashboard.py  # Interactive visualization generator
│   ├── visualize_results.py   # Legacy visualization module
│   └── data_analysis.py   # Statistical analysis module
├── requirements.txt       # Python package dependencies
└── README.md             # This documentation
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment capability (venv or conda)
- 4GB RAM minimum, 8GB recommended

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/SebastianBanda1/Message_IX.git
   cd Message_IX
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Verification
Run the test suite to verify installation:
```bash
python scripts/run_model.py
```

## Usage Guide

### Basic Execution
Execute the complete analysis pipeline:
```bash
python scripts/run_model.py          # Generate scenarios
python scripts/advanced_dashboard.py # Create interactive dashboard
```

### VS Code Integration
For enhanced development experience:
1. Open workspace in VS Code
2. Use Command Palette (Ctrl+Shift+P)
3. Select "Tasks: Run Task" → "Full Analysis Pipeline"

### Output Interpretation
- **Interactive Dashboard**: Open `results/comprehensive_dashboard_2050.html` in web browser
- **Raw Data**: CSV files in `data/` directory for custom analysis
- **Scenario Results**: JSON format in `results/scenario_comparison_2050.json`

## Model Specifications

### Regional Characteristics
- **Industrial Region**: 100 MW baseline demand, 92% load factor, minimal diurnal variation
- **Residential Region**: 80 MW baseline demand, 64% load factor, morning/evening peaks

### Technology Parameters
| Technology | CAPEX 2025 ($/MW) | Capacity Factor | Learning Rate | Lifetime |
|------------|------------------|-----------------|---------------|----------|
| Natural Gas CCGT | 950,000 | 85% | 0% | 30 years |
| Onshore Wind | 1,320,000 | 42% | 8% | 25 years |
| Utility Solar PV | 980,000 | 28% | 15% | 25 years |
| Li-ion Battery | 1,580,000 | 95% | 18% | 15 years |

### Environmental Targets
- 2030: 50% CO2 reduction vs 2025 baseline
- 2040: 75% CO2 reduction vs 2025 baseline  
- 2050: 90% CO2 reduction vs 2025 baseline

## Results Overview

### Scenario Comparison (2025-2050)
| Metric | Baseline | Battery Storage | Improvement |
|--------|----------|-----------------|-------------|
| Cumulative Emissions | 5,405 tons CO2 | 4,634 tons CO2 | -14.3% |
| Renewable Share | 27.5% | 35.0% | +27.3% |
| Peak Demand 2050 | 328 MW | 328 MW | 0% |

### Technology Cost Evolution
- Wind turbine CAPEX: $1.32M/MW (2025) → $164k/MW (2050)
- Solar PV CAPEX: $980k/MW (2025) → $17k/MW (2050)
- Battery CAPEX: $1.58M/MW (2025) → $126k/MW (2050)

## Documentation

### Technical References
- **Complete Guide**: `docs/COMPLETE_PROJECT_GUIDE.md` (15,000+ words)
- **Methodology**: `docs/technical_documentation.md`
- **Data Sources**: NREL ATB 2024, IEA World Energy Outlook 2023, IPCC AR6

### Academic Applications
- Energy systems engineering courses
- Renewable energy integration studies
- Climate policy analysis
- Technology assessment research

## Contributing

This project follows academic software development standards:
- Issue tracking for bug reports and feature requests
- Pull requests for code contributions
- Documentation updates for methodology improvements
- Citation requirements for academic use

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this model in academic work, please cite:

```
@software{message_ix_two_region_2025,
  title={MESSAGE-IX Two-Region Energy System Model},
  author={SebastianBanda1},
  year={2025},
  url={https://github.com/SebastianBanda1/Message_IX}
}
```

## Contact

For questions, issues, or collaboration opportunities:
- GitHub Issues: https://github.com/SebastianBanda1/Message_IX/issues
- Repository: https://github.com/SebastianBanda1/Message_IX

## Acknowledgments

- MESSAGE-IX framework by IIASA
- Technology cost data from NREL Annual Technology Baseline 2024
- Emissions factors from IPCC AR6 Working Group III
- Energy projections from IEA World Energy Outlook 2023