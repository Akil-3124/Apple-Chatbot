import streamlit as st
from typing import Generator, Optional
from groq import Groq
import json
import requests
import os

# Set up Streamlit page configuration
st.set_page_config(layout="wide", page_title="Apple Chatbot")

st.title("Apple chatbot")
st.subheader("",divider="orange", anchor=False)

# Initialize Groq client with API key
client = Groq(api_key="Groq API KEY")

# Load the external knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the knowledge base from the JSON file
knowledge_base = load_knowledge_base("knowledge_base.json")

# Check if session_state has messages initialized
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Function to search the knowledge base
def search_knowledge_base(prompt: str) -> Optional[str]:
    """Check if the prompt matches any title in the knowledge base and return the description if found."""
    for item in knowledge_base:
        if item['title'].lower() in prompt.lower():
            return item['description']
    return None

# Function to generate chat responses from Groq API response
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def create_prompt_template(user_prompt: str, knowledge_response: str = "") -> str:
    """Create a prompt template that ensures the chat is an Apple customer care chatbot."""
    return f"""
    You are an Apple customer care representative with 10 years of experience. 
    Only provide answers related to Apple products and services, with a focus on Apple iPhones.
    Always be professional and courteous in your responses. If the question is not related to Apple or its products, politely inform the user that your expertise is limited to Apple products.

    Knowledge Base Information: {knowledge_response}  # Add knowledge response to the prompt
    User's Question: {user_prompt}
    """

# Function to extract titles and descriptions from API response
def extract_titles_and_descriptions(data, query):
    output = []
    # Check if 'results' key exists in the API response
    if 'results' in data:
        for result in data['results']:
            output.append({
                "title": query,  # Set the title to the user's query
                "description": result.get("description", "No description")  # Use the API's description
            })
    return output

# Get the API response for related keywords
def fetch_related_keywords(query):
    url = "https://joj-web-search.p.rapidapi.com/"
    querystring = {"query": query, "limit": "2", "related_keywords": "true"}

    headers = {
        "x-rapidapi-key": "RAPIDAPI KEY",
        "x-rapidapi-host": "joj-web-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Load existing knowledge base or initialize an empty list
file_path = "knowledge_base.json"
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        knowledge_base = json.load(file)
else:
    knowledge_base = []

if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch related keywords from the API
    api_response = fetch_related_keywords(prompt)
    output_data = extract_titles_and_descriptions(api_response, prompt)  # Pass the prompt as the title
    
    # Append new data to the existing knowledge base
    knowledge_base.extend(output_data)

    # Save the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(knowledge_base, file, indent=4)

    # Now search the knowledge base after updating it
    knowledge_base_response = search_knowledge_base(prompt)

    # If a knowledge base response is found, use it in the prompt
    if knowledge_base_response:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(knowledge_base_response)
        st.session_state.messages.append({"role": "assistant", "content": knowledge_base_response})
        formatted_prompt = create_prompt_template(prompt, knowledge_response=knowledge_base_response)  # Add knowledge response to prompt
    else:
        formatted_prompt = create_prompt_template(prompt)

    try:
        chat_completion = client.chat.completions.create(
            model="gemma-7b-it",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an Apple iPhone customer care assistant with 10 years of experience."
                },
                {
                    "role": "user", 
                    "content": formatted_prompt
                }
            ],
            stream=True
        )

        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)
    except Exception as e:
        st.error(e, icon="🚨")

    if isinstance(full_response, str):
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        combined_response = "\n".join(str(item) for item in full_response)
        st.session_state.messages.append({"role": "assistant", "content": combined_response})
