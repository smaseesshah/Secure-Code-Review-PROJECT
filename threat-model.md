# Threat Model & Attack Surface

Before diving into the code, I modeled the TaskVault application to understand its attack surface and potential risks.

## Assets
What are we trying to protect?
*   **User Credentials:** Passwords stored in the database.
*   **Application Data:** Task titles and private comments.
*   **Third-Party Access:** The SendGrid API key used for notifications.
*   **Server Integrity:** Preventing unauthorized code execution on the host.

## Threat Assessment (STRIDE)
I evaluated the application against the STRIDE threat model:

| Threat | Definition | Findings in TaskVault |
| :--- | :--- | :--- |
| **Spoofing** | Pretending to be someone else. | The "Bearer token" system blindly trusts the provided username header, allowing instant impersonation. |
| **Tampering** | Modifying data maliciously. | An **IDOR** vulnerability allows any user to delete tasks belonging to others via the API. |
| **Repudiation** | Claiming you didn't do something. | The app lacks audit logging for task deletions. |
| **Information Disclosure**| Exposing sensitive data. | **SQL Injection (SQLi)** in the search bar allows attackers to dump the entire database. A **Hardcoded API Key** exposes third-party billing. |
| **Denial of Service** | Taking the application offline. | Lack of rate limiting on the `/login` route allows brute-force attacks. |
| **Elevation of Privilege**| Gaining higher access. | **Stored XSS** allows an attacker to execute scripts in another user's browser, potentially hijacking their session. |

* 🔙 [Return to Global Documentation](../README.md)