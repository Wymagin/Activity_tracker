# Use an official Python runtime as a parent image
FROM python:3.12.7

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]