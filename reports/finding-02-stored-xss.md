# Finding 02: Stored Cross-Site Scripting (XSS)

**Severity:** High  
**Affected Component:** `static/app.js` (`displayComments` function)

## Description
User comments are fetched from the database and injected directly into the DOM using the `.innerHTML` property without any prior sanitization or encoding. 

## Root Cause
Use of a dangerous sink (`.innerHTML`) combined with a lack of contextual output encoding.

## Impact
If an attacker submits a comment containing malicious JavaScript (e.g., `<script>`), the browser assumes it is legitimate code and executes it when other users view the task. This can lead to session hijacking, defacement, or forced actions.

## Remediation: The 3 Levels of Defense
To ensure this vulnerability is eradicated and cannot easily return, I implemented a 3-tiered Defense in Depth strategy:

### Level 1: Context-Aware Encoding (The Fix)
The first step is neutralizing the data before it touches the DOM. If a developer *must* use `.innerHTML` to render formatting, they must pass the untrusted input through an encoding library (like `he.js`) first.
*   **Action:** `he.encode("<script>")` converts the payload to `&#x3C;script&#x3E;`, rendering it harmless.

### Level 2: Enforce Safe Sinks (The Architecture)
Instead of relying on developers to remember Level 1, we altered the frontend architecture to ban `.innerHTML` entirely for user data.
*   **Action:** Replaced `.innerHTML` with `document.createTextNode()` and `.textContent`. These native DOM APIs automatically treat all input as flat text, making XSS mathematically impossible in this context.

### Level 3: Content Security Policy (The Safety Net)
If a future developer ignores Level 2 and forgets Level 1, we need a server-side safety net. 
*   **Action:** Configured Flask's `after_request` to inject a strict CSP header: `Content-Security-Policy: default-src 'self'; script-src 'self'`. This tells the browser to strictly block any inline `<script>` tags, instantly killing any payload that slips through the JavaScript defenses.

## Retest Result
✅ **Fixed** - Payloads are now rendered safely as text via Level 2, and the CSP actively monitors the browser via Level 3.

* 🔙 [Return to Global Documentation](../README.md)