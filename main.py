import pandas as pd
import requests
import glob
import os

# 1. data pre-processing layer
def load_and_clean_data():
    # load all yearly files then standardize them
    yearly_files = glob.glob('Books - 20*.csv') # find all the Books - YYYY.csv files automatically
    read_list = []
    
    for file in yearly_files:
        df = pd.read_csv(file)
        df = df.rename(columns={'Book title': 'Name'}) # standardize column names
        if 'Vote' in df.columns: # convert '⭐' to numeric scores (e.g., 4 stars = 4)
            df['Vote_Score'] = df['Vote'].str.count('⭐').fillna(0).astype(int)
        else:
            df['Vote_Score'] = 0
        read_list.append(df[['Name', 'Author', 'Genre', 'Vote_Score']])
    
    all_read = pd.concat(read_list, ignore_index=True) if read_list else pd.DataFrame()
    
    # load wishlist
    if os.path.exists('Book_wishlist.csv'):
        wishlist = pd.read_csv('Book_wishlist.csv')
    else:
        wishlist = pd.DataFrame(columns=['Name', 'Author', 'Genre'])
        
    return all_read, wishlist

# 2. API integration layer
def get_external_recommendations(read_df, wishlist_df):
    favorites = read_df[read_df['Vote_Score'] >= 4] # filter books you really liked (4 or 5 stars)
    if favorites.empty:
        return pd.DataFrame(columns=['Title', 'Author', 'Description'])
    
    top_genre = favorites['Genre'].mode()[0] if not favorites['Genre'].empty else "Fiction" # the most common genre you liked, or default to 'Fiction'    
    
    known_titles = set(read_df['Name'].str.lower().tolist() + # track existing titles in both read and wishlist to avoid duplicates
                       wishlist_df['Name'].str.lower().tolist())

    print(f"--- Profiling interest: {top_genre} ---")
    
    # Google Books API
    query = f"subject:{top_genre}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&orderBy=relevance&maxResults=20"
    
    new_suggestions = []
    try:
        response = requests.get(url)
        data = response.json()
        
        for item in data.get('items', []):
            info = item.get('volumeInfo', {})
            title = info.get('title')
            authors = info.get('authors', ['Unknown Author'])
            
            # Deduplication Check
            if title.lower() not in known_titles:
                new_suggestions.append({
                    'Title': title,
                    'Author': ", ".join(authors),
                    'Description': info.get('description', 'No description available.')[:150] + "..."
                })
    except Exception as e:
        print(f"Connection Error: {e}")
        
    return pd.DataFrame(new_suggestions).head(5)

# recommendation engine entry point
if __name__ == "__main__":
    print("Initializing Book Recommendation Engine...\n")
    
    # Step 1: clean and load
    all_read_books, wishlist = load_and_clean_data()
    
    if all_read_books.empty:
        print("Error: No reading history found. Please check your CSV files.")
    else:
        # Step 2: fetch and display recommendations
        recommendations = get_external_recommendations(all_read_books, wishlist)
        
        print("\n--- RECOMMENDED FOR YOU (NEW DISCOVERIES) ---")
        if not recommendations.empty:
            for i, row in recommendations.iterrows():
                print(f"{i+1}. {row['Title']} by {row['Author']}")
                print(f"   Summary: {row['Description']}\n")
        else:
            print("No new books found at this time.")