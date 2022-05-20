# syntax=docker/dockerfile:1

FROM python:3.7.8

WORKDIR /roomnode

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


# Add this:
ENV FLASK_APP=main.py

# either production or development (defaults to development if empty...)
ENV pfIBM-mode=production

CMD [ "python", "./main.py" ]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]