# Module 6: Deploy Anywhere

> **Course:** JHU EP 605.256 – Modern Software Concepts in Python  
> **Assignment:** Dockerize and deploy your Module 1 Flask personal website so it can run anywhere.

---
## Link to Dockerhub Repository

https://hub.docker.com/r/pjroelofsen/module_6/tags

## Overview

This repository contains your Flask personal website from Module 1, now fully containerized with Docker. You will be able to:

- Build a Docker image based on **python:3.10**  
- Run the site in a container on port **8080**  
- Lint your Python code to **pylint 10/10**  
- Push the resulting image to Docker Hub for sharing

---

## Prerequisites

- **Python 3.10+** (for local development & linting)  
- **Docker** (Docker Desktop on macOS/Windows or Docker Engine on Linux)  
- A **Docker Hub** account and a public repository named `module_6`

---

## Repository Structure

```text
module_6/
├── app/                  # Your Flask package
│   ├── __init__.py
│   └── routes/
│       └── main.py
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build instructions
└── README.md             # ← you are here
