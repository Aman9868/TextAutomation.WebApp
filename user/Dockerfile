FROM python:3.9
COPY . /user/routes
WORKDIR /user/routes
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind