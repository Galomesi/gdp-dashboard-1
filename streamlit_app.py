import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Set Streamlit page config
st.set_page_config(page_title="Startups Dashboard", page_icon="🌵", layout="wide")

st.title("📊 Startups Dashboard")
st.write("Welcome to the dashboard displaying data on startups!")

# Load the datasets
founders_data = pd.read_csv("Cleaned_Founders_Data.csv")
startup_data = pd.read_csv("Cleaned_Startup_Data.csv")

# Function to clean 'Cohort' column
def clean_cohort(value):
    if pd.isna(value) or value in ["Cactus Academy", "Checks"]:  
        return None  # Remove invalid values
    if value == "Current":
        return 12  # Convert 'Current' to cohort 12
    match = re.search(r'\d+', str(value))  # Extract only numbers
    return int(match.group()) if match else None  # Convert to integer

# Apply cleaning
founders_data["Cohort"] = founders_data["Cohort"].apply(clean_cohort)
founders_data["Cohort"] = pd.to_numeric(founders_data["Cohort"], errors="coerce")
founders_data = founders_data.dropna(subset=["Cohort"])

# Convert to calendar years
start_year = 2019
founders_data["Year"] = start_year + ((founders_data["Cohort"] - 1) // 2).astype(int)

# 🔍 **Filters in Sidebar**
st.sidebar.header("🔎 Filters")

# **Filter by Faculty**
if "Faculty" in founders_data.columns:
    faculty_list = ["All"] + list(founders_data["Faculty"].dropna().unique())
    selected_faculty = st.sidebar.selectbox("Select Faculty", faculty_list)
    
    if selected_faculty != "All":
        founders_data = founders_data[founders_data["Faculty"] == selected_faculty]

# **Filter by Startup Name**
if "Startup Name" in startup_data.columns:
    startup_list = ["All"] + list(startup_data["Startup Name"].dropna().unique())
    selected_startup = st.sidebar.selectbox("Select Startup", startup_list)
    
    if selected_startup != "All":
        startup_data = startup_data[startup_data["Startup Name"] == selected_startup]

# **Filter by Startup Type (Industry)**
if "Industry" in startup_data.columns:
    industry_list = ["All"] + list(startup_data["Industry"].dropna().unique())
    selected_industry = st.sidebar.selectbox("Select Startup Type (Industry)", industry_list)
    
    if selected_industry != "All":
        startup_data = startup_data[startup_data["Industry"] == selected_industry]

# Creating two columns for side-by-side visualization
col1, col2 = st.columns(2)

# 📊 **Graph 1: Yearly Trend of Startups**
with col1:
    st.subheader("📈 Startups by Year")
    
    # Slider to select year range
    min_year, max_year = int(founders_data["Year"].min()), int(founders_data["Year"].max())
    selected_years = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    # Filter data based on selected years
    filtered_data = founders_data[(founders_data["Year"] >= selected_years[0]) & (founders_data["Year"] <= selected_years[1])]

    # Count startups per year
    yearly_counts = filtered_data["Year"].value_counts().reset_index()
    yearly_counts.columns = ["Year", "Startup Count"]
    yearly_counts = yearly_counts.sort_values("Year")

    # Create an interactive bar chart with Plotly
    fig1 = px.bar(
        yearly_counts, 
        x="Year", 
        y="Startup Count", 
        title="📈 Trends in Number of Startups Over the Years", 
        labels={"Year": "Year", "Startup Count": "Number of Startups"}, 
        text_auto=True
    )
    
    st.plotly_chart(fig1)

# 📈 **Graph 2: Cohort (Semester) Distribution**
with col2:
    st.subheader("📊 Startups by Cohort (Semester)")

    # Count startups per cohort (th)
    cohort_counts = founders_data["Cohort"].value_counts().reset_index()
    cohort_counts.columns = ["Cohort", "Startup Count"]
    cohort_counts = cohort_counts.sort_values("Cohort")

    # Create an interactive bar chart with Plotly
    fig2 = px.bar(
        cohort_counts, 
        x="Cohort", 
        y="Startup Count", 
        title="📊 Distribution of Startups by Cohort (th)", 
        labels={"Cohort": "Cohort (Semester)", "Startup Count": "Number of Startups"}, 
        text_auto=True
    )
    
    st.plotly_chart(fig2)
