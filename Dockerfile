FROM python:3.10.10-bullseye

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./banking
WORKDIR /banking
EXPOSE 5000
CMD [ "python3", "app.py"]
