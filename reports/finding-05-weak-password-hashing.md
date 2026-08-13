# Finding 05: Weak Password Cryptography

**Severity:** Critical  
**Affected Component:** `app.py` (`/api/register` and `/api/login`)

## Description
User passwords are hashed using the MD5 algorithm without any cryptographic salt.

## Root Cause
Use of an outdated, fast hashing algorithm designed for file integrity, not password storage.

## Impact
If the database is leaked, attackers can use Rainbow Tables or brute-force tools (like Hashcat) to crack the hashes almost instantly, leading to full account takeovers.

## Remediation
Replaced MD5 with Flask's built-in `werkzeug.security` module. Passwords are now hashed using PBKDF2/scrypt with automatic, unique salting for every user.

## Retest Result
✅ **Fixed** - Hashes are now secure, unique, and computationally expensive to crack.


* 🔙 [Return to Global Documentation](../README.md)