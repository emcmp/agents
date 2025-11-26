# Use a slim Python base image for smaller size
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy the requirements file and install dependencies using uv
# Assuming requirements.txt is in the same directory as Dockerfile
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This includes crew.py, and the config directory
COPY . .

# Set default environment variables for LLM configuration.
# These can be overridden at runtime using 'docker run -e VAR_NAME=value'.
ENV LLM_PROVIDER=OPENAI
ENV OPENAI_MODEL=gpt-4o
ENV GEMINI_MODEL=gemini-1.5-pro

# Command to run the CrewAI application
# The crew.py is the main entry point to initiate the crew.
# The crew.py might contain the logic to run the crew (e.g., crew.kickoff()).
# Assuming crew.py is set up to run the crew when executed directly.
CMD ["python", "crew.py"]