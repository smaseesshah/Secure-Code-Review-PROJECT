# Methodology & Threat Model

## Threat Model (STRIDE)
To identify the attack surface, I modeled the application against standard threat categories:

* **Spoofing:** Can a user act as someone else? *(Identified weak auth token handling).*
* **Tampering:** Can a user modify data they shouldn't? *(Identified IDOR on task deletion).*
* **Repudiation:** (Not in scope for this minimal lab).
* **Information Disclosure:** Can a user view hidden data? *(Identified SQLi and Hardcoded Secrets).*
* **Denial of Service:** Can a user crash the app? *(Identified missing rate limiting).*
* **Elevation of Privilege:** Can a user gain admin rights? *(Identified XSS for session hijacking).*

## Secure Code Review Approach
My review process followed a "Source to Sink" tracking methodology:

1. **Identify Sources:** Mapped all entry points where user data enters the application (API routes, URL parameters, JSON payloads).
2. **Trace the Data Flow:** Followed the data from the router, to the database controllers, and finally to the frontend rendering logic.
3. **Identify Sinks:** Located dangerous execution points (e.g., `cursor.execute()`, `.innerHTML`).
4. **Verify Mitigation:** Checked if the data was properly encoded, parameterized, or sanitized *before* hitting the sink. 
5. **Defense in Depth:** Even where mitigations existed, I evaluated if architectural safety nets (like CSP) were present in case the primary mitigation failed.

* 🔙 [Return to Global Documentation](README.md)
