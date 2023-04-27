# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directiory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirement.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose port 5000 for this Flask app
EXPOSE 8080

# Start the Flask app
CMD ["python3", "app.py"]
