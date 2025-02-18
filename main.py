import traceback
import streamlit as st
import pandas as pd
import plotly.express as px



@st.cache_data
def load_data() -> pd.DataFrame:
    df:pd.DataFrame = pd.read_csv("animated_tv_Series.csv", encoding='latin-1')
    pd.set_option('display.max_colwidth', None)
    return df

def configure_page() -> None:
    st.set_page_config(page_title = "Animated TV Shows", layout="wide")

def get_highest_rated_imdb(df:pd.DataFrame) -> list:

    highest = df[df['IMDb'] == df['IMDb'].max()].reset_index()
    highest_names = ""
    n = len(highest.index)

    for i in range(n):
        highest_names += highest['Title'][i] + ", "

    return highest_names[:-2]

def get_highest_rated_google(df:pd.DataFrame) -> list:

    highest = df[df['google_user_rating'] == df['google_user_rating'].max()].reset_index()
    highest_names = ""
    n = len(highest.index)

    for i in range(n):
        highest_names += highest['Title'][i] + ", "

    return highest_names[:-2]

def generate_dashboard(_df:pd.DataFrame) -> None:
    
    try:
        df:pd.DataFrame = _df.copy()

        # Insights Calculation
        total_shows = len(df.index)
        total_techniques = len((df['Technique']).unique())
        total_channels = len(df['Channel'].unique())

        longest_running_show = df[df['TotalYears'] == df['TotalYears'].max()].reset_index()
        shortest_running_show = df[df['TotalYears'] == df['TotalYears'].min()].reset_index()
        max_episodes_per_year_show = df[df['EpisodesPerYear'] == df['EpisodesPerYear'].max()].reset_index()
        min_episodes_per_year_show = df[df['EpisodesPerYear'] == df['EpisodesPerYear'].min()].reset_index()
        df["Truncated Channel"] = df["Channel"].apply(lambda x: x[:15] + "..." if isinstance(x, str) and len(x) > 15 else x)
        top_10_channel = df["Channel"].value_counts().head(10).index[0]
        highest_rated_imdb = get_highest_rated_imdb(df)
        highest_rated_google = get_highest_rated_google(df)
        
        # Rendering Insights -  Overall
        st.title("Animated TV Shows Dashboard")
        st.subheader("Overall Insights")
        col1, col2, col3, col4, col5 = st.columns(5, gap="small",border=True)

        with col1:
            st.metric("Total Shows", total_shows)
        with col2:
            st.metric("Total Animation Techniques", total_techniques)
        with col3:
            st.metric("Total Channels", total_channels)
        with col4:
            st.metric("Shortest Running Show", shortest_running_show['Title'][0])
        with col5:
            st.metric("Longest Running Show", longest_running_show['Title'][0])
        


        col1, col2, col3 = st.columns(3, gap="small", border=True)

        with col1:
            st.metric("Show with max episodes per year", max_episodes_per_year_show['Title'][0])
        with col2:
            st.metric("Show with min episodes per year", min_episodes_per_year_show['Title'][0])
        with col3:
            st.metric("Most Popular Channel", top_10_channel)
            

        col1, col2 = st.columns(2, gap="small", border=True)
        with col1:
            st.metric("Highest Rated Shows (Imdb)", highest_rated_imdb)
        
        with col2:
            st.metric("Highest Rated Shows (Google)", highest_rated_google)
        
        # Rendering charts
        st.subheader("Detailed Insights")
        col1_chart, col2_chart, col3_chart = st.columns(3, gap="small", border=True)

        with col1_chart:
            top_10_channels = df['Technique'].value_counts().head(10)
            fig1 = px.pie(names=top_10_channels.index, values=top_10_channels.values, title="Top 10 Shows by Animation Technique")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2_chart:
            top_10_channels = df["Channel"].value_counts().head(10)
            fig2 = px.bar(x=top_10_channels.index, y=top_10_channels.values, labels={'x': 'Channel', 'y': 'Number of Shows'}, title="Top 10 Channels")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3_chart:
            episodes_per_year = df.groupby('YearStart')['EpisodesPerYear'].sum().reset_index()
            fig3 = px.line(x=episodes_per_year['YearStart'], y=episodes_per_year['EpisodesPerYear'], labels={'x': 'Year', 'y': 'Total Episodes'}, title="Episodes Over the Years")
            st.plotly_chart(fig3, use_container_width=True)

    
        col1 , col2 = st.columns(2, border=True)
        percentile_95 = df['Episodes'].quantile(0.95)
        df1 = df[df['Episodes'] < percentile_95]
        with col1:
            fig4 = px.scatter(df1, x="IMDb", y="Episodes", color="Truncated Channel", hover_data=["Title"],
                  labels={"Episodes": "Number of Episodes", "IMDb Rating": "IMDb Rating"},
                  title="Scatter Plot of IMDb Rating vs. Number of Episodes")
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            fig5 = px.scatter(df1, x="google_user_rating", y="Episodes", color="Truncated Channel", hover_data=["Title"],
                  labels={"Episodes": "Number of Episodes", "Google Rating": "google_user_rating"},
                  title="Scatter Plot of Google Rating vs. Number of Episodes")
            st.plotly_chart(fig5, use_container_width=True)
        
        # Explore Dataset
        with st.expander("Preview of Data"):
            st.write(df)
    
    
    except Exception as e:
        print(f"{traceback.format_exc()}")
        print(e)

def main() -> None:
    configure_page()
    df:pd.DataFrame = load_data()
    generate_dashboard(df)


if __name__ == "__main__":
    main()



