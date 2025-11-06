# MESSAGE-IX Energy System Modeling Project

This repository implements a comprehensive two-region energy system model using the MESSAGE-IX framework for long-term energy planning analysis (2025-2050). The model incorporates realistic technology costs, environmental constraints, and renewable energy integration scenarios with battery storage capabilities.

## Technical Framework
- **Core Model**: MESSAGE-IX optimization framework with Python API
- **Analysis Period**: 2025-2050 with annual time steps and 2.3% demand growth
- **Regional Structure**: Industrial and Residential demand zones with differentiated characteristics
- **Technology Portfolio**: Natural gas CCGT, onshore wind, utility solar PV, lithium-ion battery storage
- **Scenarios**: Baseline transition vs accelerated battery storage integration

## Repository Organization
- `/data/` - Generated datasets including demand patterns, technology costs, and renewable profiles
- `/models/` - MESSAGE-IX model definitions and optimization configurations
- `/scripts/` - Core analysis modules for modeling, visualization, and data processing
- `/results/` - Analysis outputs including interactive dashboard and scenario comparisons
- `/docs/` - Comprehensive technical documentation and methodology references

## Development Standards
- Follow MESSAGE-IX API conventions and optimization modeling best practices
- Implement robust data validation and error handling throughout analysis pipeline
- Maintain comprehensive documentation of modeling assumptions and data sources
- Ensure reproducible results with clear parameter specifications
- Provide interactive visualizations for stakeholder communication and analysis interpretation