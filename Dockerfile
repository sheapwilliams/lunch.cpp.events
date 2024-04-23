FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY migrations migrations
COPY lunch.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP lunch.py
#RUN flask translate compile

EXPOSE 5001
ENTRYPOINT ["./boot.sh"]