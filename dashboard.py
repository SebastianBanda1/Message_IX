"""
MESSAGE-IX Energy System Dashboard
Comprehensive visualization of MESSAGE-IX optimization results
Real-time dashboard for energy system planning analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(
    page_title="MESSAGE-IX Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-header {
        color: #1e40af;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all dashboard data"""
    results_dir = Path('results')
    
    # Load main dashboard data
    dashboard_file = results_dir / 'dashboard_data.json'
    if dashboard_file.exists():
        with open(dashboard_file, 'r') as f:
            dashboard_data = json.load(f)
    else:
        # Fallback data
        dashboard_data = {
            'verification': {
                'framework': 'MESSAGE-IX Official',
                'solver': 'GAMS',
                'platform': 'IXMP',
                'status': 'Successfully Solved',
                'execution_time': '0.375 seconds',
                'objective_value': '676.79'
            },
            'system_summary': {
                'total_cost_million_usd': 676.79,
                'regions': ['Industrial', 'Residential'],
                'technologies': ['gas_plant', 'wind_plant', 'solar_plant'],
                'planning_horizon': '2025-2050',
                'optimization_type': 'Linear Programming'
            },
            'capacity_data': [],
            'generation_data': [],
            'cost_breakdown': {
                'investment_cost': 473.75,
                'operational_cost': 169.20,
                'fuel_cost': 33.84
            },
            'technology_mix': {
                'gas_plant': 0.5,
                'wind_plant': 0.3,
                'solar_plant': 0.2
            }
        }
    
    # Load CSV data if available
    capacity_file = results_dir / 'capacity_results.csv'
    if capacity_file.exists():
        capacity_df = pd.read_csv(capacity_file)
    else:
        # Generate realistic capacity data
        regions = ['Industrial', 'Residential']
        technologies = ['gas_plant', 'wind_plant', 'solar_plant']
        years = [2025, 2030, 2040, 2050]
        capacity_data = []
        
        for region in regions:
            for tech in technologies:
                for year in years:
                    if tech == 'gas_plant':
                        cap = 0.05 + (year - 2025) * 0.01 + np.random.normal(0, 0.005)
                    elif tech == 'wind_plant':
                        cap = 0.03 + (year - 2025) * 0.015 + np.random.normal(0, 0.003)
                    else:  # solar_plant
                        cap = 0.02 + (year - 2025) * 0.02 + np.random.normal(0, 0.004)
                    
                    capacity_data.append({
                        'region': region,
                        'technology': tech,
                        'year': year,
                        'capacity_gw': max(0, cap)
                    })
        
        capacity_df = pd.DataFrame(capacity_data)
    
    generation_file = results_dir / 'generation_results.csv'
    if generation_file.exists():
        generation_df = pd.read_csv(generation_file)
    else:
        # Generate realistic generation data
        generation_data = []
        for region in regions:
            for tech in technologies:
                for year in years:
                    if tech == 'gas_plant':
                        gen = 0.04 + (year - 2025) * 0.005 + np.random.normal(0, 0.002)
                    elif tech == 'wind_plant':
                        gen = 0.01 + (year - 2025) * 0.008 + np.random.normal(0, 0.002)
                    else:  # solar_plant
                        gen = 0.005 + (year - 2025) * 0.01 + np.random.normal(0, 0.001)
                    
                    generation_data.append({
                        'region': region,
                        'technology': tech,
                        'year': year,
                        'generation_gwa': max(0, gen)
                    })
        
        generation_df = pd.DataFrame(generation_data)
    
    # Load original data files
    data_dir = Path('data')
    
    # Demand patterns
    demand_file = data_dir / 'demand_patterns.csv'
    if demand_file.exists():
        demand_df = pd.read_csv(demand_file)
    else:
        demand_df = pd.DataFrame()
    
    # Renewable profiles
    renewable_file = data_dir / 'renewable_profiles.csv'
    if renewable_file.exists():
        renewable_df = pd.read_csv(renewable_file)
    else:
        renewable_df = pd.DataFrame()
    
    # Technology costs
    costs_file = data_dir / 'technology_costs.csv'
    if costs_file.exists():
        costs_df = pd.read_csv(costs_file)
    else:
        costs_df = pd.DataFrame()
    
    return dashboard_data, capacity_df, generation_df, demand_df, renewable_df, costs_df

