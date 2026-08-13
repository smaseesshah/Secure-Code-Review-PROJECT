# Lab Setup & Execution Guide

Follow these steps to run the complete environment locally.

## Prerequisites

* Python 3.8+ installed.

## Step 1: Install Dependencies

Open your terminal in the root directory and run:

```bash
pip install flask python-dotenv requests
```

## Step 2: Configure Environment Variables

Inside the `secure-app/` folder, create a file named `.env` and add:

```text
SENDGRID_API_KEY=sg-secret-key-987654321-taskvault
```

## Step 3: Run the Lab

From the root directory, launch the dashboard:

```bash
python run_lab.py
```

A browser window will open automatically, allowing you to easily click between the vulnerable and secure apps.


* 🔙 [Return to Global Documentation](README.md)