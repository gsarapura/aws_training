# Use an official Python runtime as a parent image
FROM python:3.12.3-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY ./lambda_handler.py /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

# Set the entry point to run the scripts
ENTRYPOINT ["python", "lambda_handler.py"]
