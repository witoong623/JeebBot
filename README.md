# JeebBot

JeebBot is an AI-powered conversational agent designed to simulate dating conversations. It helps users practice and improve their conversational skills, providing an engaging and dynamic experience. The project aims to demonstrate advanced conversational capabilities such as tone adjustment, memory building, and real-time information retrieval.

## Features

The following features are being developed for JeebBot. Check them off as they are completed:

- [x] **Basic Conversation**
  Simple and engaging conversational abilities for general communication.

- [x] **Adjustable Characteristic**
  Allows users to specify name and characteristic of the bot.

- [ ] **Memory Building**
  Builds and retains knowledge about the "other person" during conversations.

- [ ] **Knowledge Retrieval During Conversations**
  Uses stored knowledge to make contextually relevant responses.

- [ ] **Conversation Initiation and Conclusion**
  Initiates conversations at appropriate times and knows when to conclude them.

- [ ] **Web Information Retrieval**
  Searches for relevant real-time information from external sources (e.g., Wikipedia).

- [ ] **Streamlit UI**
  Provides an intuitive chat interface with messaging and tone selection capabilities.

---

## Technologies Used

JeebBot is built using the following technologies:

- **LangChain**: For constructing and managing the conversational agent.
- **OpenAI compatible API**: Language model powering the conversation.
- **Streamlit**: For creating a user-friendly web-based interface.
- **Python**: Core programming language for logic and integration.
- **FAISS / Pinecone**: For memory and knowledge storage (if applicable).

---

## Installation and Setup

Follow these steps to set up and run JeebBot locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/jeebbot.git
   cd jeebbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501` to start using JeebBot.

---

## Project Structure

```
jeebbot/
├── app.py               # Main Streamlit application file
├── agent/               # Logic and configurations for LangChain agent
├── memory/              # Memory management modules
├── tools/               # Modules for external tool integrations
├── templates/           # Prompt templates for tone adjustment
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

---

## Roadmap

JeebBot is currently under active development. Here's the roadmap:

1. Complete the basic conversation feature.  
2. Implement tone adjustment for dynamic responses.  
3. Add memory capabilities to remember key facts.  
4. Integrate real-time web search for factual responses.  
5. Polish the Streamlit-based UI for a seamless user experience.
