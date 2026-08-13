# TaskVault (Secure Version) 🛡️

This directory contains the fully remediated version of the application (runs on **Port 4000**).

## 🛡️ Implemented Defenses
1. **Parameterized SQL Queries:** Neutralized SQLi using SQLite tuple parameterization.
2. **Context-Aware Encoding & Safe Sinks:** Replaced `.innerHTML` with `.textContent` to stop XSS.
3. **Content Security Policy (CSP):** Configured strict HTTP headers to block inline scripts as a Layer-4 safety net.
4. **Backend Authorization:** Added owner checks before executing deletion queries (IDOR fix).
5. **Modern Hashing:** Upgraded to Werkzeug salted password hashing (PBKDF2).
6. **Environment Secrets:** Loaded sensitive API keys using `python-dotenv`.

## 🔗 Quick Links
* 🔙 [Return to Global Documentation](../README.md)
* 🚩 [View the Vulnerable Version Documentation](../vulnerable-app/README.md)
* 📋 [Read the Vulnerability Audit Reports](../reports/)