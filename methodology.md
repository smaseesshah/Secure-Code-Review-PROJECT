# Methodology

## Secure Code Review Approach
My review process followed a "Source to Sink" tracking methodology:

1. **Identify Sources:** Mapped all entry points where user data enters the application (API routes, URL parameters, JSON payloads).
2. **Trace the Data Flow:** Followed the data from the router, to the database controllers, and finally to the frontend rendering logic.
3. **Identify Sinks:** Located dangerous execution points (e.g., `cursor.execute()`, `.innerHTML`).
4. **Verify Mitigation:** Checked if the data was properly encoded, parameterized, or sanitized *before* hitting the sink. 
5. **Defense in Depth:** Even where mitigations existed, I evaluated if architectural safety nets (like CSP) were present in case the primary mitigation failed.

* 🔙 [Return to Global Documentation](README.md)
