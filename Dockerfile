FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --root-user-action=ignore .

CMD ["python3.12", "-u", "app.py"]
