
# Apple Chatbot with Streamlit


This repository contains a chatbot application for Apple product support, built using Streamlit, Groq API, and RapidAPI. The chatbot uses an external knowledge base and API integration to provide real-time Apple-related answers to user queries.



## Features

- Apple Chatbot: A virtual Apple customer support agent, specializing in Apple iPhones. 
- Knowledge Base: Searches an external knowledge base for answers and learns from new user queries.
- Real-Time API Integration: Fetches related keywords and information through RapidAPI to dynamically expand the knowledge base.
- Session State: Retains user and assistant messages for ongoing conversations.
- Streamlit UI: Displays chat messages with user-friendly avatars for a seamless interaction experience.



## Installation

#### 1.Clone the repository:

```bash
  git clone https://github.com/your-username/apple-chatbot.git
  cd apple-chatbot
```
#### 2.Install dependencies: Create a virtual environment (optional but recommended) and install the necessary packages: 

```bash
 pip install -r requirements.txt
```
#### 3.Set up API keys:
- Replace "Groq API KEY" in the code with your actual Groq API key.
- Replace "RAPIDAPI KEY" with your actual RapidAPI key in the - - - fetch_related_keywords function.

#### 4.Prepare Knowledge Base:

- Place a knowledge_base.json file in the project root directory.
- If you don't have a knowledge base file, the app will initialize with an empty list and dynamically update as new queries are entered.



## Running the Application

#### 1.Run the Streamlit app:

```bash
  streamlit run chatbot.py
```


#### 2.Interact with the chatbot:

- The application will launch in your browser, where you can start chatting with the Apple virtual assistant.
- Enter prompts to receive answers related to Apple products.
- The chatbot learns from new queries and adds relevant information to the knowledge base.



## API Integration

#### The chatbot uses two APIs:

- Groq API: Provides natural language processing to simulate the Apple customer care chatbot.
- RapidAPI Web Search: Fetches related keywords and descriptions to dynamically extend the knowledge






## File Structure
```bash
├── chatbot.py                 # Main Streamlit application
├── knowledge_base.json        # JSON file storing the knowledge base
├── requirements.txt           # List of required Python packages
└── README.md                  # Project documentation (this file)

```





## Customization

- Knowledge Base: You can modify the knowledge_base.json file with predefined questions and answers.
- Prompt Template: Customize the chatbot's tone and expertise by editing the create_prompt_template function.
