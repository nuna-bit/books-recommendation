# Books Recommendation 📚
## Project overview 

This repository contains a Python-based recommendation engine designed to analyze personal reading data and generate high-relevance book suggestions. The project documents an iterative development process, moving from a local similarity-based model to a dynamic hybrid system that integrates external data via a REST API.

## Technical implementation
### Phase 1: Local similarity-based model
The initial version of the engine utilized **content-based filtering** to map relationships between established reading history and a target wishlist.
- **Vectorization (TF-IDF)**: I used TfidfVectorizer to transform a *"metadata soup"* (concatenated author and genre strings) into a numerical feature space. This method uses **term frequency-inverse document frequency** to weight unique identifiers more heavily than common terms.
- **Similarity Mapping**: To determine the "distance" between books, I implemented **cosine similarity**. By calculating the cosine of the angle between two vectors, the model identifies books with the most similar metadata profiles.
- **Engineering Challenge**: While effective for known datasets, this approach was limited by the *"filter bubble"* effect—it could not suggest titles outside the existing CSV records

### Phase 2: Hybrid integration via Google Books API
To achieve true discovery and solve the "cold start" problem for small datasets, the architecture was upgraded to a *hybrid system*.
- **Dynamic profiling**: The system parses historical logs (2023–2026) to identify "high-affinity" features based on weighted user ratings (4 and 5-star filtered events).
- **External data fetching**: I integrated the **Google Books REST API** to query a global database using these high-affinity parameters.
- **Data integrity & deduplication**: To ensure recommendation quality, I implemented a filtering layer using Python `sets` that cross-references API results against the entire local history to prevent duplicate suggestions.

## Key Features
- **Preprocessing pipeline**: Automated cleaning of multi-year CSV files, including the conversion of UTF-8 star emojis into a numerical format for analysis.
- **Language-agnostic matching**: The feature engineering process is designed to handle diverse scripts (e.g., korean, japanese, and latin) by focusing on metadata commonalities.
- **Modular architecture**: The codebase is separated into logical modules for data ingestion, mathematical modeling, and API communication.

## Tech Stack
- Language: Python
- Data Analysis: `pandas`
- Machine Learning: `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`)
- Network: `requests` (REST API Integration)

## How to use
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/book-discovery-ml.git](https://github.com/your-username/book-discovery-ml.git)
   cd book-discovery-ml

2. Install Dependencies:
``` Bash
    pip install pandas scikit-learn requests
```
3. Data Configuration:
Ensure your local environment contains your reading history and wishlist files in the root directory:
- `books_2023.csv`, `books_2024.csv`, etc.
- `Book_wishlist.csv`

> Note: Personal CSV files are excluded from version control via .gitignore to maintain data privacy.

4. Run the Engine:
Execute the main script to process your data and fetch real-time recommendations from the Google Books API:
``` Bash
    python main.py