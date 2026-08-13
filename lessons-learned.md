# Lessons Learned: The AppSec Mindset

Building and immediately breaking this application provided several key takeaways about modern Application Security.

### 1. Frameworks abstract risk, but don't eliminate it.
Writing Vanilla JavaScript (using `.innerHTML`) immediately exposed how easy it is to introduce XSS. Modern frameworks (React, Vue) protect against this by default using `.textContent` under the hood. However, if a developer explicitly bypasses the framework (e.g., `dangerouslySetInnerHTML`), the exact same vulnerability reappears.

### 2. The Frontend cannot be trusted for security.
In the IDOR vulnerability, the frontend successfully hid the "Delete" button from users who didn't own the task. However, UI logic is not security. Because the backend API did not independently verify ownership, the application remained completely vulnerable to API-level attacks. **Security must always be enforced at the server level.**

### 3. Complexity is the enemy of security.
The SQL Injection occurred because the developer tried to dynamically build a search query string using f-strings, rather than trusting the database driver's built-in parameterization (`?`). Writing "clever" or custom logic for data handling almost always introduces flaws. 

### 4. Defense in Depth is mandatory.
Developers are human and will inevitably make mistakes. Relying solely on input sanitization for XSS is a losing battle. By implementing a strict Content Security Policy (CSP), the application gained a safety net that protects users *even when* a developer writes bad code.

* 🔙 [Return to Global Documentation](README.md)
