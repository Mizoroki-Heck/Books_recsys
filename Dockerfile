# Используем Python-образ на базе Debian
FROM python:3.11-buster

# Обновляем пакеты и устанавливаем cron, supervisor
RUN apt-get update && \
    apt-get install -y cron supervisor && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Даем права на выполнение ETL-скрипта
RUN chmod +x /app/utils/ETL.py

# Копируем cron файл в контейнер
COPY ./etl-cron /etc/cron.d/etl-cron

# Даем правильные права для cron файла
RUN chmod 0644 /etc/cron.d/etl-cron

# Копируем скрипт для выполнения
COPY ./utils/ETL.py /ETL.py

# Даем права на выполнение скрипта
RUN chmod +x /ETL.py

# Добавляем cron задачу в crontab
RUN crontab /etc/cron.d/etl-cron

# Открываем порт (если нужно для веб-приложения)
EXPOSE 5000

# Копируем конфиг для supervisord (если используешь supervisor для управления процессами)
COPY supervisord.conf /etc/supervisord.conf

# Запускаем supervisor, чтобы cron запускался в контейнере
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
