FROM python:3.13-trixie
 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env /app/.env

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]




 