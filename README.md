# Recipe Generator Chatbot 🍳 #
## ***Project Summary*** ##
The Recipe Finder Chatbot is an interactive AI-powered application that helps users explore and discover recipes based on their preferences. Built using Streamlit, the chatbot queries a FAISS vector database for relevant recipes and uses the Gemini API for AI-generated contextual responses. Users can ask queries like "low-calorie chicken recipe" or "quick pasta recipe," and the chatbot provides detailed information, including recipe descriptions, ingredients, steps, reviews, and ratings.This project leverages FAISS (Facebook AI Similarity Search) for efficient similarity searches and SentenceTransformers for embedding textual data. It integrates Streamlit to create a user-friendly conversational interface, making recipe discovery simple and fun.

## ***Features*** ##
*Recipe Search*: Find recipes based on keywords.
*Detailed Responses*: Includes ingredients, number of steps, reviews, ratings, and more.
*AI-Enhanced Results*: Uses the Gemini API to provide AI-generated summaries.
*Conversational Interface*: A chatbot-like interface for an engaging user experience.
*Dataset*
The project uses a dataset of recipes containing details like:

Recipe names
Descriptions
Ingredients and steps
Reviews and ratings
The dataset has been preprocessed and reduced for performance. The reduced_dataset.csv file contains 50,000 recipes sampled from the original dataset.

## ***Setup Instructions*** ##
*Step 1*: Clone the Repository
Clone this repository to your local machine and extract the zip file which include the dataset for chatbot:

*Step 2*: Install Dependencies
Create a virtual environment and install the required libraries:
- `pip install -r requirements.txt`

*Step 3*: Add Dataset
Ensure the `reduced_dataset.csv` file is placed in the project folder. The dataset is essential for the chatbot to retrieve recipes.

*Step 4*: Add Your Gemini API Key
Create your gemini API from Gemini website and add that API in the app.py

*Step 5*: Run the Application
Launch the chatbot using Streamlit:
- `streamlit run app.py`

*Step 6*: Interact with the Chatbot
Open the URL displayed in your terminal (e.g., http://localhost:8501).
Start typing your queries in the chatbot interface.
Receive detailed, AI-enhanced recipe suggestions!
