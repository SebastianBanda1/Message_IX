"""
Data Processing and Analysis Module for MESSAGE-IX Energy System

This module provides utilities for processing energy system data,
calculating key metrics, and preparing data for optimization.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class EnergyDataProcessor:
    """
    Process and analyze energy system data for MESSAGE-IX modeling
    """
    
    def __init__(self):
        """Initialize the data processor"""
        self.demand_data = None
        self.renewable_data = None
        self.tech_data = None
        
    def load_all_data(self):
        """Load all data files"""
        try:
            self.demand_data = pd.read_csv('data/demand_patterns.csv')
            self.renewable_data = pd.read_csv('data/renewable_profiles.csv')
            self.tech_data = pd.read_csv('data/technology_costs.csv')
            return True
        except FileNotFoundError:
            print("Data files not found. Run 'python scripts/run_model.py' first.")
            return False
            
    def calculate_system_metrics(self):
        """Calculate comprehensive system performance metrics"""
        if not self.load_all_data():
            return None
            
        metrics = {}
        
        # Demand metrics
        total_industrial = self.demand_data['Industrial_Demand_MW'].sum()
        total_residential = self.demand_data['Residential_Demand_MW'].sum()
        total_demand = total_industrial + total_residential
        
        peak_industrial = self.demand_data['Industrial_Demand_MW'].max()
        peak_residential = self.demand_data['Residential_Demand_MW'].max()
        system_peak = (self.demand_data['Industrial_Demand_MW'] + 
                      self.demand_data['Residential_Demand_MW']).max()
        
        metrics['demand'] = {
            'total_daily_demand_mwh': total_demand,
            'industrial_share': total_industrial / total_demand,
            'residential_share': total_residential / total_demand,
            'system_peak_mw': system_peak,
            'system_load_factor': total_demand / (system_peak * 24),
            'peak_to_average_ratio': system_peak / (total_demand / 24)
        }
        
        # Renewable metrics
        wind_cf = self.renewable_data['Wind_Availability'].mean()
        solar_cf = self.renewable_data['Solar_Availability'].mean()
        
        # Calculate complementarity (how well wind and solar complement each other)
        wind_norm = self.renewable_data['Wind_Availability'] / wind_cf
        solar_norm = self.renewable_data['Solar_Availability'] / solar_cf
        complementarity = 1 - np.corrcoef(wind_norm, solar_norm)[0, 1]
        
        metrics['renewables'] = {
            'wind_capacity_factor': wind_cf,
            'solar_capacity_factor': solar_cf,
            'combined_capacity_factor': (wind_cf + solar_cf) / 2,
            'resource_complementarity': complementarity,
            'peak_wind_hour': self.renewable_data['Wind_Availability'].idxmax(),
            'peak_solar_hour': self.renewable_data['Solar_Availability'].idxmax()
        }
        
        # Technology economics
        tech_metrics = {}
        for idx, row in self.tech_data.iterrows():
            tech_name = row['Technology']
            
            # Simple LCOE calculation
            if 'wind' in tech_name:
                cf = wind_cf
            elif 'solar' in tech_name:
                cf = solar_cf
            else:
                cf = 0.85  # Natural gas plant
                
            # Capital recovery factor
            r = 0.07  # 7% discount rate
            n = row['Lifetime_Years']
            crf = r * (1 + r)**n / ((1 + r)**n - 1)
            
            annual_capital_cost = row['Capital_Cost_USD_MW'] * crf
            annual_energy = cf * 8760  # MWh/year
            annual_om_cost = row['Operating_Cost_USD_MWh'] * annual_energy
            annual_fuel_cost = row['Fuel_Cost_USD_MWh'] * annual_energy
            
            if annual_energy > 0:
                lcoe = (annual_capital_cost + annual_om_cost + annual_fuel_cost) / annual_energy
            else:
                lcoe = float('inf')
                
            tech_metrics[tech_name] = {
                'lcoe_usd_mwh': lcoe,
                'capacity_factor': cf,
                'annual_output_mwh_per_mw': annual_energy
            }
            
        metrics['technologies'] = tech_metrics
        
        return metrics
        
    def generate_scenario_analysis(self):
        """Generate scenarios for sensitivity analysis"""
        if not self.load_all_data():
            return None
            
        scenarios = {}
        
        # Base case
        base_metrics = self.calculate_system_metrics()
        scenarios['base_case'] = base_metrics
        
        # High renewable scenario (20% higher capacity factors)
        wind_high = self.renewable_data['Wind_Availability'] * 1.2
        wind_high = wind_high.clip(upper=0.9)  # Cap at 90%
        
        solar_high = self.renewable_data['Solar_Availability'] * 1.2
        solar_high = solar_high.clip(upper=0.9)
        
        scenarios['high_renewable'] = {
            'description': 'Improved renewable resources (+20%)',
            'wind_cf': wind_high.mean(),
            'solar_cf': solar_high.mean(),
            'improvement_factor': 1.2
        }
        
        # High demand scenario (15% higher demand)
        high_demand_factor = 1.15
        scenarios['high_demand'] = {
            'description': 'Increased energy demand (+15%)',
            'total_demand_increase': high_demand_factor,
            'new_system_peak': base_metrics['demand']['system_peak_mw'] * high_demand_factor,
            'capacity_requirement_increase': high_demand_factor
        }
        
        # Technology cost reduction scenario
        cost_reduction = 0.8  # 20% cost reduction for renewables
        scenarios['cost_reduction'] = {
            'description': 'Renewable technology cost reduction (-20%)',
            'wind_cost_factor': cost_reduction,
            'solar_cost_factor': cost_reduction,
            'impact_on_lcoe': 'Approximately 15-20% LCOE reduction for renewables'
        }
        
        return scenarios
        
    def export_results_summary(self, filename='results/system_analysis_summary.json'):
        """Export comprehensive analysis to JSON file"""
        metrics = self.calculate_system_metrics()
        scenarios = self.generate_scenario_analysis()
        
        if metrics and scenarios:
            summary = {
                'analysis_timestamp': datetime.now().isoformat(),
                'system_metrics': metrics,
                'scenario_analysis': scenarios,
                'key_insights': {
                    'demand_characteristics': [
                        f"System peak demand: {metrics['demand']['system_peak_mw']:.1f} MW",
                        f"Load factor: {metrics['demand']['system_load_factor']:.2%}",
                        f"Industrial share: {metrics['demand']['industrial_share']:.1%}",
                        f"Residential share: {metrics['demand']['residential_share']:.1%}"
                    ],
                    'renewable_potential': [
                        f"Wind capacity factor: {metrics['renewables']['wind_capacity_factor']:.1%}",
                        f"Solar capacity factor: {metrics['renewables']['solar_capacity_factor']:.1%}",
                        f"Resource complementarity index: {metrics['renewables']['resource_complementarity']:.3f}",
                        "Higher complementarity indicates better combined performance"
                    ],
                    'technology_rankings': []
                }
            }
            
            # Rank technologies by LCOE
            tech_lcoes = [(tech, data['lcoe_usd_mwh']) 
                         for tech, data in metrics['technologies'].items()]
            tech_lcoes.sort(key=lambda x: x[1])
            
            for i, (tech, lcoe) in enumerate(tech_lcoes, 1):
                summary['key_insights']['technology_rankings'].append(
                    f"{i}. {tech.replace('_', ' ').title()}: ${lcoe:.2f}/MWh"
                )
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2)
                
            print(f"Analysis summary saved to {filename}")
            return summary
        
        return None
        
    def create_optimization_inputs(self):
        """Prepare data for MESSAGE-IX optimization"""
        if not self.load_all_data():
            return None
            
        # This would typically prepare data in MESSAGE-IX format
        # For now, we'll create a simplified structure
        
        optimization_data = {
            'regions': ['Industrial', 'Residential'],
            'commodities': ['electricity', 'natural_gas'],
            'technologies': list(self.tech_data['Technology']),
            'time_periods': list(range(24)),
            'demand_profile': {
                'Industrial': self.demand_data['Industrial_Demand_MW'].tolist(),
                'Residential': self.demand_data['Residential_Demand_MW'].tolist()
            },
            'technology_parameters': {},
            'renewable_availability': {
                'wind_turbine': self.renewable_data['Wind_Availability'].tolist(),
                'solar_pv': self.renewable_data['Solar_Availability'].tolist()
            }
        }
        
        # Add technology parameters
        for idx, row in self.tech_data.iterrows():
            tech = row['Technology']
            optimization_data['technology_parameters'][tech] = {
                'capital_cost': row['Capital_Cost_USD_MW'],
                'operating_cost': row['Operating_Cost_USD_MWh'],
                'fuel_cost': row['Fuel_Cost_USD_MWh'],
                'efficiency': row['Efficiency'],
                'lifetime': row['Lifetime_Years']
            }
            
        return optimization_data

if __name__ == "__main__":
    print("=== Energy System Data Analysis ===")
    
    processor = EnergyDataProcessor()
    
    # Generate comprehensive analysis
    summary = processor.export_results_summary()
    
    if summary:
        print("\n=== KEY SYSTEM METRICS ===")
        metrics = summary['system_metrics']
        
        print(f"\nDemand Analysis:")
        print(f"  Total Daily Demand: {metrics['demand']['total_daily_demand_mwh']:.1f} MWh")
        print(f"  System Peak: {metrics['demand']['system_peak_mw']:.1f} MW")
        print(f"  Load Factor: {metrics['demand']['system_load_factor']:.2%}")
        print(f"  Industrial Share: {metrics['demand']['industrial_share']:.1%}")
        
        print(f"\nRenewable Resources:")
        print(f"  Wind Capacity Factor: {metrics['renewables']['wind_capacity_factor']:.1%}")
        print(f"  Solar Capacity Factor: {metrics['renewables']['solar_capacity_factor']:.1%}")
        print(f"  Complementarity Index: {metrics['renewables']['resource_complementarity']:.3f}")
        
        print(f"\nTechnology Economics (LCOE):")
        for tech, data in metrics['technologies'].items():
            print(f"  {tech.replace('_', ' ').title()}: ${data['lcoe_usd_mwh']:.2f}/MWh")
        
        print(f"\nDetailed analysis saved to: results/system_analysis_summary.json")
    else:
        print("Error: Could not generate analysis. Please run model first.")