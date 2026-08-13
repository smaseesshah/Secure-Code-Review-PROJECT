# TaskVault (Vulnerable Version) 🚩

**TaskVault** is a deliberately vulnerable team task management application built with Python/Flask, SQLite, and Vanilla JavaScript. 

It is designed to serve as a practical lab environment for learning Application Security (AppSec) and practicing secure code review methodologies. This version of the application contains several critical security flaws intentionally baked into its architecture.

---

## 🎯 Lab Objectives

The primary goal of this environment is to successfully identify, exploit, and document the following core vulnerabilities:

1.  **SQL Injection (SQLi)**
2.  **Stored Cross-Site Scripting (XSS)**
3.  **Insecure Direct Object Reference (IDOR / BOLA)**
4.  **Hardcoded Secrets/Credentials**
5.  **Weak Cryptography (Password Hashing)**

*Note: While these are the primary intended flaws, the application may contain other unintentional vulnerabilities typical of rapid prototyping.*

---

## 🏗️ Architecture & Stack

To ensure the vulnerabilities are transparent and easy to trace from the UI down to the database, the application avoids complex ORMs or frontend frameworks.

*   **Backend:** Python 3.x with Flask (RESTful API)
*   **Database:** SQLite3 (Raw SQL Queries)
*   **Frontend:** Vanilla HTML5, CSS3, and JavaScript (ES6)
*   **Communication:** JSON payloads via Fetch API

---

## 🚀 Setup & Installation

Follow these steps to initialize the lab environment locally.

### Prerequisites
*   Python 3.8+ installed on your system.
*   Basic understanding of command-line operations.

### Installation Steps

1.  **Navigate to the vulnerable app directory:**
    ```bash
    cd vulnerable-app
    ```

2.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the application:**
    ```bash
    python app.py
    ```
    *The application will automatically detect that the database is missing and initialize `taskvault.db` on its first run.*

4.  **Access the application:**
    Open your web browser and navigate to: 
    [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

## 🗺️ Application Attack Surface

This section outlines the key workflows of the application to aid in threat modeling and exploitation.

| Feature | Description | Related Files |
| :--- | :--- | :--- |
| **Authentication** | Users can register and log in to receive an authorization token (simulated via header). | `login.html`, `register.html`, `app.py (/api/register, /api/login)` |
| **Task Management** | Authenticated users can create tasks and view a dashboard of all tasks on the platform. | `dashboard.html`, `app.py (/api/tasks)` |
| **Search Functionality**| Users can search for tasks by keyword against the database. | `dashboard.html`, `database.py (search_tasks)` |
| **Task Deletion** | Users can delete tasks from the dashboard. The UI attempts to restrict this to task owners. | `app.js (deleteTask)`, `app.py (DELETE /api/tasks/<id>)` |
| **Comments System** | Users can view task details and post comments that are visible to all users. | `task.html`, `app.py (/api/tasks/<id>/comments)` |

