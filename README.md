# 📌 ViSoldierQA

---

*ViSoldierQA is an AI assistant capable of providing accurate and reliable answers, explaining concepts, and addressing users' questions related to the military, specifically concerning the Vietnam People's Army.*

---

# 🔍 Why ViSoldierQA?

- Specifically built for the military context of the Vietnam People's Army.

- Offers trustworthy and up-to-date information.

- Provides clear and reliable answers to complex topics.

- Helps users quickly understand military concepts, history, structure, and more.

<p align="center">
<img src="https://i.imgur.com/iz94DjN.png" alt="ViSoldierQA"/>
</p>

# 🗪 Chat with ViSoliderQA

You can quickly review the chat UI below:

<p align="center">
<img src="https://i.imgur.com/AY2I6ay.png" alt="Chat with ViSoldierQA">
</p>

To ask a new question, click on **"Bắt đầu đoạn chat mới"**. You can also continue a previous conversation by clicking on a topic in the sidebar.

# 🛠 What have I done?

- Developed an AI assistant powered by **RAG (Retrieval-Augmented Generation)** using the LangChain framework.

- Crawled, cleaned, and processed military-related documents from official and reliable sources, then stored them in a **Qdrant Cloud** vector database.

- Built a **FastAPI** backend to serve the AI model and stream responses.

- Created a responsive **web interface** with user authentication (login/registration) and real-time chat.

- Integrated a **PostgreSQL** database to manage user information and chat history securely.

## Details

---

## 📃 Data sources

I had crawled various documents from trustworthy and reliable sources:

- <a href="https://mod.gov.vn/home" target="_blank"> Cổng thông tin điện tử Bộ Quốc Phòng </a>

- <a href="https://www.qdnd.vn/" target="_blank"> Báo Quân đội nhân dân </a>

- <a href="https://thuvienphapluat.vn/" target="_blank"> Thư viện pháp luật </a>

- <a href="https://www.bienphong.com.vn/" target="_blank"> Báo Biên Phòng </a>

- Army universities & institutions:

    * <a href="http://daihocchinhtri.edu.vn/" target="_blank"> Trường Đại học Chính Trị </a> 

    * <a href="https://hvannd.edu.vn/" target="_blank"> Học Viện An ninh Nhân Dân </a>

    * Other schools ...
    
The collected documents were:

- Cleaned and chunked

- Converted into vector embeddings using <a href="https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder" target="_blank"> Vietnamese Bi-Encoder </a>

- Stored in a **Qdrant Cloud** vector database for efficient retrieval.


## 💡Technologies Used
- **LangChain**: Orchestrates LLM interactions with the vector database and enables output streaming for smooth UX.

- **Qdrant**: A cloud-based vector database used for fast similarity search and document retrieval.

- **FastAPI**: A high-performance web framework used to build and deploy backend services.

- **PostgreSQL**: Stores user data and chat history efficiently and securely.

# 🔜 What's next?
- In the future, I will implement some improvements for the system:

    *  **Chain-Of-Thought (CoT)**: Enhance the performance of the system by intergrating Chain-of-thought - a technique to enhance the response from the model. 

    * **AutoRAG - AgenticRAG**: The data sources from the database will need to be often upated, or search for external sources in case there is not enough context for the answer. In the near future, I will integrate some agents to enhance the performance.

# 💻 Run the system
- First, install all the dependancies:
```bash
    pip install -r requirements.txt
```

- Host your server:
```bash
  python server.py
```
or 
```bash
  uvicorn app:app
```

- Access the address `http://localhost:8000` to view the results.

- **Important**: 
    
    * Some libraries such as sentence-transformers could be installed with default dependancies (PyTorch, ...). This could lead to an *Conflict Error*, or *Incompatible Device* (Cuda). You should install these dependancies manually.

    * For personal information security, API keys will not be included in this repository. You can create your own keys or adjust the models in ***config/ModelConfig.py***
# ViSoldierQA
