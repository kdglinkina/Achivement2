FROM ubuntu:latest
LABEL owner = "Kseniia Glinkina"
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential
# Make a directory for our application
WORKDIR /app
COPY requirements.txt .
# Install dependencies
RUN pip3 install -r requirements.txt
# Copy our source code
COPY . /app
EXPOSE 5000
# Run the application
ENTRYPOINT  ["python3"]
CMD ["app.py"]
