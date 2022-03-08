FROM python:3.9

EXPOSE 8000
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn \
    && useradd app \
    && chown -R app:app /app

USER app
COPY --chown=app:app . /app/
WORKDIR /app/cms
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "-w 2", "-b 0.0.0.0:8000", "cms.wsgi", "--timeout", "300"]
