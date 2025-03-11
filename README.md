# Video-DAG
An assignment on the extraction of Youtube videos based on topics and storage of data to MongoDB with the assistance of Airflow and DAGs.

# 🎥 Video Data Pipeline with Apache Airflow & MongoDB

## 📖 Overview
This project implements a **data pipeline using Apache Airflow**, where:
1. **YouTube video data** is fetched via the YouTube API.
2. The data is **stored as JSON** in a mounted `data/` folder.
3. The JSON data is **inserted into MongoDB** collections.
4. The project is **fully containerized using Docker & Docker Compose**.

This allows easy scheduling, automation, and storage of video-related metadata.

---

## 🚀 Features
✅ **Apache Airflow DAG Workflow**  
✅ **MongoDB for NoSQL Storage**  
✅ **Dockerized for Easy Deployment**  
✅ **YouTube API Integration**  
✅ **Automated Data Processing & Storage**  

---

## 🔧 **Setup & Installation**

### **1️⃣ Prerequisites**
- **Install [Docker](https://www.docker.com/)**
- **Install [MongoDB Compass](https://www.mongodb.com/try/download/compass)** (for database viewing)
- **Create a YouTube API Key** from [Google Developer Console](https://console.developers.google.com/)

---

### **2️⃣ Clone the Repository**
git clone https://github.com/Dawntwister/Video-DAG.git
cd Video-DAG

---

### **3️⃣ Configure YouTube API Key (dags/.env)**
Create a new .env file inside the dags/ folder:
touch dags/.env
Then, open it and add:
YOUTUBE_API_KEY=your-api-key-here
✅ This ensures the YouTube API key is not exposed in code.

---

### **4️⃣ Start the Docker Containers**
docker-compose up -d --build

---

### **5️⃣Connection in MongoDB Compass**
Add a connection instance:
URI: mongodb://root:example@localhost:27017/

---

### **6️⃣ Access the Web Interfaces**
Apache Airflow UI:	http://localhost:8080
Go to Airflow UI to run the DAG
---

## **📜 License**
This project is licensed under the **Apache License 2.0**.  
See the [LICENSE](LICENSE) file for details.
