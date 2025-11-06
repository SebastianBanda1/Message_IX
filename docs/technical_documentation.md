# Two-Region Energy System Model - Technical Documentation

## Overview

This MESSAGE-IX based model simulates a two-region energy system with realistic demand patterns and renewable energy integration. The model is designed for educational and research purposes to demonstrate energy system optimization principles.

## Model Structure

### Regions

1. **Industrial Region**
   - Characteristics: Steady, predictable demand
   - Base load: ~100 MW
   - Variation: ±5% around baseline
   - Load pattern: Relatively flat with minor fluctuations

2. **Residential Region**
   - Characteristics: Variable demand with daily peaks
   - Base load: ~80 MW
   - Peak periods: Morning (7-9 AM) and evening (6-9 PM)
   - Peak multipliers: 1.4x (morning), 1.6x (evening)
   - Night-time reduction: 0.6x baseline

### Energy Technologies

#### Natural Gas Plant
- **Role**: Baseload and peaking power
- **Efficiency**: 45%
- **Capacity Factor**: 85%
- **Capital Cost**: $800,000/MW
- **Operating Cost**: $45/MWh
- **Fuel Cost**: $35/MWh

#### Wind Turbine
- **Role**: Variable renewable generation
- **Capacity Factor**: 35% (average)
- **Profile**: Higher availability at night
- **Capital Cost**: $1,500,000/MW
- **Operating Cost**: $25/MWh
- **Fuel Cost**: $0/MWh

#### Solar PV
- **Role**: Daytime renewable generation
- **Capacity Factor**: 22% (average)
- **Profile**: Parabolic pattern peaking at noon
- **Capital Cost**: $1,200,000/MW
- **Operating Cost**: $15/MWh
- **Fuel Cost**: $0/MWh

## Demand Patterns

### Industrial Demand Model

```python
# Industrial demand: constant with small variations
industrial_base = 100  # MW
variation = random.normal(1.0, 0.05)  # ±5% variation
demand = industrial_base * variation
```

### Residential Demand Model

```python
# Residential demand: time-dependent multipliers
if 6 <= hour <= 9:      # Morning peak
    multiplier = 1.4
elif 17 <= hour <= 21:  # Evening peak  
    multiplier = 1.6
elif 22 <= hour <= 5:   # Night time
    multiplier = 0.6
else:                   # Day time
    multiplier = 1.0
    
demand = residential_base * multiplier
```

## Renewable Resource Modeling

### Wind Profile

Wind generation follows a realistic pattern with:
- Higher availability during night hours
- Lower availability during day hours
- Stochastic variations around mean values
- Capacity factors ranging from 5% to 80%

### Solar Profile

Solar generation follows solar irradiance patterns:
- Zero generation at night (6 PM - 6 AM)
- Parabolic profile during day (6 AM - 6 PM)
- Peak at solar noon (12 PM)
- Weather-induced variability

## Key Metrics and Analysis

### Load Metrics
- **Total Daily Demand**: Sum of all hourly demands
- **Peak Demand**: Maximum hourly demand
- **Load Factor**: Average demand / Peak demand
- **Peak-to-Average Ratio**: Peak demand / Average demand

### Renewable Metrics
- **Capacity Factor**: Average output / Rated capacity
- **Complementarity**: How well wind and solar complement each other
- **Resource Correlation**: Statistical correlation between resources

### Economic Metrics
- **LCOE**: Levelized Cost of Energy
- **Capital Recovery Factor**: Annualized capital costs
- **System Costs**: Total cost of meeting demand

## Mathematical Formulations

### Levelized Cost of Energy (LCOE)

```
LCOE = (Capital_Cost × CRF + O&M_Cost + Fuel_Cost × CF × 8760) / (CF × 8760)

Where:
- CRF = Capital Recovery Factor = r(1+r)^n / ((1+r)^n - 1)
- r = Discount rate (7%)
- n = Technology lifetime (years)
- CF = Capacity Factor
```

### Capital Recovery Factor

```
CRF = r × (1 + r)^n / ((1 + r)^n - 1)

Where:
- r = 0.07 (7% discount rate)
- n = Technology lifetime in years
```

### Resource Complementarity Index

```
Complementarity = 1 - correlation(wind_normalized, solar_normalized)

Where values closer to 1 indicate better complementarity
```

## Model Assumptions

1. **Perfect Foresight**: Model has complete information about future conditions
2. **Linear Costs**: All costs scale linearly with capacity
3. **No Transmission**: Regions are electrically isolated
4. **Fixed Efficiency**: Technology efficiencies remain constant
5. **No Storage**: No energy storage technologies included
6. **Deterministic Weather**: Renewable profiles are deterministic

## Data Sources and Validation

### Demand Patterns
- Industrial patterns based on typical manufacturing facilities
- Residential patterns reflect standard household consumption
- Validation against published load curves

### Renewable Profiles  
- Wind patterns based on meteorological data characteristics
- Solar profiles follow solar irradiance physics
- Capacity factors align with industry benchmarks

### Technology Costs
- Capital costs from NREL ATB (Annual Technology Baseline)
- Operating costs from industry reports
- Fuel costs from market data

## Scenario Analysis

The model supports several scenario analyses:

1. **High Renewable Scenario**: +20% renewable capacity factors
2. **High Demand Scenario**: +15% demand growth
3. **Cost Reduction Scenario**: -20% renewable technology costs
4. **Sensitivity Analysis**: Parameter variations

## Limitations and Extensions

### Current Limitations
- No energy storage modeling
- No transmission between regions  
- Simplified cost structures
- No reliability/reserve requirements
- No environmental constraints

### Potential Extensions
- Battery storage integration
- Transmission network modeling
- Stochastic renewable profiles
- Carbon pricing mechanisms
- Reliability constraints
- Multiple years/seasons

## References

1. MESSAGE-IX Documentation: https://docs.messageix.org/
2. NREL Annual Technology Baseline
3. IEA Energy Technology Roadmaps
4. Renewable energy integration studies