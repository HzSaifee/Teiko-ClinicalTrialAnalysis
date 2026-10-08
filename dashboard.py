import streamlit as st
import pandas as pd
import sqlite3
from scipy.stats import mannwhitneyu
import plotly.express as px


st.set_page_config(page_title="Loblaw Bio Clinical Trial Dashboard", layout="wide")
st.title("Loblaw Bio: Clinical Trial Analysis Dashboard")


@st.cache_data
def load_data(query):
    conn = sqlite3.connect('cell-count.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.markdown("---")


st.header("Part 2: Cell Population Frequencies per Sample")
part2_query = """
    WITH sample_totals AS (
        SELECT sample, SUM(count) as total_count
        FROM cell_counts
        GROUP BY sample
    )
    SELECT 
        c.sample,
        s.total_count,
        c.population,
        c.count,
        ROUND((CAST(c.count AS FLOAT) / s.total_count) * 100, 2) AS percentage
    FROM cell_counts c
    JOIN sample_totals s ON c.sample = s.sample
    ORDER BY c.sample, c.population;
"""
df_frequencies = load_data(part2_query)
st.dataframe(df_frequencies, use_container_width=True)

st.markdown("---")


st.header("Part 3: Responder vs Non-Responder Analysis")
st.markdown("Comparing relative frequencies in melanoma patients receiving miraclib (PBMC samples only).")
part3_query = """
    WITH sample_totals AS (
        SELECT sample, SUM(count) as total_count
        FROM cell_counts
        GROUP BY sample
    )
    SELECT 
        m.sample,
        m.response,
        c.population,
        ROUND((CAST(c.count AS FLOAT) / s.total_count) * 100, 2) AS percentage
    FROM samples m
    JOIN cell_counts c ON m.sample = c.sample
    JOIN sample_totals s ON m.sample = s.sample
    WHERE m.condition = 'melanoma' 
      AND m.treatment = 'miraclib' 
      AND m.sample_type = 'PBMC';
"""
df_stats = load_data(part3_query)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Relative Frequencies Distribution")
    
    fig = px.box(
        df_stats, 
        x='population', 
        y='percentage', 
        color='response',
        title="Immune Cell Population Frequencies: Responders vs Non-Responders",
        labels={
            'population': 'Cell Population', 
            'percentage': 'Relative Frequency (%)',
            'response': 'Response'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Statistical Significance")
    st.markdown("Mann-Whitney U Test Results (α = 0.05)")
    
    responders = df_stats[df_stats['response'] == 'yes']
    non_responders = df_stats[df_stats['response'] == 'no']
    
    results = []
    for cell_pop in df_stats['population'].unique():
        res_freq = responders[responders['population'] == cell_pop]['percentage']
        non_res_freq = non_responders[non_responders['population'] == cell_pop]['percentage']
        
        if len(res_freq) > 0 and len(non_res_freq) > 0:
            stat, p_value = mannwhitneyu(res_freq, non_res_freq, alternative='two-sided')
            results.append({
                'Population': cell_pop,
                'P-Value': round(p_value, 4),
                'Significant?': 'Yes' if p_value < 0.05 else 'No'
            })
            
    df_results = pd.DataFrame(results)
    st.table(df_results)

st.markdown("---")


st.header("Part 4: Baseline Subset Analysis")
st.markdown("Subset: Melanoma PBMC samples at baseline (time = 0) treated with miraclib.")

part4_query = """
    SELECT sample, project, subject, response, sex
    FROM samples
    WHERE condition = 'melanoma'
      AND sample_type = 'PBMC'
      AND time_from_treatment_start = 0
      AND treatment = 'miraclib';
"""
df_subset = load_data(part4_query)


df_subjects = df_subset.drop_duplicates(subset=['subject'])

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.subheader("Samples per Project")
    st.dataframe(df_subset['project'].value_counts().reset_index().rename(columns={'count': 'Samples'}))

with col_b:
    st.subheader("Subjects by Response")
    st.dataframe(df_subjects['response'].value_counts().reset_index().rename(columns={'count': 'Subjects'}))

with col_c:
    st.subheader("Subjects by Gender")
    st.dataframe(df_subjects['sex'].value_counts().reset_index().rename(columns={'count': 'Subjects'}))
