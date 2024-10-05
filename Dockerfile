FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . .

EXPOSE 8000

CMD ["/wait-for-it.sh", "db_pokemon:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
