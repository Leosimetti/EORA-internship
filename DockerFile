FROM python:3.8

COPY ./requirements.txt /
COPY ./app /app/
COPY ./main.py /
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python3", "main.py"]