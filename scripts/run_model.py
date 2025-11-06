"""
MESSAGE-IX Two-Region Energy System Model (2025-2050 Projection)

This module implements a comprehensive energy system model with:
- Two regions: Industrial and Residential with 2.3% annual demand growth
- Multiple energy sources: Natural Gas, Wind, Solar, Battery Storage
- Real-world technology costs and environmental impact tracking
- Carbon reduction scenarios through 2050
- Scenario comparison framework
"""

import pandas as pd
import numpy as np
from message_ix import Scenario, make_df
import ixmp
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TwoRegionEnergyModel:
    """
    MESSAGE-IX based two-region energy system model with 2025-2050 projections
    and environmental impact assessment
    """
    
    def __init__(self, model_name='TwoRegionModel_2050', scenario_name='baseline'):
        """
        Initialize the two-region energy model for 2025-2050 analysis
        
        Args:
            model_name (str): Name of the MESSAGE-IX model
            scenario_name (str): Name of the scenario ('baseline' or 'battery_storage')
        """
        self.model_name = model_name
        self.scenario_name = scenario_name
        self.mp = None
        self.scenario = None
        
        # Time parameters
        self.start_year = 2025
        self.end_year = 2050
        self.years = list(range(self.start_year, self.end_year + 1))
        self.demand_growth_rate = 0.023  # 2.3% annual growth
        
        # Model parameters
        self.regions = ['Industrial', 'Residential']
        self.commodities = ['electricity', 'natural_gas', 'co2_emissions']
        
        # Real-world technology data (based on NREL ATB 2024, IEA data)
        self.technologies = {
            'natural_gas_plant': {
                'input': 'natural_gas',
                'output': 'electricity',
                'capacity_factor': 0.85,
                'efficiency': 0.48,  # Modern CCGT efficiency
                'capex_2025': 950000,  # $/MW (NREL ATB 2024)
                'opex_fixed': 15000,   # $/MW/year
                'opex_variable': 35,   # $/MWh
                'fuel_cost': 38,       # $/MWh (Henry Hub + transport)
                'co2_intensity': 354,  # kg CO2/MWh (CCGT)
                'lifetime': 30,        # years
                'learning_rate': 0.0   # No cost reduction expected
            },
            'wind_turbine': {
                'input': None,
                'output': 'electricity',
                'capacity_factor': 0.42,  # Improved with modern turbines
                'efficiency': 1.0,
                'capex_2025': 1320000,    # $/MW (NREL ATB 2024)
                'opex_fixed': 25000,      # $/MW/year
                'opex_variable': 12,      # $/MWh
                'fuel_cost': 0,           # $/MWh
                'co2_intensity': 11,      # kg CO2/MWh (lifecycle emissions)
                'lifetime': 25,           # years
                'learning_rate': 0.08     # 8% cost reduction per doubling
            },
            'solar_pv': {
                'input': None,
                'output': 'electricity',
                'capacity_factor': 0.28,  # Modern utility-scale PV
                'efficiency': 1.0,
                'capex_2025': 980000,     # $/MW (NREL ATB 2024)
                'opex_fixed': 18000,      # $/MW/year
                'opex_variable': 8,       # $/MWh
                'fuel_cost': 0,           # $/MWh
                'co2_intensity': 41,      # kg CO2/MWh (lifecycle emissions)
                'lifetime': 25,           # years
                'learning_rate': 0.15     # 15% cost reduction per doubling
            },
            'lithium_battery': {
                'input': 'electricity',
                'output': 'electricity',
                'capacity_factor': 0.95,  # High availability when needed
                'efficiency': 0.90,       # Round-trip efficiency
                'capex_2025': 1580000,    # $/MW (4-hour storage, NREL ATB 2024)
                'opex_fixed': 22000,      # $/MW/year
                'opex_variable': 5,       # $/MWh
                'fuel_cost': 0,           # $/MWh (storage, not generation)
                'co2_intensity': 0,       # No direct emissions during operation
                'lifetime': 15,           # years (battery degradation)
                'learning_rate': 0.18,    # 18% cost reduction per doubling
                'storage_duration': 4     # hours of storage capacity
            }
        }
        
        # Environmental targets
        self.carbon_targets = {
            2030: 0.50,  # 50% reduction from 2025 baseline
            2040: 0.75,  # 75% reduction
            2050: 0.90   # 90% reduction (near net-zero)
        }
        
        # Time periods (24 hours) and seasonal variations
        self.time_periods = list(range(24))
        self.seasons = ['winter', 'spring', 'summer', 'fall']
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
        with 2.3% annual growth from 2025-2050
        
        Returns:
            dict: Demand data by region, year, and time period
        """
        np.random.seed(42)  # For reproducible results
        
        demand_patterns = {}
        
        # Base year (2025) demand levels
        industrial_base_2025 = 100  # MW baseline
        residential_base_2025 = 80   # MW baseline
        
        for year in self.years:
            # Calculate demand with annual growth
            growth_factor = (1 + self.demand_growth_rate) ** (year - self.start_year)
            industrial_base = industrial_base_2025 * growth_factor
            residential_base = residential_base_2025 * growth_factor
            
            year_demands = {}
            
            # Industrial demand: relatively constant with slight variations
            industrial_demand = []
            for hour in self.time_periods:
                # Industrial demand varies ±5% around baseline
                variation = np.random.normal(1.0, 0.05)
                demand = industrial_base * variation
                industrial_demand.append(max(demand, industrial_base * 0.8))
                
            # Residential demand: peaks in morning (7-9) and evening (18-21)
            residential_demand = []
            for hour in self.time_periods:
                # Base pattern with seasonal and efficiency improvements
                efficiency_improvement = 0.005 * (year - self.start_year)  # 0.5% annual efficiency gain
                base_adjusted = residential_base * (1 - efficiency_improvement)
                
                if 6 <= hour <= 9:  # Morning peak
                    multiplier = 1.4 + np.random.normal(0, 0.1)
                elif 17 <= hour <= 21:  # Evening peak
                    multiplier = 1.6 + np.random.normal(0, 0.1)
                elif 22 <= hour <= 24 or 0 <= hour <= 5:  # Night time
                    multiplier = 0.6 + np.random.normal(0, 0.05)
                else:  # Day time
                    multiplier = 1.0 + np.random.normal(0, 0.1)
                    
                demand = base_adjusted * max(multiplier, 0.4)
                residential_demand.append(demand)
                
            year_demands['Industrial'] = industrial_demand
            year_demands['Residential'] = residential_demand
            
            demand_patterns[year] = year_demands
            
        return demand_patterns
    
    def calculate_technology_costs(self, year):
        """
        Calculate technology costs for a given year with learning curves
        
        Args:
            year (int): Year for cost calculation
            
        Returns:
            dict: Updated technology costs
        """
        costs = {}
        years_from_base = year - self.start_year
        
        for tech, params in self.technologies.items():
            # Apply learning curve cost reductions
            cost_reduction_factor = (1 - params['learning_rate']) ** years_from_base
            
            costs[tech] = {
                'capex': params['capex_2025'] * cost_reduction_factor,
                'opex_fixed': params['opex_fixed'],
                'opex_variable': params['opex_variable'],
                'fuel_cost': params['fuel_cost'],
                'co2_intensity': params['co2_intensity']
            }
            
        return costs
    
    def calculate_emissions(self, generation_mix, year):
        """
        Calculate CO2 emissions based on generation mix
        
        Args:
            generation_mix (dict): Generation by technology in MWh
            year (int): Year for calculation
            
        Returns:
            dict: Emissions data
        """
        total_emissions = 0
        total_generation = sum(generation_mix.values())
        
        emissions_by_tech = {}
        for tech, generation in generation_mix.items():
            tech_emissions = generation * self.technologies[tech]['co2_intensity'] / 1000  # Convert to tons CO2
            emissions_by_tech[tech] = tech_emissions
            total_emissions += tech_emissions
            
        carbon_intensity = total_emissions / total_generation if total_generation > 0 else 0
        
        return {
            'total_emissions_tons': total_emissions,
            'carbon_intensity_kg_mwh': carbon_intensity * 1000,
            'emissions_by_tech': emissions_by_tech,
            'renewable_share': self._calculate_renewable_share(generation_mix)
        }
    
    def _calculate_renewable_share(self, generation_mix):
        """Calculate renewable energy share"""
        renewable_techs = ['wind_turbine', 'solar_pv']
        renewable_gen = sum(generation_mix.get(tech, 0) for tech in renewable_techs)
        total_gen = sum(generation_mix.values())
        return renewable_gen / total_gen if total_gen > 0 else 0
        
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
        """Save generated multi-year data to CSV files for analysis"""
        # Generate data
        demand_data = self.generate_demand_patterns()
        renewable_data = self.generate_renewable_profiles()
        
        # Create data directory if it doesn't exist
        Path('data').mkdir(exist_ok=True)
        
        # Save multi-year demand patterns
        demand_rows = []
        for year in self.years:
            if year in demand_data:
                for hour in self.time_periods:
                    demand_rows.append({
                        'Year': year,
                        'Hour': hour,
                        'Industrial_Demand_MW': demand_data[year]['Industrial'][hour],
                        'Residential_Demand_MW': demand_data[year]['Residential'][hour],
                        'Total_Demand_MW': demand_data[year]['Industrial'][hour] + demand_data[year]['Residential'][hour]
                    })
        
        demand_df = pd.DataFrame(demand_rows)
        demand_df.to_csv(f'data/demand_patterns_{self.scenario_name}_2025_2050.csv', index=False)
        
        # Save renewable profiles 
        renewable_df = pd.DataFrame({
            'Hour': self.time_periods,
            'Wind_Availability': renewable_data['wind_turbine'],
            'Solar_Availability': renewable_data['solar_pv']
        })
        renewable_df.to_csv('data/renewable_profiles.csv', index=False)
        
        # Save technology costs with learning curves
        tech_costs_rows = []
        for year in [2025, 2030, 2040, 2050]:
            costs = self.calculate_technology_costs(year)
            for tech_name, cost_data in costs.items():
                tech_costs_rows.append({
                    'Year': year,
                    'Technology': tech_name,
                    'Scenario': self.scenario_name,
                    'CAPEX_USD_per_MW': cost_data['capex'],
                    'OPEX_Fixed_USD_per_MW_year': cost_data['opex_fixed'],
                    'OPEX_Variable_USD_per_MWh': cost_data['opex_variable'],
                    'Fuel_Cost_USD_per_MWh': cost_data['fuel_cost'],
                    'CO2_Intensity_kg_per_MWh': cost_data['co2_intensity'],
                    'Capacity_Factor': self.technologies[tech_name]['capacity_factor'],
                    'Efficiency': self.technologies[tech_name]['efficiency'],
                    'Lifetime_Years': self.technologies[tech_name]['lifetime']
                })
        
        tech_df = pd.DataFrame(tech_costs_rows)
        tech_df.to_csv(f'data/technology_costs_{self.scenario_name}.csv', index=False)
        
        print(f"Multi-year data files generated for {self.scenario_name} scenario")
        return demand_data, renewable_data
        
    def run_scenario_analysis(self):
        """
        Run comprehensive 2025-2050 scenario analysis with environmental goals
        """
        print(f"Running {self.scenario_name.upper()} Scenario Analysis (2025-2050)...")
        
        # Generate multi-year data
        demand_data, renewable_data = self.save_data_to_files()
        
        scenario_results = {
            'scenario_name': self.scenario_name,
            'years': self.years,
            'annual_results': {},
            'summary_metrics': {},
            'environmental_progress': {}
        }
        
        # Analyze each year
        for year in self.years:
            year_results = self._analyze_year(year, demand_data, renewable_data)
            scenario_results['annual_results'][year] = year_results
            
        # Calculate scenario summary
        scenario_results['summary_metrics'] = self._calculate_scenario_summary(scenario_results['annual_results'])
        scenario_results['environmental_progress'] = self._track_environmental_progress(scenario_results['annual_results'])
        
        return scenario_results
    
    def _analyze_year(self, year, demand_data, renewable_data):
        """Analyze a specific year"""
        if year not in demand_data:
            return {}
            
        year_demand = demand_data[year]
        
        # Calculate demand metrics
        total_demand = {}
        for region in self.regions:
            total_daily_demand = sum(year_demand[region])
            peak_demand = max(year_demand[region])
            min_demand = min(year_demand[region])
            
            total_demand[region] = {
                'total_daily_mwh': total_daily_demand,
                'peak_mw': peak_demand,
                'min_mw': min_demand,
                'load_factor': total_daily_demand / (peak_demand * 24)
            }
        
        # Simulate optimal generation mix (simplified optimization)
        optimal_mix = self._optimize_generation_mix(year, total_demand)
        
        # Calculate costs and emissions
        costs = self.calculate_technology_costs(year)
        emissions = self.calculate_emissions(optimal_mix, year)
        
        return {
            'demand_analysis': total_demand,
            'generation_mix': optimal_mix,
            'costs': costs,
            'emissions': emissions,
            'renewable_share': emissions['renewable_share']
        }
    
    def _optimize_generation_mix(self, year, total_demand):
        """
        Simplified generation mix optimization considering costs and carbon targets
        """
        # Total system demand (sum of both regions)
        system_demand = sum(region_data['total_daily_mwh'] for region_data in total_demand.values())
        
        # Get technology costs for this year
        costs = self.calculate_technology_costs(year)
        
        # Determine renewable target based on carbon goals
        renewable_target = self._get_renewable_target(year)
        
        # Simple dispatch logic (can be made more sophisticated)
        if self.scenario_name == 'battery_storage':
            # Higher renewable penetration with battery storage
            generation_mix = {
                'wind_turbine': system_demand * 0.4 * renewable_target,
                'solar_pv': system_demand * 0.3 * renewable_target,
                'lithium_battery': system_demand * 0.1,  # Storage dispatch
                'natural_gas_plant': system_demand * (1 - renewable_target * 0.7)
            }
        else:
            # Baseline scenario without storage
            generation_mix = {
                'wind_turbine': system_demand * 0.3 * renewable_target,
                'solar_pv': system_demand * 0.2 * renewable_target,
                'natural_gas_plant': system_demand * (1 - renewable_target * 0.5)
            }
            
        return generation_mix
    
    def _get_renewable_target(self, year):
        """Get renewable energy target for a given year"""
        if year <= 2030:
            return 0.40  # 40% renewable by 2030
        elif year <= 2040:
            return 0.70  # 70% renewable by 2040
        else:
            return 0.85  # 85% renewable by 2050
    
    def _calculate_scenario_summary(self, annual_results):
        """Calculate summary metrics across all years"""
        total_emissions = sum(annual_results[year]['emissions']['total_emissions_tons'] 
                             for year in annual_results if 'emissions' in annual_results[year])
        
        avg_renewable_share = np.mean([annual_results[year]['renewable_share'] 
                                      for year in annual_results if 'renewable_share' in annual_results[year]])
        
        return {
            'total_cumulative_emissions': total_emissions,
            'average_renewable_share': avg_renewable_share,
            'peak_system_demand_2050': max([sum(annual_results[year]['demand_analysis'][region]['peak_mw'] 
                                               for region in annual_results[year]['demand_analysis']) 
                                           for year in annual_results if 'demand_analysis' in annual_results[year]]),
            'demand_growth_factor': (1 + self.demand_growth_rate) ** (self.end_year - self.start_year)
        }
    
    def _track_environmental_progress(self, annual_results):
        """Track progress toward environmental goals"""
        baseline_emissions = annual_results.get(2025, {}).get('emissions', {}).get('total_emissions_tons', 1000)
        
        progress = {}
        for year in [2030, 2040, 2050]:
            if year in annual_results:
                current_emissions = annual_results[year]['emissions']['total_emissions_tons']
                reduction_achieved = 1 - (current_emissions / baseline_emissions)
                target_reduction = self.carbon_targets.get(year, 0)
                
                progress[year] = {
                    'target_reduction': target_reduction,
                    'achieved_reduction': reduction_achieved,
                    'on_track': reduction_achieved >= target_reduction * 0.9  # Within 90% of target
                }
                
        return progress

def run_scenario_comparison():
    """Run both baseline and battery storage scenarios"""
    
    print("=== MESSAGE-IX Two-Region Energy System Model (2025-2050) ===")
    print("Running comprehensive scenario analysis with environmental goals...\n")
    
    scenarios_results = {}
    
    # Run baseline scenario
    print("🔋 Running BASELINE scenario...")
    baseline_model = TwoRegionEnergyModel(scenario_name='baseline')
    scenarios_results['baseline'] = baseline_model.run_scenario_analysis()
    
    print("\n🔋 Running BATTERY STORAGE scenario...")
    battery_model = TwoRegionEnergyModel(scenario_name='battery_storage')
    scenarios_results['battery_storage'] = battery_model.run_scenario_analysis()
    
    # Save comprehensive results
    results_path = Path('results/scenario_comparison_2050.json')
    results_path.parent.mkdir(exist_ok=True)
    
    with open(results_path, 'w') as f:
        json.dump(scenarios_results, f, indent=2, default=str)
    
    # Display summary
    print("\n" + "="*60)
    print("🎯 SCENARIO COMPARISON SUMMARY (2025-2050)")
    print("="*60)
    
    for scenario_name, results in scenarios_results.items():
        print(f"\n📊 {scenario_name.upper()} SCENARIO:")
        summary = results['summary_metrics']
        env_progress = results['environmental_progress']
        
        print(f"  Total Cumulative Emissions: {summary['total_cumulative_emissions']:,.0f} tons CO2")
        print(f"  Average Renewable Share: {summary['average_renewable_share']:.1%}")
        print(f"  Peak System Demand 2050: {summary['peak_system_demand_2050']:,.0f} MW")
        print(f"  Total Demand Growth: {summary['demand_growth_factor']:.1%}")
        
        print(f"\n  🎯 Environmental Targets Progress:")
        for year, progress in env_progress.items():
            status = "✅ ON TRACK" if progress['on_track'] else "❌ BEHIND"
            print(f"    {year}: {progress['achieved_reduction']:.1%} achieved (target: {progress['target_reduction']:.1%}) {status}")
    
    print(f"\n📁 Detailed results saved to: {results_path}")
    print("📈 Run visualization script to see interactive dashboard!")
    
    return scenarios_results

if __name__ == "__main__":
    run_scenario_comparison()