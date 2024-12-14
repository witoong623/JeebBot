# JeebBot

<p align="center">
  <img src="images/jeeb-bot-logo.webp" alt="JeebBot Logo" width="15%">
</p>

JeebBot is an AI-powered conversational agent designed to simulate dating conversations. It helps users practice and improve their conversational skills, providing an engaging and dynamic experience.

The project aims to gain hands-on experience in developing LLM conversational application and to explore the generative AI prompt engineering techniques.

## Features

The following features are being developed for JeebBot. Check them off as they are completed:

- [x] **Basic Conversation**
  Simple and engaging conversational abilities for general communication.

- [x] **Adjustable Characteristic**
  Allows users to specify name and characteristic of the bot.

- [x] **Memory Building**
  Builds and retains knowledge about the "other person" during conversations.

- [ ] **Conversation Initiation and Conclusion**
  Initiates conversations at appropriate times and knows when to conclude them.

- [ ] **Web Information Retrieval**
  Searches for relevant real-time information from external sources.

- [x] **Streamlit UI**
  Provides an intuitive chat interface with messaging and tone selection capabilities.

---

## Technologies Used

JeebBot is built using the following technologies:

- **LangChain**: For constructing and managing the conversational agent.
- **OpenAI API**: Language model powering the conversation.
- **Streamlit**: For creating a user-friendly web-based interface.
- **llama.cpp**: For hosting local LLM.

---

## Installation and Setup
Follow these steps to set up and run JeebBot locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/witoong623/JeebBot.git
   cd jeebbot
   ```

2. **Create virtual environment**:
  Create virtual environment using tool such as virtualenv.

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py config.yaml
   ```

5. Open your browser and navigate to `http://localhost:8501` to start using JeebBot.

### Running JeebBot in Docker
Follow these steps to set up and run JeebBot locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/witoong623/JeebBot.git
   cd jeebbot
   ```

2. **Build the Docker image**:
   ```bash
   ./scripts/build-prod-image.sh
   ```

3. **Run the Docker Compose**:
   ```bash
   docker compose -f docker/docker-compose.yaml up -d
   ```

4. Open your browser and navigate to `http://localhost:8501` to start using JeebBot.

## Running local LLM
Please read [LOCAL_MODEL_HOSTING.md](LOCAL_MODEL_HOSTING.md) for more detail.

---

## Roadmap

JeebBot is currently under active development. Here's the roadmap:

1. Complete the basic conversation feature. (DONE)
2. Implement bot's characteristic adjustment. (DONE)
3. Add memory capabilities to remember key facts. (DONE)
    1. Make the bot remember key facts automatically.
4. Inject context of conversation such as time, day.
5. Tune prompt or implement time base to initiate conversation from bot first, and to stop when appropriate.
6. Polish the UI for a seamless user experience.
7. Implement infrastructure to evaludate chat experience.
