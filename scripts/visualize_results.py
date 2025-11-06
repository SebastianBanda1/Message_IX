"""
Visualization Module for Two-Region Energy System Model

This module creates comprehensive visualizations for the energy system analysis
including demand patterns, renewable profiles, and system optimization results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class EnergySystemVisualizer:
    """
    Comprehensive visualization toolkit for energy system analysis
    """
    
    def __init__(self):
        """Initialize the visualizer"""
        self.demand_data = None
        self.renewable_data = None
        self.tech_data = None
        
    def load_data(self):
        """Load data from CSV files"""
        try:
            self.demand_data = pd.read_csv('data/demand_patterns.csv')
            self.renewable_data = pd.read_csv('data/renewable_profiles.csv')
            self.tech_data = pd.read_csv('data/technology_costs.csv')
            print("Data loaded successfully!")
            return True
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            print("Please run 'python scripts/run_model.py' first to generate data files.")
            return False
            
    def create_demand_visualization(self):
        """Create comprehensive demand pattern visualizations"""
        if self.demand_data is None:
            if not self.load_data():
                return
                
        # Create subplot figure
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Energy Demand Analysis - Two Region System', fontsize=16, fontweight='bold')
        
        # 1. Hourly demand patterns
        axes[0, 0].plot(self.demand_data['Hour'], self.demand_data['Industrial_Demand_MW'], 
                       marker='o', linewidth=2, label='Industrial', color='#2E86AB')
        axes[0, 0].plot(self.demand_data['Hour'], self.demand_data['Residential_Demand_MW'], 
                       marker='s', linewidth=2, label='Residential', color='#A23B72')
        axes[0, 0].set_xlabel('Hour of Day')
        axes[0, 0].set_ylabel('Demand (MW)')
        axes[0, 0].set_title('Hourly Demand Patterns')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_xticks(range(0, 24, 2))
        
        # 2. Demand distribution
        industrial_data = self.demand_data['Industrial_Demand_MW']
        residential_data = self.demand_data['Residential_Demand_MW']
        
        axes[0, 1].hist(industrial_data, alpha=0.7, bins=15, label='Industrial', 
                       color='#2E86AB', density=True)
        axes[0, 1].hist(residential_data, alpha=0.7, bins=15, label='Residential', 
                       color='#A23B72', density=True)
        axes[0, 1].set_xlabel('Demand (MW)')
        axes[0, 1].set_ylabel('Density')
        axes[0, 1].set_title('Demand Distribution')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Stacked area chart
        axes[1, 0].fill_between(self.demand_data['Hour'], 0, self.demand_data['Industrial_Demand_MW'],
                               alpha=0.7, color='#2E86AB', label='Industrial')
        axes[1, 0].fill_between(self.demand_data['Hour'], self.demand_data['Industrial_Demand_MW'],
                               self.demand_data['Industrial_Demand_MW'] + self.demand_data['Residential_Demand_MW'],
                               alpha=0.7, color='#A23B72', label='Residential')
        axes[1, 0].set_xlabel('Hour of Day')
        axes[1, 0].set_ylabel('Cumulative Demand (MW)')
        axes[1, 0].set_title('Stacked Demand Profile')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_xticks(range(0, 24, 2))
        
        # 4. Peak vs Average analysis
        peak_times_ind = self.demand_data.loc[self.demand_data['Industrial_Demand_MW'] > 
                                            self.demand_data['Industrial_Demand_MW'].mean(), 'Hour']
        peak_times_res = self.demand_data.loc[self.demand_data['Residential_Demand_MW'] > 
                                            self.demand_data['Residential_Demand_MW'].mean(), 'Hour']
        
        axes[1, 1].scatter(peak_times_ind, [1]*len(peak_times_ind), s=100, alpha=0.7, 
                          color='#2E86AB', label='Industrial Peak Hours')
        axes[1, 1].scatter(peak_times_res, [0]*len(peak_times_res), s=100, alpha=0.7, 
                          color='#A23B72', label='Residential Peak Hours')
        axes[1, 1].set_xlabel('Hour of Day')
        axes[1, 1].set_ylabel('Region')
        axes[1, 1].set_title('Peak Demand Hours')
        axes[1, 1].set_yticks([0, 1])
        axes[1, 1].set_yticklabels(['Residential', 'Industrial'])
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_xticks(range(0, 24, 2))
        
        plt.tight_layout()
        plt.savefig('results/demand_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_renewable_visualization(self):
        """Create renewable energy availability visualizations"""
        if self.renewable_data is None:
            if not self.load_data():
                return
                
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Renewable Energy Resource Analysis', fontsize=16, fontweight='bold')
        
        # 1. Renewable availability profiles
        axes[0, 0].plot(self.renewable_data['Hour'], self.renewable_data['Wind_Availability'], 
                       marker='o', linewidth=2, label='Wind', color='#00A8CC')
        axes[0, 0].plot(self.renewable_data['Hour'], self.renewable_data['Solar_Availability'], 
                       marker='s', linewidth=2, label='Solar', color='#FFB400')
        axes[0, 0].set_xlabel('Hour of Day')
        axes[0, 0].set_ylabel('Availability Factor')
        axes[0, 0].set_title('Renewable Resource Availability')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_xticks(range(0, 24, 2))
        axes[0, 0].set_ylim(0, 1)
        
        # 2. Combined renewable profile
        combined_renewable = (self.renewable_data['Wind_Availability'] + 
                            self.renewable_data['Solar_Availability']) / 2
        
        axes[0, 1].fill_between(self.renewable_data['Hour'], 0, self.renewable_data['Wind_Availability'],
                               alpha=0.7, color='#00A8CC', label='Wind')
        axes[0, 1].fill_between(self.renewable_data['Hour'], 0, self.renewable_data['Solar_Availability'],
                               alpha=0.7, color='#FFB400', label='Solar')
        axes[0, 1].plot(self.renewable_data['Hour'], combined_renewable, 
                       linewidth=3, color='#2D5016', label='Combined Average')
        axes[0, 1].set_xlabel('Hour of Day')
        axes[0, 1].set_ylabel('Availability Factor')
        axes[0, 1].set_title('Renewable Energy Complementarity')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_xticks(range(0, 24, 2))
        
        # 3. Capacity factor analysis
        wind_cf = self.renewable_data['Wind_Availability'].mean()
        solar_cf = self.renewable_data['Solar_Availability'].mean()
        
        capacity_factors = [wind_cf, solar_cf]
        technologies = ['Wind', 'Solar']
        colors = ['#00A8CC', '#FFB400']
        
        bars = axes[1, 0].bar(technologies, capacity_factors, color=colors, alpha=0.8)
        axes[1, 0].set_ylabel('Average Capacity Factor')
        axes[1, 0].set_title('Renewable Technology Performance')
        axes[1, 0].set_ylim(0, 0.6)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, cf in zip(bars, capacity_factors):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{cf:.1%}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Renewable vs demand correlation
        total_demand = (self.demand_data['Industrial_Demand_MW'] + 
                       self.demand_data['Residential_Demand_MW'])
        
        axes[1, 1].scatter(combined_renewable, total_demand, alpha=0.7, s=60, color='#8B5A3C')
        
        # Add trend line
        z = np.polyfit(combined_renewable, total_demand, 1)
        p = np.poly1d(z)
        axes[1, 1].plot(combined_renewable, p(combined_renewable), "r--", alpha=0.8, linewidth=2)
        
        axes[1, 1].set_xlabel('Combined Renewable Availability')
        axes[1, 1].set_ylabel('Total Demand (MW)')
        axes[1, 1].set_title('Renewable Supply vs Demand Correlation')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Calculate correlation
        correlation = np.corrcoef(combined_renewable, total_demand)[0, 1]
        axes[1, 1].text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                       transform=axes[1, 1].transAxes, bbox=dict(boxstyle="round", facecolor='wheat'))
        
        plt.tight_layout()
        plt.savefig('results/renewable_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_technology_comparison(self):
        """Create technology cost and performance comparison"""
        if self.tech_data is None:
            if not self.load_data():
                return
                
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Technology Comparison Analysis', fontsize=16, fontweight='bold')
        
        # 1. Capital costs comparison
        axes[0, 0].bar(self.tech_data['Technology'], self.tech_data['Capital_Cost_USD_MW']/1000000,
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        axes[0, 0].set_ylabel('Capital Cost (Million $/MW)')
        axes[0, 0].set_title('Capital Cost Comparison')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # 2. Operating costs
        axes[0, 1].bar(self.tech_data['Technology'], self.tech_data['Operating_Cost_USD_MWh'],
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        axes[0, 1].set_ylabel('Operating Cost ($/MWh)')
        axes[0, 1].set_title('Operating Cost Comparison')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # 3. Levelized cost estimation (simplified)
        # LCOE = (Capital Cost * CRF + O&M) / (Capacity Factor * 8760)
        interest_rate = 0.07
        crfs = []
        lcoes = []
        
        for idx, row in self.tech_data.iterrows():
            n = row['Lifetime_Years']
            crf = interest_rate * (1 + interest_rate)**n / ((1 + interest_rate)**n - 1)
            crfs.append(crf)
            
            # Use technology-specific capacity factors
            if 'wind' in row['Technology']:
                cf = 0.35
            elif 'solar' in row['Technology']:
                cf = 0.22
            else:  # natural gas
                cf = 0.85
                
            annual_capital = row['Capital_Cost_USD_MW'] * crf
            annual_om = row['Operating_Cost_USD_MWh'] * cf * 8760
            annual_fuel = row['Fuel_Cost_USD_MWh'] * cf * 8760
            
            lcoe = (annual_capital + annual_om + annual_fuel) / (cf * 8760)
            lcoes.append(lcoe)
        
        axes[1, 0].bar(self.tech_data['Technology'], lcoes,
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        axes[1, 0].set_ylabel('LCOE ($/MWh)')
        axes[1, 0].set_title('Levelized Cost of Energy')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Technology characteristics radar chart (using matplotlib)
        # Normalize values for radar chart
        categories = ['Capital Cost\n(Normalized)', 'Operating Cost\n(Normalized)', 
                     'Efficiency', 'Lifetime\n(Normalized)']
        
        # Normalize data (0-1 scale, higher is better for radar)
        cap_cost_norm = 1 - (self.tech_data['Capital_Cost_USD_MW'] - self.tech_data['Capital_Cost_USD_MW'].min()) / \
                           (self.tech_data['Capital_Cost_USD_MW'].max() - self.tech_data['Capital_Cost_USD_MW'].min())
        op_cost_norm = 1 - (self.tech_data['Operating_Cost_USD_MWh'] - self.tech_data['Operating_Cost_USD_MWh'].min()) / \
                          (self.tech_data['Operating_Cost_USD_MWh'].max() - self.tech_data['Operating_Cost_USD_MWh'].min())
        efficiency_norm = self.tech_data['Efficiency'] / self.tech_data['Efficiency'].max()
        lifetime_norm = (self.tech_data['Lifetime_Years'] - self.tech_data['Lifetime_Years'].min()) / \
                       (self.tech_data['Lifetime_Years'].max() - self.tech_data['Lifetime_Years'].min())
        
        # Create simple comparison chart instead of radar
        x_pos = np.arange(len(self.tech_data))
        width = 0.2
        
        axes[1, 1].bar(x_pos - width, cap_cost_norm, width, label='Capital Cost (inv)', alpha=0.8)
        axes[1, 1].bar(x_pos, op_cost_norm, width, label='Operating Cost (inv)', alpha=0.8)
        axes[1, 1].bar(x_pos + width, efficiency_norm, width, label='Efficiency', alpha=0.8)
        
        axes[1, 1].set_xlabel('Technologies')
        axes[1, 1].set_ylabel('Normalized Performance (0-1)')
        axes[1, 1].set_title('Technology Performance Comparison')
        axes[1, 1].set_xticks(x_pos)
        axes[1, 1].set_xticklabels([tech.replace('_', ' ').title() for tech in self.tech_data['Technology']])
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('results/technology_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_interactive_dashboard(self):
        """Create an interactive Plotly dashboard"""
        if not self.load_data():
            return
            
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Demand Patterns', 'Renewable Profiles', 
                          'Technology Costs', 'System Summary'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "indicator"}]]
        )
        
        # 1. Demand patterns
        fig.add_trace(
            go.Scatter(x=self.demand_data['Hour'], y=self.demand_data['Industrial_Demand_MW'],
                      mode='lines+markers', name='Industrial Demand', line=dict(color='#2E86AB')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=self.demand_data['Hour'], y=self.demand_data['Residential_Demand_MW'],
                      mode='lines+markers', name='Residential Demand', line=dict(color='#A23B72')),
            row=1, col=1
        )
        
        # 2. Renewable profiles
        fig.add_trace(
            go.Scatter(x=self.renewable_data['Hour'], y=self.renewable_data['Wind_Availability'],
                      mode='lines+markers', name='Wind Availability', line=dict(color='#00A8CC')),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=self.renewable_data['Hour'], y=self.renewable_data['Solar_Availability'],
                      mode='lines+markers', name='Solar Availability', line=dict(color='#FFB400')),
            row=1, col=2
        )
        
        # 3. Technology costs
        fig.add_trace(
            go.Bar(x=self.tech_data['Technology'], y=self.tech_data['Capital_Cost_USD_MW']/1000000,
                  name='Capital Cost (M$/MW)', marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']),
            row=2, col=1
        )
        
        # 4. Summary indicators
        total_demand = (self.demand_data['Industrial_Demand_MW'].sum() + 
                       self.demand_data['Residential_Demand_MW'].sum())
        
        fig.add_trace(
            go.Indicator(
                mode = "gauge+number+delta",
                value = total_demand,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Total Daily Demand (MWh)"},
                delta = {'reference': 4000},
                gauge = {
                    'axis': {'range': [None, 5000]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 2500], 'color': "lightgray"},
                        {'range': [2500, 4000], 'color': "gray"}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 4500}}),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="MESSAGE-IX Two-Region Energy System Dashboard",
            title_x=0.5,
            showlegend=True,
            height=800
        )
        
        fig.write_html('results/interactive_dashboard.html')
        print("Interactive dashboard saved as 'results/interactive_dashboard.html'")
        
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("Generating comprehensive energy system visualizations...")
        
        if not self.load_data():
            return
            
        self.create_demand_visualization()
        self.create_renewable_visualization() 
        self.create_technology_comparison()
        self.create_interactive_dashboard()
        
        print("\n=== VISUALIZATION SUMMARY ===")
        print("Generated visualizations:")
        print("- results/demand_analysis.png")
        print("- results/renewable_analysis.png") 
        print("- results/technology_comparison.png")
        print("- results/interactive_dashboard.html")
        print("\nAll visualizations completed successfully!")

if __name__ == "__main__":
    visualizer = EnergySystemVisualizer()
    visualizer.generate_all_visualizations()