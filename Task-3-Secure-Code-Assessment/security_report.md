# Secure Code Assessment Report

## 1. Introduction

This project performs a security assessment of a Python user management
application.

Two versions are included:

- vulnerable_app.py - intentionally insecure version
- secure_app.py - corrected version

The purpose is to demonstrate common security weaknesses and secure
coding practices.

---

## 2. Technologies

- Python 3
- SQLite
- Python Standard Library

---

## 3. Vulnerabilities Identified

### 3.1 SQL Injection

**Severity:** High

The vulnerable application creates SQL queries using string formatting.

Example:

```python
query = f"""
SELECT id, username, role
FROM users
WHERE username = '{username}'
"""