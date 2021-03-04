FROM python:3.8.0-buster
LABEL owner = "Kseniia Glinkina"
RUN apt-get upgrade -y
RUN pip install --upgrade pip
# Make a directory for our application
WORKDIR /app
# Install dependencies
COPY requirements.txt .
COPY config.py .
RUN pip3 install -r requirements.txt
# Copy our source code
COPY app.py .
EXPOSE 5000
# Run the application
ENTRYPOINT  ["python3"]
CMD ["app.py"]



