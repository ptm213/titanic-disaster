# Dockerfile (repo root)
# Running this file will create an isolated environment ("image") containing
# all the code and dependencies needed to run the Titanic Disaster analysis.
# On the Docker desktop app, it creates an image called "titanic-disaster" 
# that you can then activate to build a Docker container.

# Use an official lightweight Python image as the base.
FROM python:3.11-slim
 
# Set environment variables to control how Python behaves inside the container.
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the default working directory inside the container.
WORKDIR /app

# Copy the requirements file from your repo into the image.
COPY requirements.txt /app/requirements.txt

# Install the required Python packages.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code folder into the image.
COPY src /app/src

# Specify the default command to run when the container starts.
# This runs the main Python script automatically when someone does "docker run".
CMD ["python", "src/python/main.py"]