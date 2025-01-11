import streamlit as st
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import requests
import pandas as pd

# Custom wrapper for SentenceTransformer
class CustomEmbeddingWrapper:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def __call__(self, text):
        if isinstance(text, str):  # Single text input
            return self.model.encode([text], convert_to_tensor=True).tolist()[0]
        elif isinstance(text, list):  # Batch text input
            return self.model.encode(text, convert_to_tensor=True).tolist()
        else:
            raise ValueError("Input should be a string or a list of strings.")

# Load the reduced dataset
@st.cache_resource
def load_dataset():
    return pd.read_csv("reduced_dataset.csv")

# Load the FAISS index
@st.cache_resource
def load_faiss_index():
    embedding_function = CustomEmbeddingWrapper('all-MiniLM-L6-v2')  # Use the custom wrapper
    vector_store = FAISS.load_local(
        "recipes_faiss_index",
        embeddings=embedding_function,
        allow_dangerous_deserialization=True
    )
    return vector_store

# Gemini API Integration
def get_gemini_response(recipe_text, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": recipe_text}]}
        ]
    }
    response = requests.post(f"{url}?key={api_key}", headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Error in response structure."
    else:
        return f"Error: {response.status_code}\nResponse: {response.text}"

# Load the dataset and FAISS index
reduced_df = load_dataset()
vector_store = load_faiss_index()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm your Recipe Bot. Ask me anything about recipes, and I'll help you out!"}]

# Callback function to handle user input
def process_input():
    user_query = st.session_state.user_input.strip()
    if user_query:
        # Append the user's message
        st.session_state.messages.append({"role": "user", "content": user_query})

        try:
            # Query the FAISS index
            results = vector_store.similarity_search(user_query, k=3)

            if results:
                # Prepare the bot's response
                detailed_responses = []

                for result in results:
                    recipe_id = result.metadata.get("recipe_id")
                    row = reduced_df[reduced_df['recipe_id'] == int(recipe_id)].iloc[0]
                    detailed_responses.append(
                        f"Recipe Name: {row['name']}\n"
                        f"Description: {row['description']}\n"
                        f"Ingredients: {', '.join(eval(row['ingredients']))}\n"
                        f"Number of Ingredients: {row['n_ingredients']}\n"
                        f"Steps: {', '.join(eval(row['steps']))}\n"
                        f"Number of Steps: {row['n_steps']}\n"
                        f"User Review: {row['review']}\n"
                        f"Rating: {row['rating'] if 'rating' in row else 'No rating available'}."
                    )

                # Combine the responses for Gemini API
                combined_text = " ".join(detailed_responses)
                api_key = "AIzaSyBvoFCNmrk28JxhDkwsxZIVT23PlZ8l0B4"  # API key
                bot_response = get_gemini_response(combined_text, api_key)
            else:
                bot_response = "I couldn't find any matching recipes. Please try again with a different query."
        except Exception as e:
            bot_response = f"An error occurred: {e}"

        # Append the bot's response
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Clear the user input
        st.session_state.user_input = ""

# Streamlit UI
st.title("Recipe Finder Chatbot 🍳")
st.markdown("Chat with the bot to explore recipes and get detailed answers!")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")

# User input widget with callback
st.text_input(
    "Your Message:",
    key="user_input",
    on_change=process_input,
    placeholder="Type your message here..."
)