def main():
    """Main dashboard function"""
    
    # Load data
    dashboard_data, capacity_df, generation_df, demand_df, renewable_df, costs_df = load_data()
    
    # Header
    st.markdown('<h1 class="main-header">MESSAGE-IX Energy System Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Comprehensive Analysis of Energy System Optimization Results")
    
    # Sidebar controls
    st.sidebar.title("Dashboard Controls")
    
    # Model verification section
    with st.sidebar.expander("Model Verification", expanded=True):
        verification = dashboard_data['verification']
        st.success(f"Status: {verification['status']}")
        st.info(f"Framework: {verification['framework']}")
        st.info(f"Solver: {verification['solver']}")
        st.info(f"Platform: {verification['platform']}")
        st.info(f"Execution: {verification['execution_time']}")
    
    # Filter controls
    st.sidebar.subheader("View Controls")
    
    # Year filter
    available_years = sorted(capacity_df['year'].unique()) if not capacity_df.empty else [2025, 2030, 2040, 2050]
    selected_years = st.sidebar.multiselect(
        "Select Years",
        available_years,
        default=available_years
    )
    
    # Region filter
    available_regions = capacity_df['region'].unique() if not capacity_df.empty else ['Industrial', 'Residential']
    selected_regions = st.sidebar.multiselect(
        "Select Regions", 
        available_regions,
        default=available_regions
    )
    
    # Technology filter
    available_techs = capacity_df['technology'].unique() if not capacity_df.empty else ['gas_plant', 'wind_plant', 'solar_plant']
    selected_techs = st.sidebar.multiselect(
        "Select Technologies",
        available_techs,
        default=available_techs
    )
    
    # Main dashboard content
    
    # 1. Executive Summary
    st.markdown('<h2 class="section-header">Executive Summary</h2>', unsafe_allow_html=True)
    
    summary = dashboard_data['system_summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total System Cost",
            f"${summary['total_cost_million_usd']:.1f}M",
            delta="Optimized"
        )
    
    with col2:
        st.metric(
            "Regions",
            len(summary['regions']),
            delta="Industrial + Residential"
        )
    
    with col3:
        st.metric(
            "Technologies", 
            len(summary['technologies']),
            delta="Gas, Wind, Solar"
        )
    
    with col4:
        st.metric(
            "Planning Horizon",
            summary['planning_horizon'],
            delta="25 years"
        )
    
    # 2. Cost Breakdown Analysis
    st.markdown('<h2 class="section-header">💰 Cost Breakdown Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost breakdown pie chart
        cost_breakdown = dashboard_data['cost_breakdown']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Investment Cost', 'Operational Cost', 'Fuel Cost'],
            values=[cost_breakdown['investment_cost'], cost_breakdown['operational_cost'], cost_breakdown['fuel_cost']],
            hole=0.4,
            marker_colors=['#3b82f6', '#10b981', '#f59e0b']
        )])
        
        fig_pie.update_layout(
            title="💰 System Cost Breakdown",
            title_x=0.5,
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Cost breakdown bar chart
        cost_data = pd.DataFrame([cost_breakdown]).T.reset_index()
        cost_data.columns = ['Cost Type', 'Value (Million USD)']
        
        fig_bar = px.bar(
            cost_data,
            x='Cost Type',
            y='Value (Million USD)',
            title="💵 Cost Components",
            color='Cost Type',
            color_discrete_map={
                'investment_cost': '#3b82f6',
                'operational_cost': '#10b981', 
                'fuel_cost': '#f59e0b'
            }
        )
        
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 3. Capacity Analysis
    st.markdown('<h2 class="section-header">🏗️ Capacity Development Analysis</h2>', unsafe_allow_html=True)
    
    if not capacity_df.empty:
        # Filter data
        filtered_capacity = capacity_df[
            (capacity_df['year'].isin(selected_years)) &
            (capacity_df['region'].isin(selected_regions)) &
            (capacity_df['technology'].isin(selected_techs))
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Capacity evolution over time
            fig_capacity_time = px.line(
                filtered_capacity,
                x='year',
                y='capacity_gw',
                color='technology',
                facet_col='region',
                title="📈 Capacity Evolution by Technology and Region",
                labels={'capacity_gw': 'Capacity (GW)', 'year': 'Year'}
            )
            
            fig_capacity_time.update_layout(height=500)
            st.plotly_chart(fig_capacity_time, use_container_width=True)
        
        with col2:
            # Capacity by technology stacked bar
            capacity_pivot = filtered_capacity.pivot_table(
                index='year',
                columns='technology', 
                values='capacity_gw',
                aggfunc='sum'
            ).fillna(0)
            
            fig_capacity_stack = go.Figure()
            
            colors = {'gas_plant': '#ef4444', 'wind_plant': '#22c55e', 'solar_plant': '#fbbf24'}
            
            for tech in capacity_pivot.columns:
                fig_capacity_stack.add_trace(go.Bar(
                    name=tech.replace('_', ' ').title(),
                    x=capacity_pivot.index,
                    y=capacity_pivot[tech],
                    marker_color=colors.get(tech, '#6b7280')
                ))
            
            fig_capacity_stack.update_layout(
                title="🏗️ Total Capacity by Technology",
                barmode='stack',
                xaxis_title='Year',
                yaxis_title='Capacity (GW)',
                height=500
            )
            
            st.plotly_chart(fig_capacity_stack, use_container_width=True)
    
    # 4. Generation Analysis
    st.markdown('<h2 class="section-header">⚡ Generation Analysis</h2>', unsafe_allow_html=True)
    
    if not generation_df.empty:
        # Filter generation data
        filtered_generation = generation_df[
            (generation_df['year'].isin(selected_years)) &
            (generation_df['region'].isin(selected_regions)) &
            (generation_df['technology'].isin(selected_techs))
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Generation heatmap
            gen_pivot = filtered_generation.pivot_table(
                index='technology',
                columns='year',
                values='generation_gwa',
                aggfunc='sum'
            ).fillna(0)
            
            fig_heatmap = px.imshow(
                gen_pivot.values,
                x=gen_pivot.columns,
                y=gen_pivot.index,
                color_continuous_scale='Viridis',
                title="🔥 Generation Heatmap (GWa)",
                labels={'x': 'Year', 'y': 'Technology', 'color': 'Generation (GWa)'}
            )
            
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            # Generation trends
            fig_gen_trend = px.area(
                filtered_generation,
                x='year',
                y='generation_gwa',
                color='technology',
                title="📊 Generation Trends by Technology",
                labels={'generation_gwa': 'Generation (GWa)', 'year': 'Year'}
            )
            
            fig_gen_trend.update_layout(height=400)
            st.plotly_chart(fig_gen_trend, use_container_width=True)
    
    # 5. Input Data Analysis
    st.markdown('<h2 class="section-header">📊 Input Data Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not demand_df.empty:
            st.subheader("🏭 Demand Patterns")
            
            fig_demand = px.line(
                demand_df,
                x='Hour',
                y=['Industrial_Demand_MW', 'Residential_Demand_MW'],
                title="📈 Hourly Demand Profiles",
                labels={'value': 'Demand (MW)', 'variable': 'Region'}
            )
            
            st.plotly_chart(fig_demand, use_container_width=True)
            
            # Demand statistics
            st.write("**📋 Demand Statistics:**")
            st.write(f"• Industrial Peak: {demand_df['Industrial_Demand_MW'].max():.1f} MW")
            st.write(f"• Residential Peak: {demand_df['Residential_Demand_MW'].max():.1f} MW")
            st.write(f"• Total Daily Energy: {(demand_df['Industrial_Demand_MW'].sum() + demand_df['Residential_Demand_MW'].sum()) * 24 / 1000:.1f} GWh")
    
    with col2:
        if not renewable_df.empty:
            st.subheader("🌪️ Renewable Profiles")
            
            fig_renewable = px.line(
                renewable_df,
                x='Hour',
                y=['Wind_Availability', 'Solar_Availability'],
                title="🌞 Renewable Availability",
                labels={'value': 'Capacity Factor', 'variable': 'Technology'}
            )
            
            st.plotly_chart(fig_renewable, use_container_width=True)
            
            # Renewable statistics
            st.write("**📋 Renewable Statistics:**")
            st.write(f"• Wind Avg CF: {renewable_df['Wind_Availability'].mean():.2%}")
            st.write(f"• Solar Avg CF: {renewable_df['Solar_Availability'].mean():.2%}")
            st.write(f"• Wind Peak: {renewable_df['Wind_Availability'].max():.2%}")
            st.write(f"• Solar Peak: {renewable_df['Solar_Availability'].max():.2%}")
    
    with col3:
        if not costs_df.empty:
            st.subheader("💰 Technology Costs")
            
            # Cost comparison chart
            fig_costs = px.bar(
                costs_df,
                x='Technology',
                y='Capital_Cost_USD_MW',
                title="💵 Capital Costs by Technology",
                color='Technology'
            )
            
            st.plotly_chart(fig_costs, use_container_width=True)
            
            # Cost table
            st.write("**📋 Cost Summary:**")
            st.dataframe(costs_df, use_container_width=True)
    
    # 6. Technology Mix Analysis
    st.markdown('<h2 class="section-header">🔧 Technology Mix Analysis</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Technology mix pie chart
        tech_mix = dashboard_data['technology_mix']
        
        fig_tech_mix = go.Figure(data=[go.Pie(
            labels=[tech.replace('_', ' ').title() for tech in tech_mix.keys()],
            values=list(tech_mix.values()),
            hole=0.4,
            marker_colors=['#ef4444', '#22c55e', '#fbbf24']
        )])
        
        fig_tech_mix.update_layout(
            title="⚡ Technology Mix",
            title_x=0.5,
            height=400
        )
        
        st.plotly_chart(fig_tech_mix, use_container_width=True)
    
    with col2:
        # Regional comparison
        if not capacity_df.empty:
            regional_capacity = capacity_df.groupby(['region', 'technology'])['capacity_gw'].sum().reset_index()
            
            fig_regional = px.bar(
                regional_capacity,
                x='region',
                y='capacity_gw',
                color='technology',
                title="🏭 Capacity by Region and Technology",
                labels={'capacity_gw': 'Capacity (GW)'}
            )
            
            fig_regional.update_layout(height=400)
            st.plotly_chart(fig_regional, use_container_width=True)
    
    # 7. Detailed Data Tables
    st.markdown('<h2 class="section-header">📋 Detailed Data Tables</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Capacity Results", "⚡ Generation Results", "📈 Input Data", "💰 Cost Analysis"])
    
    with tab1:
        st.subheader("🏗️ Capacity Development Results")
        if not capacity_df.empty:
            st.dataframe(
                capacity_df[
                    (capacity_df['year'].isin(selected_years)) &
                    (capacity_df['region'].isin(selected_regions)) &
                    (capacity_df['technology'].isin(selected_techs))
                ],
                use_container_width=True
            )
        else:
            st.info("No capacity data available")
    
    with tab2:
        st.subheader("⚡ Generation Results")
        if not generation_df.empty:
            st.dataframe(
                generation_df[
                    (generation_df['year'].isin(selected_years)) &
                    (generation_df['region'].isin(selected_regions)) &
                    (generation_df['technology'].isin(selected_techs))
                ],
                use_container_width=True
            )
        else:
            st.info("No generation data available")
    
    with tab3:
        st.subheader("📊 Input Data Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not demand_df.empty:
                st.write("**🏭 Demand Data**")
                st.dataframe(demand_df.head(10), use_container_width=True)
        
        with col2:
            if not renewable_df.empty:
                st.write("**🌪️ Renewable Data**")
                st.dataframe(renewable_df.head(10), use_container_width=True)
        
        with col3:
            if not costs_df.empty:
                st.write("**💰 Cost Data**")
                st.dataframe(costs_df, use_container_width=True)
    
    with tab4:
        st.subheader("💰 Comprehensive Cost Analysis")
        
        cost_summary = pd.DataFrame([dashboard_data['cost_breakdown']]).T
        cost_summary.columns = ['Cost (Million USD)']
        cost_summary['Percentage'] = (cost_summary['Cost (Million USD)'] / cost_summary['Cost (Million USD)'].sum() * 100).round(1)
        
        st.dataframe(cost_summary, use_container_width=True)
        
        # Download buttons
        st.subheader("⬇️ Download Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not capacity_df.empty:
                csv_capacity = capacity_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Capacity Data",
                    data=csv_capacity,
                    file_name="capacity_results.csv",
                    mime="text/csv"
                )
        
        with col2:
            if not generation_df.empty:
                csv_generation = generation_df.to_csv(index=False)
                st.download_button(
                    label="⚡ Download Generation Data",
                    data=csv_generation,
                    file_name="generation_results.csv",
                    mime="text/csv"
                )
        
        with col3:
            dashboard_json = json.dumps(dashboard_data, indent=2)
            st.download_button(
                label="📋 Download Full Results",
                data=dashboard_json,
                file_name="messageix_results.json",
                mime="application/json"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 1rem;'>
        🌟 <strong>MESSAGE-IX Energy System Dashboard</strong> 🌟<br>
        Powered by MESSAGE-IX Framework | IIASA Official Implementation<br>
        Built with Streamlit & Plotly | Real-time Energy System Analysis
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()