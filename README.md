# 🚀 OmniDesk – Multi-Agent AI System

OmniDesk is an AI-powered productivity assistant that uses a **multi-agent architecture** to manage tasks, calendar events, and notes. It leverages **Google Gemini (Vertex AI)** along with **FastAPI** and **Firestore** to provide intelligent, conversational automation.

---

## 🧠 Features

- Multi-agent system (Task, Calendar, Notes)
- Natural language interaction
- Task management (create, update, delete, list)
- Calendar scheduling
- Note creation and search
- Multi-step workflow execution
- Firestore database integration
- Deployed as an API using Google Cloud Run

---

## 🏗️ Architecture

User Input  
↓  
Orchestrator Agent  
↓  
Task Agent | Calendar Agent | Notes Agent  
↓  
Tool Layer (MCP-style)  
↓  
Firestore Database  
↓  
Response to User  

---

## ⚙️ Tech Stack

- Backend: FastAPI  
- AI Model: Gemini 2.5 Flash (Vertex AI)  
- Database: Google Firestore  
- Deployment: Google Cloud Run (Docker)  
- Frontend: HTML, CSS, JavaScript  

---

## 📂 Project Structure

omnidesk/

├── agents/              # AI agents (task, calendar, notes, orchestrator)  
├── tools/               # Firestore + MCP tools  
├── frontend/            # UI files  
├── main.py              # FastAPI app  
├── requirements.txt  
├── Dockerfile  
└── README.md  

---

## 🚀 How It Works

1. User sends a natural language request  
2. Orchestrator decides which agent(s) to use  
3. Agents call tools (MCP-style)  
4. Tools interact with Firestore  
5. Response is returned to the user  

---

## 🧪 Example Prompts

Create a task "Finish AI report" with high priority due 2025-04-10  

Schedule a meeting "Project discussion" on 2025-04-09 at 5 PM  

Create a note titled "Ideas" with content "Discuss architecture"  

Mark my task "Finish AI report" as completed  

Show me all my tasks  

---

## 🔄 Multi-Step Workflow Example

Create a task "Prepare slides"  
Schedule a meeting "Team sync" tomorrow at 6 PM  
Then mark the task as completed and delete the event  
Show everything  

---

## 🛠️ Setup (Local)

git clone https://github.com/your-username/omnidesk-ai.git  
cd omnidesk  

pip install -r requirements.txt  

uvicorn main:app --reload  

---

## 🧩 Requirements Covered

- Primary orchestrator agent  
- Multiple sub-agents  
- MCP-style tool integration  
- Firestore database usage  
- Multi-step workflows  
- API-based deployment  


## 🌟 Future Improvements

- User authentication  
- Persistent memory   
- Notifications and reminders  
