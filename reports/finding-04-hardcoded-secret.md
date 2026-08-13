# Finding 04: Hardcoded API Secret

**Severity:** Medium  
**Affected Component:** `app.py` (Global variables)

## Description
A third-party API key (`SENDGRID_API_KEY`) is stored as a plaintext string directly in the source code.

## Root Cause
Improper secrets management.

## Impact
If the codebase is pushed to a repository (even a private one), the secret is exposed in the commit history, allowing attackers to abuse the third-party service at the company's expense.

## Remediation
Removed the hardcoded string. Implemented `python-dotenv` to load the secret from a local `.env` file, and added `.env` to `.gitignore`.

## Retest Result
✅ **Fixed** - Codebase is clean and secrets are isolated from version control.
