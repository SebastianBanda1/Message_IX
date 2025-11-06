"""
MESSAGE-IX Two-Region Energy System Model

This module implements a comprehensive energy system model with:
- Two regions: Industrial and Residential
- Multiple energy sources: Natural Gas, Wind, Solar
- Realistic demand patterns and renewable variability
"""

import pandas as pd
import numpy as np
from message_ix import Scenario, make_df
import ixmp
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class TwoRegionEnergyModel:
    """
    MESSAGE-IX based two-region energy system model
    """
    
    def __init__(self, model_name='TwoRegionModel', scenario_name='baseline'):
        """
        Initialize the two-region energy model
        
        Args:
            model_name (str): Name of the MESSAGE-IX model
            scenario_name (str): Name of the scenario
        """
        self.model_name = model_name
        self.scenario_name = scenario_name
        self.mp = None
        self.scenario = None
        
        # Model parameters
        self.regions = ['Industrial', 'Residential']
        self.commodities = ['electricity', 'natural_gas']
        self.technologies = {
            'natural_gas_plant': {
                'input': 'natural_gas',
                'output': 'electricity',
                'capacity_factor': 0.85,
                'efficiency': 0.45
            },
            'wind_turbine': {
                'input': None,
                'output': 'electricity', 
                'capacity_factor': 0.35,
                'efficiency': 1.0
            },
            'solar_pv': {
                'input': None,
                'output': 'electricity',
                'capacity_factor': 0.22,
                'efficiency': 1.0
            }
        }
        
        # Time periods (hours of the day)
        self.time_periods = list(range(24))
        self.years = [2025, 2030, 2035, 2040]
        
    def setup_platform(self):
        """Initialize MESSAGE-IX platform"""
        self.mp = ixmp.Platform(name='message_ix_tutorial', jvmargs=['-Xms800m', '-Xmx2g'])
        
    def create_scenario(self):
        """Create and initialize the scenario"""
        try:
            self.scenario = Scenario(self.mp, self.model_name, self.scenario_name, version='new')
        except:
            # If scenario exists, load it
            self.scenario = Scenario(self.mp, self.model_name, self.scenario_name)
            
    def generate_demand_patterns(self):
        """
        Generate realistic demand patterns for industrial and residential regions
        
        Returns:
            dict: Demand data by region and time period
        """
        np.random.seed(42)  # For reproducible results
        
        demand_patterns = {}
        
        # Industrial demand: relatively constant with slight variations
        industrial_base = 100  # MW baseline
        industrial_demand = []
        for hour in self.time_periods:
            # Industrial demand varies ±5% around baseline
            variation = np.random.normal(1.0, 0.05)
            demand = industrial_base * variation
            industrial_demand.append(max(demand, industrial_base * 0.8))  # Minimum 80% of base
            
        # Residential demand: peaks in morning (7-9) and evening (18-21)
        residential_base = 80  # MW baseline
        residential_demand = []
        for hour in self.time_periods:
            # Base pattern
            if 6 <= hour <= 9:  # Morning peak
                multiplier = 1.4 + np.random.normal(0, 0.1)
            elif 17 <= hour <= 21:  # Evening peak
                multiplier = 1.6 + np.random.normal(0, 0.1)
            elif 22 <= hour <= 24 or 0 <= hour <= 5:  # Night time
                multiplier = 0.6 + np.random.normal(0, 0.05)
            else:  # Day time
                multiplier = 1.0 + np.random.normal(0, 0.1)
                
            demand = residential_base * max(multiplier, 0.4)  # Minimum 40% of base
            residential_demand.append(demand)
            
        demand_patterns['Industrial'] = industrial_demand
        demand_patterns['Residential'] = residential_demand
        
        return demand_patterns
        
    def generate_renewable_profiles(self):
        """
        Generate renewable energy availability profiles
        
        Returns:
            dict: Availability factors for wind and solar by time period
        """
        np.random.seed(42)
        
        profiles = {}
        
        # Wind profile: higher at night, variable
        wind_profile = []
        for hour in self.time_periods:
            if 0 <= hour <= 6 or 20 <= hour <= 24:  # Night - higher wind
                base_factor = 0.4
            else:  # Day - lower wind
                base_factor = 0.25
                
            # Add variability
            factor = base_factor * (1 + np.random.normal(0, 0.3))
            wind_profile.append(max(min(factor, 0.8), 0.05))  # Clamp between 5% and 80%
            
        # Solar profile: follows sun pattern
        solar_profile = []
        for hour in self.time_periods:
            if 6 <= hour <= 18:  # Daylight hours
                # Parabolic pattern peaking at noon
                sun_angle = 1 - abs(hour - 12) / 6
                base_factor = 0.8 * sun_angle ** 2
                # Add some cloud variability
                factor = base_factor * (1 + np.random.normal(0, 0.2))
            else:  # Night
                factor = 0
                
            solar_profile.append(max(min(factor, 0.9), 0))
            
        profiles['wind_turbine'] = wind_profile
        profiles['solar_pv'] = solar_profile
        
        return profiles
        
    def save_data_to_files(self):
        """Save generated data to CSV files for analysis"""
        # Generate data
        demand_data = self.generate_demand_patterns()
        renewable_data = self.generate_renewable_profiles()
        
        # Save demand patterns
        demand_df = pd.DataFrame({
            'Hour': self.time_periods,
            'Industrial_Demand_MW': demand_data['Industrial'],
            'Residential_Demand_MW': demand_data['Residential']
        })
        demand_df.to_csv('data/demand_patterns.csv', index=False)
        
        # Save renewable profiles
        renewable_df = pd.DataFrame({
            'Hour': self.time_periods,
            'Wind_Availability': renewable_data['wind_turbine'],
            'Solar_Availability': renewable_data['solar_pv']
        })
        renewable_df.to_csv('data/renewable_profiles.csv', index=False)
        
        # Generate technology costs data
        tech_costs = pd.DataFrame({
            'Technology': ['natural_gas_plant', 'wind_turbine', 'solar_pv'],
            'Capital_Cost_USD_MW': [800000, 1500000, 1200000],  # $/MW
            'Operating_Cost_USD_MWh': [45, 25, 15],  # $/MWh
            'Fuel_Cost_USD_MWh': [35, 0, 0],  # $/MWh (gas cost)
            'Lifetime_Years': [25, 20, 25],
            'Efficiency': [0.45, 1.0, 1.0]
        })
        tech_costs.to_csv('data/technology_costs.csv', index=False)
        
        print("Data files generated successfully in /data/ directory")
        return demand_data, renewable_data
        
    def run_simple_analysis(self):
        """Run a simplified analysis without full MESSAGE-IX optimization"""
        print("Running Two-Region Energy System Analysis...")
        
        # Generate and save data
        demand_data, renewable_data = self.save_data_to_files()
        
        # Calculate basic metrics
        total_demand = {}
        for region in self.regions:
            total_daily_demand = sum(demand_data[region])
            peak_demand = max(demand_data[region])
            min_demand = min(demand_data[region])
            
            total_demand[region] = {
                'total_daily_mwh': total_daily_demand,
                'peak_mw': peak_demand,
                'min_mw': min_demand,
                'load_factor': total_daily_demand / (peak_demand * 24)
            }
            
        # Calculate renewable potential
        wind_capacity_factor = np.mean(renewable_data['wind_turbine'])
        solar_capacity_factor = np.mean(renewable_data['solar_pv'])
        
        results = {
            'demand_analysis': total_demand,
            'renewable_analysis': {
                'wind_capacity_factor': wind_capacity_factor,
                'solar_capacity_factor': solar_capacity_factor,
                'combined_cf': (wind_capacity_factor + solar_capacity_factor) / 2
            }
        }
        
        return results

if __name__ == "__main__":
    # Initialize and run the model
    model = TwoRegionEnergyModel()
    
    print("=== MESSAGE-IX Two-Region Energy System Model ===")
    print("Generating demand patterns and renewable profiles...")
    
    # Run simplified analysis
    results = model.run_simple_analysis()
    
    print("\n=== ANALYSIS RESULTS ===")
    print("\nDemand Analysis:")
    for region, metrics in results['demand_analysis'].items():
        print(f"\n{region} Region:")
        print(f"  Total Daily Demand: {metrics['total_daily_mwh']:.1f} MWh")
        print(f"  Peak Demand: {metrics['peak_mw']:.1f} MW")
        print(f"  Minimum Demand: {metrics['min_mw']:.1f} MW")
        print(f"  Load Factor: {metrics['load_factor']:.2%}")
        
    print(f"\nRenewable Analysis:")
    print(f"  Wind Capacity Factor: {results['renewable_analysis']['wind_capacity_factor']:.2%}")
    print(f"  Solar Capacity Factor: {results['renewable_analysis']['solar_capacity_factor']:.2%}")
    
    print(f"\nData files saved to /data/ directory for further analysis.")
    print("Run visualization script: python scripts/visualize_results.py")