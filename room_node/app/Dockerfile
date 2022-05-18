# syntax=docker/dockerfile:1

FROM python:3.7.8

WORKDIR /tododocker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
# Add this:
ENV FLASK_APP=room_logic.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]