# Secure Code Review Lab: TaskVault

A practical AppSec case study demonstrating real-world vulnerabilities, secure code remediation, and verification testing.

## 📌 Project Overview
This repository contains two parallel versions of **TaskVault** (a simple Flask task-management app):
1. **Vulnerable Version:** Contains deliberate security flaws for code review, exploitation, and threat modeling.
2. **Secure Version:** Implements production-grade fixes, secure architecture, and defense-in-depth safety nets.

## 🚀 Quick Start (Single Command)
You can run both versions simultaneously and access them through a central browser hub.

```bash
python run_lab.py
```

* **Central Hub:** [http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)
* **Vulnerable App:** [http://127.0.0.1:3000](https://www.google.com/search?q=http://127.0.0.1:3000)
* **Secure App:** [http://127.0.0.1:4000](https://www.google.com/search?q=http://127.0.0.1:4000)

---

## 📚 Documentation Map

I have documented the entire lifecycle of finding, exploiting, and fixing these vulnerabilities. Explore the lab using the links below:

### 🏗️ The AppSec Mindset (Start Here)

* 🎯 **[Threat Model & Attack Surface](https://www.google.com/search?q=./threat-model.md)** - A STRIDE analysis mapping out what we need to protect and how it can be attacked.
* 🧠 **[Review Methodology](https://www.google.com/search?q=./methodology.md)** - My "Source to Sink" approach to hunting bugs in the codebase.
* 💡 **[Lessons Learned](https://www.google.com/search?q=./lessons-learned.md)** - Key takeaways on why modern apps still fail and the importance of defense-in-depth.

### 💻 The Lab Environments

* ⚙️ **[Setup Guide](https://www.google.com/search?q=./setup.md)** - Step-by-step installation instructions.
* 🚩 **[Vulnerable App Docs](https://www.google.com/search?q=./vulnerable-app/README.md)** - Exploring the intentionally flawed architecture.
* 🛡️ **[Secure App Docs](https://www.google.com/search?q=./secure-app/README.md)** - How the defense mechanisms and CSP safety nets were implemented.

### 📋 Security Finding Reports

Read the detailed breakdowns, root causes, and remediations for each vulnerability:

* 🕷️ [Finding 01: SQL Injection (SQLi)](https://www.google.com/search?q=./reports/finding-01-sqli.md)
* 🕷️ [Finding 02: Stored Cross-Site Scripting (XSS)](https://www.google.com/search?q=./reports/finding-02-stored-xss.md)
* 🕷️ [Finding 03: Insecure Direct Object Reference (IDOR)](https://www.google.com/search?q=./reports/finding-03-missing-authorization.md)
* 🕷️ [Finding 04: Hardcoded API Secret](https://www.google.com/search?q=./reports/finding-04-hardcoded-secret.md)
* 🕷️ [Finding 05: Weak Password Cryptography](https://www.google.com/search?q=./reports/finding-05-weak-password-hashing.md)
