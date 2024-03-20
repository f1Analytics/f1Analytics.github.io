# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app
COPY app.py /app
COPY data_engine /app/data_engine

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV STREAMLIT_SERVER_PORT=8000

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
