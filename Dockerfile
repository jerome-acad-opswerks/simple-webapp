FROM python:3.12.8

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", ":8000", "app:app"]
