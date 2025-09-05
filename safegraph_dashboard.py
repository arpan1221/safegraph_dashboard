import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import gzip
import csv
from pathlib import Path
from collections import defaultdict, Counter

# Page configuration
st.set_page_config(
    page_title="SafeGraph Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Load data (you can replace this with your actual data loading)
@st.cache_data
def load_safegraph_data():
    """Load SafeGraph analysis results"""
    # This is the data from your analysis - you can load from a file or database
    return {
        'summary': {
            'files_processed': 355,
            'total_countries': 54,
            'total_years': 7,
            'total_observations': 82258359
        },
        'countries': {
            'AK': {'total_observations': 161531, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'AL': {'total_observations': 1435489, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'AR': {'total_observations': 650754, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'AZ': {'total_observations': 1837518, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'CA': {'total_observations': 9089835, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'CO': {'total_observations': 1555083, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'CT': {'total_observations': 877345, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'DC': {'total_observations': 213756, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'DE': {'total_observations': 295024, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'FL': {'total_observations': 5757769, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'GA': {'total_observations': 2982614, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'GU': {'total_observations': 1018, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 328},
            'HI': {'total_observations': 360463, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'IA': {'total_observations': 713128, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'ID': {'total_observations': 575163, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'IL': {'total_observations': 3256771, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'IN': {'total_observations': 1901972, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'KS': {'total_observations': 620241, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'KY': {'total_observations': 1237199, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'LA': {'total_observations': 1014531, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'MA': {'total_observations': 1500754, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'MD': {'total_observations': 1533119, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'ME': {'total_observations': 415258, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'MI': {'total_observations': 2532556, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'MN': {'total_observations': 975086, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'MO': {'total_observations': 1263233, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'MS': {'total_observations': 679167, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'MT': {'total_observations': 272116, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'NC': {'total_observations': 2991914, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'ND': {'total_observations': 173484, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'NE': {'total_observations': 396218, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'NH': {'total_observations': 358016, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'NJ': {'total_observations': 2197496, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'NM': {'total_observations': 510081, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'NV': {'total_observations': 815713, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'NY': {'total_observations': 4248586, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'OH': {'total_observations': 3222940, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'OK': {'total_observations': 851591, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'OR': {'total_observations': 1260443, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'PA': {'total_observations': 3176600, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'PR': {'total_observations': 34927, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'RI': {'total_observations': 237627, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'SC': {'total_observations': 1460614, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'SD': {'total_observations': 171842, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'TN': {'total_observations': 1859970, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'TX': {'total_observations': 7347965, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'UT': {'total_observations': 905365, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'VA': {'total_observations': 2309786, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'VI': {'total_observations': 758, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 298},
            'VT': {'total_observations': 164183, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'WA': {'total_observations': 1917706, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'WI': {'total_observations': 1315724, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354},
            'WV': {'total_observations': 449563, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 355},
            'WY': {'total_observations': 170754, 'years_present': [2019, 2020, 2021, 2022, 2023, 2024, 2025], 'files_with_data': 354}
        },
        'years': {
            '2019': {'total_observations': 12273495, 'countries_present': 54},
            '2020': {'total_observations': 11752616, 'countries_present': 54},
            '2021': {'total_observations': 12338129, 'countries_present': 54},
            '2022': {'total_observations': 12623873, 'countries_present': 54},
            '2023': {'total_observations': 12624914, 'countries_present': 54},
            '2024': {'total_observations': 13003950, 'countries_present': 54},
            '2025': {'total_observations': 7641382, 'countries_present': 54}
        }
    }

def main():
    # Load data
    data = load_safegraph_data()
    
    # Header
    st.markdown('<h1 class="main-header">📊 SafeGraph Data Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Quick Answer Section
    st.markdown("---")
    st.markdown("### 🎯 Quick Answers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**How many countries?**")
        st.markdown(f"# {data['summary']['total_countries']}")
        st.markdown("*US States & Territories*")
    
    with col2:
        st.markdown("**Which countries?**")
        country_list = sorted(data['countries'].keys())
        st.markdown(f"**{len(country_list)}** countries including:")
        st.markdown(f"• **Top 5:** {', '.join(country_list[:5])}")
        st.markdown(f"• **All:** {', '.join(country_list)}")
    
    with col3:
        st.markdown("**Observations per year?**")
        year_obs = {year: info['total_observations'] for year, info in data['years'].items()}
        peak_year = max(year_obs, key=year_obs.get)
        st.markdown(f"**Peak:** {peak_year} ({year_obs[peak_year]:,})")
        st.markdown(f"**Range:** {min(year_obs.values()):,} - {max(year_obs.values()):,}")
    
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("🔍 Filters & Controls")
    
    # Year filter
    available_years = sorted(data['years'].keys())
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=available_years,
        default=available_years
    )
    
    # State filter
    available_states = sorted(data['countries'].keys())
    selected_states = st.sidebar.multiselect(
        "Select States/Territories",
        options=available_states,
        default=available_states[:10]  # Show top 10 by default
    )
    
    # Summary metrics
    st.subheader("📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Observations",
            value=f"{data['summary']['total_observations']:,}",
            delta="82.3M"
        )
    
    with col2:
        st.metric(
            label="States/Territories",
            value=data['summary']['total_countries'],
            delta="54"
        )
    
    with col3:
        st.metric(
            label="Years Covered",
            value=data['summary']['total_years'],
            delta="2019-2025"
        )
    
    with col4:
        st.metric(
            label="Files Processed",
            value=data['summary']['files_processed'],
            delta="355"
        )
    
    # Countries and Observations Summary
    st.subheader("🌍 Countries with Data & Observations per Year")
    
    # Create a comprehensive summary table
    summary_data = []
    for state, info in data['countries'].items():
        # Calculate average observations per year
        avg_per_year = info['total_observations'] / len(info['years_present'])
        
        summary_data.append({
            'Country/State': state,
            'Total Observations': f"{info['total_observations']:,}",
            'Years Present': f"{len(info['years_present'])}",
            'Avg per Year': f"{avg_per_year:,.0f}",
            'Files with Data': info['files_with_data']
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.sort_values('Total Observations', ascending=False)
    
    # Display top 20 countries
    st.write("**Top 20 Countries/States by Total Observations:**")
    st.dataframe(
        summary_df.head(20), 
        use_container_width=True,
        hide_index=True
    )
    
    # Yearly breakdown
    st.subheader("📅 Observations by Year")
    year_summary_data = []
    for year, info in data['years'].items():
        year_summary_data.append({
            'Year': year,
            'Total Observations': f"{info['total_observations']:,}",
            'Countries Present': info['countries_present'],
            'Avg per Country': f"{info['total_observations'] / info['countries_present']:,.0f}"
        })
    
    year_summary_df = pd.DataFrame(year_summary_data)
    year_summary_df = year_summary_df.sort_values('Year')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Yearly Summary:**")
        st.dataframe(year_summary_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Quick stats
        st.write("**Quick Stats:**")
        st.write(f"• **Total Countries/States:** {len(data['countries'])}")
        st.write(f"• **Years Covered:** {', '.join(sorted(data['years'].keys()))}")
        st.write(f"• **Largest State:** {summary_df.iloc[0]['Country/State']} ({summary_df.iloc[0]['Total Observations']} observations)")
        st.write(f"• **Peak Year:** {year_summary_df.loc[year_summary_df['Total Observations'].str.replace(',', '').astype(int).idxmax(), 'Year']} ({year_summary_df.loc[year_summary_df['Total Observations'].str.replace(',', '').astype(int).idxmax(), 'Total Observations']} observations)")
    
    # Detailed country-year breakdown
    st.subheader("🔍 Detailed Country-Year Breakdown")
    
    # Create detailed breakdown table
    detailed_data = []
    for state in sorted(data['countries'].keys()):
        state_info = data['countries'][state]
        for year in sorted(data['years'].keys()):
            # Estimate observations for this state-year combination
            # This is a simplified calculation - in reality you'd have exact data
            state_total = state_info['total_observations']
            year_total = data['years'][year]['total_observations']
            estimated = int(state_total * year_total / data['summary']['total_observations'])
            
            detailed_data.append({
                'Country/State': state,
                'Year': year,
                'Observations': f"{estimated:,}"
            })
    
    detailed_df = pd.DataFrame(detailed_data)
    
    # Add search functionality
    search_term = st.text_input("🔍 Search for specific country/state:", placeholder="e.g., CA, TX, New York")
    
    if search_term:
        filtered_df = detailed_df[detailed_df['Country/State'].str.contains(search_term.upper(), case=False)]
        st.write(f"**Results for '{search_term}':**")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
        # Show first 50 rows by default
        st.write("**First 50 entries (use search to find specific countries):**")
        st.dataframe(detailed_df.head(50), use_container_width=True, hide_index=True)
        
        if len(detailed_df) > 50:
            st.write(f"*Showing 50 of {len(detailed_df)} total entries. Use search to find specific countries.*")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Geographic Analysis", "📅 Temporal Analysis", "🔍 Detailed Breakdown", "📊 Data Quality"])
    
    with tab1:
        st.subheader("Geographic Distribution")
        
        # Prepare data for geographic visualization
        geo_data = []
        for state, info in data['countries'].items():
            if state in selected_states:
                geo_data.append({
                    'State': state,
                    'Observations': info['total_observations'],
                    'Files with Data': info['files_with_data']
                })
        
        geo_df = pd.DataFrame(geo_data)
        
        # Bar chart
        fig_bar = px.bar(
            geo_df,
            x='State',
            y='Observations',
            title='Observations by State/Territory',
            color='Observations',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Top 10 states
        st.subheader("Top 10 States by Observations")
        top_10 = geo_df.nlargest(10, 'Observations')
        st.dataframe(top_10, use_container_width=True)
    
    with tab2:
        st.subheader("Temporal Trends")
        
        # Prepare year data
        year_data = []
        for year, info in data['years'].items():
            if year in selected_years:
                year_data.append({
                    'Year': int(year),
                    'Observations': info['total_observations'],
                    'Countries': info['countries_present']
                })
        
        year_df = pd.DataFrame(year_data)
        
        # Line chart for observations over time
        fig_line = px.line(
            year_df,
            x='Year',
            y='Observations',
            title='Observations Over Time',
            markers=True
        )
        fig_line.update_layout(height=400)
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Countries per year
        fig_countries = px.bar(
            year_df,
            x='Year',
            y='Countries',
            title='Number of Countries with Data by Year',
            color='Countries',
            color_continuous_scale='Greens'
        )
        fig_countries.update_layout(height=400)
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with tab3:
        st.subheader("Detailed State-Year Breakdown")
        
        # Create detailed breakdown
        breakdown_data = []
        for state in selected_states:
            if state in data['countries']:
                for year in selected_years:
                    # This would need to be calculated from your actual data
                    # For now, we'll estimate based on total observations
                    state_total = data['countries'][state]['total_observations']
                    year_total = data['years'][year]['total_observations']
                    estimated = int(state_total * year_total / data['summary']['total_observations'])
                    
                    breakdown_data.append({
                        'State': state,
                        'Year': int(year),
                        'Observations': estimated
                    })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        
        # Heatmap
        if not breakdown_df.empty:
            pivot_df = breakdown_df.pivot(index='State', columns='Year', values='Observations')
            
            fig_heatmap = px.imshow(
                pivot_df,
                title='Observations by State and Year (Heatmap)',
                color_continuous_scale='Reds',
                aspect='auto'
            )
            fig_heatmap.update_layout(height=600)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Data table
        st.subheader("Detailed Data Table")
        st.dataframe(breakdown_df, use_container_width=True)
    
    with tab4:
        st.subheader("Data Quality Metrics")
        
        # Data completeness
        completeness_data = []
        for state, info in data['countries'].items():
            if state in selected_states:
                completeness = (info['files_with_data'] / data['summary']['files_processed']) * 100
                completeness_data.append({
                    'State': state,
                    'Files with Data': info['files_with_data'],
                    'Completeness %': round(completeness, 2)
                })
        
        completeness_df = pd.DataFrame(completeness_data)
        
        # Completeness chart
        fig_completeness = px.bar(
            completeness_df,
            x='State',
            y='Completeness %',
            title='Data Completeness by State',
            color='Completeness %',
            color_continuous_scale='RdYlGn'
        )
        fig_completeness.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_completeness, use_container_width=True)
        
        # Summary statistics
        st.subheader("Data Quality Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            avg_completeness = completeness_df['Completeness %'].mean()
            st.metric("Average Completeness", f"{avg_completeness:.1f}%")
        
        with col2:
            min_completeness = completeness_df['Completeness %'].min()
            st.metric("Minimum Completeness", f"{min_completeness:.1f}%")
    
    # Footer
    st.markdown("---")
    st.markdown("**SafeGraph Data Analysis Dashboard** | Generated with Streamlit")
    st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
