# stage1 as builder
FROM node:alpine as builder

# copy the package.json to install dependencies
COPY ./frontend/package.json ./frontend/package-lock.json ./

# Install the dependencies and make the folder
RUN npm install && mkdir /nextjs-ui && mv ./node_modules ./nextjs-ui

WORKDIR /nextjs-ui

COPY ./frontend/ .

# Build the project and copy the files
RUN npm run build


# FROM nginx:alpine

# #!/bin/sh


# COPY ./frontend/.nginx/nginx.conf /etc/nginx/nginx.conf

# ## Remove default nginx index page
# RUN rm -rf /usr/share/nginx/html/*

# # Copy from the stahg 1
# COPY --from=builder /nextjs-ui/out /usr/share/nginx/html/

# EXPOSE 3000 80

# ENTRYPOINT ["nginx", "-g", "daemon off;"]

# Use an official Python runtime as the base image
FROM ubuntu


RUN apt-get update && apt-get upgrade -y 
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt install nginx -y
COPY .nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /nextjs-ui/out /usr/share/nginx/html/
ENV PORT=80

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./python .

# Install the necessary dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the application code into the container

RUN chmod +x ./server.sh
# Set the environment variable for Flask
ENV FLASK_APP=flask_app.py
# ENTRYPOINT ["nginx", "-g", "daemon off;"]
# CMD ["flask", "run", "--host=0.0.0.0"]

# Run the Flask application
CMD ["./server.sh"]
