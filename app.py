import streamlit as st # for building the web app interface
import pandas as pd
import plotly.express as px # for interactive visualizations
from main import load_and_clean_data, get_external_recommendations

# --- PAGE CONFIG ---
st.set_page_config(page_title="Book Discovery Engine", layout="wide")
st.title("📚 My Book Discovery Dashboard")
st.markdown("Exploring personal reading habits and discovering new titles via Google Books API.")

# --- LOAD DATA ---
all_read_books, wishlist = load_and_clean_data()

if not all_read_books.empty:
    # --- SIDEBAR: STATISTICS ---
    st.sidebar.header("📊 Library Stats")
    total_books = len(all_read_books)
    avg_rating = all_read_books['Vote_Score'].mean()
    
    st.sidebar.metric("Total Books Read", total_books)
    st.sidebar.metric("Average Rating", f"{avg_rating:.2f} ⭐")

    # --- ROW 1: VISUALIZATIONS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Genres")
        genre_counts = all_read_books['Genre'].value_counts().reset_index()
        fig_genre = px.pie(genre_counts, values='count', names='Genre', hole=0.3)
        st.plotly_chart(fig_genre, use_container_width=True)

    with col2:
        st.subheader("Rating Distribution")
        fig_rating = px.histogram(all_read_books, x='Vote_Score', nbins=5, color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig_rating, use_container_width=True)

    # --- ROW 2: RECOMMENDATIONS ---
    st.divider()
    st.header("🔍 Get New Recommendations")
    if st.button("Find New Books Based on My Favorites"):
        with st.spinner("Querying Google Books API..."):
            recs = get_external_recommendations(all_read_books, wishlist)
            
            if not recs.empty:
                for _, row in recs.iterrows():
                    with st.expander(f"📖 {row['Title']} - {row['Author']}"):
                        st.write(row['Description'])
            else:
                st.warning("No new books found. Try rating more books highly!")
else:
    st.error("No data found. Please ensure your CSV files are in the directory.")