# TaskVault (Vulnerable Version) 🚩

This directory contains the vulnerable version of the application (runs on **Port 3000**).

## 🎯 Target Vulnerabilities
This version was designed to showcase five core application flaws:
1. **SQL Injection:** Raw query concatenation in `database.py`.
2. **Stored XSS:** Unsanitized `.innerHTML` rendering in `app.js`.
3. **IDOR:** Unchecked task deletion endpoint in `app.py`.
4. **Hardcoded Secrets:** API key declared inline in `app.py`.
5. **Weak Cryptography:** MD5 password hashing without salts.

## 🔗 Quick Links
* 🔙 [Return to Global Documentation](../README.md)
* 🛡️ [View the Secure Version Documentation](../secure-app/README.md)
* 📋 [Read the Vulnerability Audit Reports](../reports/)