# Books Recommendation 📚

A personal data science and machine learning project that analyzes my historical reading data and ranks my "Wishlist" so I know exactly what book to pick up next!

## How it Works

This project uses a **content-based filtering** recommendation system powered by natural language processing (NLP). Here is a breakdown of the pipeline and the machine learning models I used:

### 1. Data collection & preprocessing
- The starting data includes CSV files of my reading history spanning multiple years, complete with my personal star ratings
- A "wishlist" CSV acts as the pool of candidates for recommendation

### 2. Text feature scraping (Google Books API)
- Titles alone aren't enough to capture the true identity of a book. The pipeline queries the **Google Books API** to dynamically fetch rich text descriptions and genre categories for every book in my dataset.

### 3. The machine learning model: TF-IDF and cosine similarity
- **TF-IDF vectorization (`scikit-learn`)**: To understand the text, the system uses a `TfidfVectorizer`. This converts the long text descriptions into high-dimensional numerical embeddings, identifying important identifying keywords and naturally filtering out common stop-words.
- **User profiling**: The algorithm then mathematically summarizes my taste by creating a personalized "user profile" vector. This is calculated by taking a weighted average of the TF-IDF vectors from my read books, heavily weighing the vectors of books I rated 4 or 5 stars.
- **Cosine similarity ranking**: Finally, the model calculates the **cosine similarity** between my aggregated user profile and every unread book in my wishlist. 

The final output is a ranked list of books from my wishlist that mathematically align with my reading preferences, based purely on their narrative and thematic content!

## 🛠️ Tech Stack & Libraries
- **Language:** Python
- **Environment:** Jupyter Notebooks
- **Data Manipulation:** `pandas`, `numpy`
- **Machine Learning:** `scikit-learn`
- **Integrations:** `urllib`, Google Books API