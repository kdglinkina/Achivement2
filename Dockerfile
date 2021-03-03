FROM python:3.8.0-buster
LABEL owner = "Kseniia Glinkina"
RUN apt-get upgrade -y
RUN pip install --upgrade pip
# Make a directory for application
#WORKDIR /application
# Install dependencies
COPY requirements.txt .
COPY config.py .
COPY ./templates.templates
RUN pip install -r requirements.txt
# Copy source code
COPY /app.py .
EXPOSE 5000
ENTRYPOINT  ["python3"]
# Run the application
CMD ["app.py"]



