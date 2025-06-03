# Dockerfile
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update && apt install -y cron

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt 

COPY . .

COPY cronjob /etc/cron.d/generate_invoices
RUN chmod 0644 /etc/cron.d/generate_invoices && \
    crontab /etc/cron.d/generate_invoices

# Asegurate de que el archivo de log exista
RUN touch /var/log/cron.log

# Comando para ejecutar cron en primer plano (necesario para contenedor Docker)
CMD ["cron", "-f"]