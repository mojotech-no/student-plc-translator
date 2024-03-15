FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --root-user-action=ignore .
RUN pip install customtkinter
CMD ["python3.12", "-u", "app.py"]
