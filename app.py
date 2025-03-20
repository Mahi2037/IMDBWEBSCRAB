import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 🎯 Connect to TiDB Cloud
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
            port=4000,
            user="3VYhXePBWtRATMR.root",
            password="x6mZSRxbndttBExE",
            database="IMDB",
            ssl_ca=r"L:\Guvi\Project 1\certs\ca.pem"  # ✅ Update CA path
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"❌ Database connection error: {err}")
        return None

# 📌 Fetch movie data from TiDB
def fetch_movies():
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()  # Return empty DataFrame if connection fails
    
    query = "SELECT `Movie Name`, `Genre`, `Ratings`, `Voting Counts`, `Duration` FROM movies"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

# 🔄 Load data
df = fetch_movies()

# 🚨 Handle case where no data is retrieved
if df.empty:
    st.error("⚠️ No data retrieved from database!")
    st.stop()

# 📢 Debugging: Print Column Names
st.write("🔍 Columns in dataset:", df.columns.tolist())

# ✅ Convert Duration to Minutes (e.g., "2h 30m" → 150)
def convert_duration(duration_str):
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', str(duration_str))  # Extract hours & minutes
    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes
    return None  # If format is incorrect

df['Duration'] = df['Duration'].apply(convert_duration)
df.dropna(subset=['Duration'], inplace=True)
df['Duration'] = df['Duration'].astype(int)

# 📢 App Title
st.title("🎬 IMDb 2024 Movie Data Analysis (TiDB Cloud)")

# 🎛 Sidebar Filters
st.sidebar.header("🔍 Filter Movies")
selected_genre = st.sidebar.multiselect("🎭 Select Genre", df['Genre'].unique())
rating_range = st.sidebar.slider("⭐ Select Rating Range", float(df['Ratings'].min()), 10.0, (5.0, 9.0))
vote_count_min = st.sidebar.number_input("🗳️ Minimum Vote Count", min_value=int(df['Voting Counts'].min()), value=1000, step=1000)
duration_range = st.sidebar.slider("⏳ Select Duration (Minutes)", float(df['Duration'].min()), float(df['Duration'].max()), (60.0, 180.0))

# 📊 Apply Filters
filtered_df = df.copy()
if selected_genre:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genre)]
filtered_df = filtered_df[(filtered_df['Ratings'] >= rating_range[0]) & (filtered_df['Ratings'] <= rating_range[1])]
filtered_df = filtered_df[filtered_df['Voting Counts'] >= vote_count_min]
filtered_df = filtered_df[(filtered_df['Duration'] >= duration_range[0]) & (filtered_df['Duration'] <= duration_range[1])]

# 📋 Display Filtered Data
st.subheader("🎯 Filtered Movies")
st.dataframe(filtered_df)

# 🎥 Top 10 Movies by Rating
st.subheader("🏆 Top 10 Movies by Rating")
top_movies = df.nlargest(10, 'Ratings')
st.table(top_movies[['Movie Name', 'Genre', 'Ratings', 'Voting Counts']])

# 📊 Genre Distribution
st.subheader("📊 Genre Distribution")
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='Genre', order=df['Genre'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(plt)

# ⏳ Average Duration by Genre
st.subheader("⏳ Average Duration by Genre")
plt.figure(figsize=(10, 5))
df.groupby('Genre')['Duration'].mean().sort_values().plot(kind='barh')
st.pyplot(plt)

# ⭐ Rating Distribution
st.subheader("⭐ Rating Distribution")
plt.figure(figsize=(8, 5))
sns.histplot(df['Ratings'], bins=20, kde=True)
st.pyplot(plt)

# 🔗 Correlation Between Ratings and Votes
st.subheader("🔗 Correlation Between Ratings and Votes")
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Ratings', y='Voting Counts')
st.pyplot(plt)

st.write("🚀 Made with ❤️ using Streamlit & TiDB Cloud")
