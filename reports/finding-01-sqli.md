# Finding 01: SQL Injection (SQLi)

**Severity:** Critical  
**Affected Component:** `database.py` (`search_tasks` function)

## Description
The application takes user input from the search bar and concatenates it directly into the SQL query string using Python f-strings.

## Root Cause
Lack of parameterization. The database engine cannot distinguish between the developer's intended SQL commands and the user's input.

## Impact
An attacker can manipulate the query structure to dump the entire database (including user credentials) or drop tables entirely.

## Remediation
Replaced the f-string with a parameterized query:
`cursor.execute("SELECT * FROM tasks WHERE title LIKE ?", (f"%{search_term}%",))`

## Retest Result
✅ **Fixed** - The database now correctly treats the input as literal text, neutralizing payloads.
