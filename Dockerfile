FROM python:3.8.0-buster
LABEL owner = "Kseniia Glinkina"
RUN apt-get upgrade -y
RUN pip install --upgrade pip
#python-pip python-dev
# Make a directory for our application
WORKDIR /application
# Install dependencies
COPY requirements.txt .
COPY config.py .
RUN pip install -r requirements.txt
# Copy our source code
COPY /app.py .
EXPOSE 5000
ENTRYPOINT  ["python3"]
# Run the application
CMD ["app.py"]



