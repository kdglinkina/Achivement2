FROM python:3.8
LABEL owner = "Kseniia Glinkina"
RUN apt-get upgrade -y python3-pip python-dev
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT  ["python3"]
CMD ["app.py"]