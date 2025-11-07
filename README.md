# MESSAGE-IX Energy System Dashboard

![MESSAGE-IX](https://img.shields.io/badge/MESSAGE--IX-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![GAMS](https://img.shields.io/badge/GAMS-Solver-orange.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)

**Professional energy system optimization platform with comprehensive interactive dashboard for strategic energy planning.**

## Overview

Complete energy optimization system featuring MESSAGE-IX framework with real-time visualization dashboard. Models a two-region energy system (Industrial and Residential zones) with natural gas, wind, and solar technologies for the planning period 2025-2050.

## Key Features

- **Advanced Energy Modeling**: MESSAGE-IX optimization framework
- **Interactive Dashboard**: Complete visualization suite with Streamlit
- **Real Optimization**: GAMS solver with linear programming
- **Multi-Regional Model**: Industrial and Residential zones
- **Technology Portfolio**: Gas, wind and solar technologies
- **Long-term Analysis**: 25-year planning horizon

## Quick Start

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/SebastianBanda1/Message_IX.git
cd Message_IX

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Energy Model
```bash
python scripts/run_messageix_final.py
```

### 3. Launch Dashboard
```bash
python launch_dashboard.py
```
*Dashboard will automatically open at `http://localhost:8501`*

## Dashboard Features

### Dashboard Capabilities:

#### **Executive Summary**
- Key system metrics
- Optimized total cost ($676.79M USD)
- Regional and technology overview
- Model verification status

#### **Cost Analysis**
- Detailed cost breakdown
- Interactive pie and bar charts
- Investment, operation and fuel costs
- Percentage analysis

#### **Capacity Development**
- Temporal capacity evolution
- Technology and regional comparison
- Line charts and stacked bars
- Interactive filters by year/region/technology

#### **Generation Analysis**
- Generation heatmaps
- Technology trend analysis
- Area charts and comparisons
- Real-time data

#### **Input Data**
- Hourly demand profiles
- Renewable availability
- Technology costs
- Detailed statistics

#### **Technology Mix**
- Technology distribution
- Regional comparison
- Market share charts
- Strategic analysis

#### **Detailed Tables**
- Capacity results
- Generation data
- Input information
- Download options

### Interactive Controls:
- **Year Filters**: Multi-selection 2025-2050
- **Region Filters**: Industrial/Residential
- **Technology Filters**: Gas/Wind/Solar
- **Data Export**: CSV, JSON, Excel
- **Dynamic Visualizations**: Interactive Plotly charts

## Project Structure

```
Message_IX/
├── scripts/
│   ├── messageix_final_working.py    # Core energy model implementation
│   └── run_messageix_final.py        # Model execution script
├── dashboard.py                      # Complete Streamlit dashboard
├── launch_dashboard.py               # Dashboard launcher
├── data/
│   ├── demand_patterns.csv           # Demand patterns
│   ├── renewable_profiles.csv        # Renewable profiles
│   └── technology_costs.csv          # Technology costs
├── results/                          # Optimization results
├── .vscode/                         # VS Code configuration
└── requirements.txt                 # Dependencies
```

## Technical Implementation

### Energy Framework
- **IXMP Platform**: Scenario and database management
- **GAMS Solver**: Linear programming optimization
- **Python API**: Official MESSAGE-IX interface
- **Objective**: System cost minimization

### Dashboard Technologies
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Dynamic visualizations
- **Pandas**: Data processing
- **NumPy**: Numerical computing

### Energy Model
- **Regions**: Industrial (high demand), Residential (low demand)
- **Technologies**: 
  - Natural Gas: $950/kW, 30-year lifetime
  - Wind: $1320/kW, 25-year lifetime  
  - Solar: $980/kW, 25-year lifetime
- **Optimization**: Minimum cost with demand constraints

## Model Results

### Key Metrics:
- **Total Cost**: $676.79 Million USD
- **Solver**: GAMS CPLEX (optimal solution found)
- **Runtime**: 0.375 seconds
- **Variables**: 157 columns, 165 rows

### Optimized Technology Mix:
- **Natural Gas**: 50% (base technology)
- **Wind**: 30% (sustained growth)
- **Solar**: 20% (accelerated expansion)

## Dashboard Usage

### VS Code Integration:
```bash
# Available tasks (Ctrl+Shift+P → "Tasks: Run Task")
1. "Run MESSAGE-IX Model"        # Execute optimization
2. "Launch Dashboard"            # Open dashboard
3. "Install Dependencies"        # Install packages
4. "Run Model + Dashboard"       # Complete workflow
```

### Direct Commands:
```bash
# Model only
python scripts/run_messageix_final.py

# Dashboard only  
python launch_dashboard.py

# Direct Streamlit
streamlit run dashboard.py
```

## Advanced Features

### Dynamic Filters:
- Multi-year selection
- Regional filters
- Technology selection
- Real-time updates

### Visualizations:
- Temporal line charts
- Heat maps
- Stacked bar charts
- Interactive pie charts
- Area charts

### Export Options:
- CSV results download
- Complete JSON export
- Detailed Excel files
- Input data included

## Dependencies

```
# Core Energy Framework
message-ix>=3.11.0
ixmp>=3.11.0

# Dashboard & Visualization
streamlit>=1.28.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Data Processing
pandas>=1.5.0
numpy>=1.24.0
```

## Comparison: VS Code vs Jupyter

| Feature | VS Code + Dashboard | Jupyter Notebooks |
|---------|-------------------|-------------------|
| **Interface** | Professional dashboard | Sequential cells |
| **Interactivity** | Dynamic filters | Static |
| **Visualization** | Interactive Plotly | Basic matplotlib |
| **Production** | Deployment ready | Exploration only |
| **Sharing** | Web URL | .ipynb files |
| **Updates** | Real-time | Manual |

## Use Cases

### **Energy Analysts**
- Energy policy evaluation
- Optimal technology mix analysis
- Investment planning

### **Decision Makers**
- Executive dashboard with key metrics
- Presentation visualizations
- Scenario analysis

### **Researchers**
- Complete energy modeling framework
- Exportable data for additional analysis
- Extensible platform

### **Education**
- Energy optimization demonstration
- Interactive learning tool
- Professional energy modeling example

## Future Enhancements

To extend the model:

1. **More Technologies**: Add batteries, nuclear, etc.
2. **More Regions**: Expand geographical model
3. **Scenarios**: Implement multiple scenarios
4. **Uncertainty**: Sensitivity analysis
5. **Real-time**: Live data connections

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **Energy Modeling Community**: Framework development
- **Streamlit**: Dashboard framework
- **GAMS Corporation**: Optimization solver
- **Plotly**: Interactive visualizations

## Support

- **MESSAGE-IX Documentation**: https://docs.messageix.org/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **GitHub Issues**: For reporting problems

---

**Professional MESSAGE-IX Dashboard | Real-time Energy Analysis | Advanced Optimization Platform**