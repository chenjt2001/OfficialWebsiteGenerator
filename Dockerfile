FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
EXPOSE 5000
CMD ["uwsgi", "-i", "uwsgi.ini"]
