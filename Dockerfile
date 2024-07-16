# Use an official TensorFlow runtime as a parent image
#FROM tensorflow/tensorflow:latest 


# Set base image (host OS)
#FROM python:3.10-slim-buster 
#-alpine

# By default, listen on port 5000
#EXPOSE 5000/tcp

# Set the working directory in the container
#WORKDIR /app

# Copy the dependencies file to the working directory
#COPY requirements.txt .

# Install any dependencies
#RUN pip install -r requirements.txt

# Install any dependencies
# Install any dependencies
#RUN pip install --upgrade pip && pip install -r requirements.txt

# Install TensorFlow
#RUN pip install tensorflow


# Copy the content of the local src directory to the working directory
#COPY app.py .

# Specify the command to run on container start
#CMD [ "python", "./app.py" ]

# Set base image (host OS)
FROM python:3.10-slim-buster

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libhdf5-dev \
        pkg-config

# Copy the dependencies file to the working directory
COPY requirements.txt .

#COPY SGModelBIN.hdf5 .

#COPY templates .

#COPY index2.html .
#COPY success.html .
#COPY static .

COPY . .

# Install any dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install TensorFlow
RUN pip install tensorflow

# Copy the content of the local src directory to the working directory
COPY app.py .

# Specify the command to run on container starts
CMD ["flask", "run", "--host", "0.0.0.0"]
# "python", "./app.py" 
#"gunicorn", "-b", "0.0.0.0:5000", "app:app"