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

* **Central Hub:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Vulnerable App:** [http://127.0.0.1:3000](http://127.0.0.1:3000)
* **Secure App:** [http://127.0.0.1:4000](http://127.0.0.1:4000)

---

## � Application Screenshots

These screenshots capture the key user flows and the vulnerable vs. fixed behaviors in the lab.

### Main app views

![Main Landing Page](./Screenshot/Main%20Landing%20Page.png)

![Login Page](./Screenshot/Login%20Page.png)

### Vulnerable vs. secure findings

![SQLi in Vulnerable Version](./Screenshot/SQLi%20in%20Vulnerable%20Version.png)

![SQLi Fixed in Secure Version](./Screenshot/SQLi%20Fixed%20in%20Secure%20Version.png)

![XSS in Vulnerable App Version](./Screenshot/XSS%20in%20Vulnerable%20App%20Version.png)

![XSS Fixes in Secure App Version](./Screenshot/XSS%20Fixes%20in%20Secure%20App%20Version.png)

![IDOR in Vulnerable Version](./Screenshot/IDOR%20in%20Vulnerable%20Version.png)

![IDOR Fixed in Secure Version](./Screenshot/IDOR%20Fixed%20in%20Secure%20Version.png)

---

## �📚 Documentation Map

I have documented the entire lifecycle of finding, exploiting, and fixing these vulnerabilities. Explore the lab using the links below:

### 🏗️ The AppSec Mindset (Start Here)

* 🎯 **[Threat Model & Attack Surface](./threat-model.md)** - A STRIDE analysis mapping out what we need to protect and how it can be attacked.
* 🧠 **[Review Methodology](./methodology.md)** - My "Source to Sink" approach to hunting bugs in the codebase.
* 💡 **[Lessons Learned](./lessons-learned.md)** - Key takeaways on why modern apps still fail and the importance of defense-in-depth.

### 💻 The Lab Environments

* ⚙️ **[Setup Guide](./setup.md)** - Step-by-step installation instructions.
* 🚩 **[Vulnerable App Docs](./vulnerable-app/README.md)** - Exploring the intentionally flawed architecture.
* 🛡️ **[Secure App Docs](./secure-app/README.md)** - How the defense mechanisms and CSP safety nets were implemented.

### 📋 Security Finding Reports

Read the detailed breakdowns, root causes, and remediations for each vulnerability:

* 🕷️ [Finding 01: SQL Injection (SQLi)](./reports/finding-01-sqli.md)
* 🕷️ [Finding 02: Stored Cross-Site Scripting (XSS)](./reports/finding-02-stored-xss.md)
* 🕷️ [Finding 03: Insecure Direct Object Reference (IDOR)](./reports/finding-03-missing-authorization.md)
* 🕷️ [Finding 04: Hardcoded API Secret](./reports/finding-04-hardcoded-secret.md)
* 🕷️ [Finding 05: Weak Password Cryptography](./reports/finding-05-weak-password-hashing.md)
