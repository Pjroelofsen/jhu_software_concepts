# module_6/Dockerfile

# 1) Use python:3.10 as the base image
FROM python:3.10

# 2) Set the working directory
WORKDIR /app

# 3) Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the rest of your module_6 application code
COPY . .

# 5) Expose port 8080 for your Flask app
EXPOSE 8080

# 6) (Optional) Ensure Flask runs on all interfaces
#    Only needed if run.py uses flask run without host override.
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# 7) Start your Flask application
CMD ["python", "run.py"]
