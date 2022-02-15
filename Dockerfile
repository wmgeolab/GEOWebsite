FROM nikolaik/python-nodejs:python3.9-nodejs16

EXPOSE 8000
COPY requirements.txt /app/requirements.txt
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn \
    && useradd app \
    && chown -R app:app /app
RUN npm install
USER app
COPY --chown=app:app . /app/
RUN npx webpack
WORKDIR /app/cms
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "-w 2", "-b 0.0.0.0:8000", "cms.wsgi", "--timeout", "300"]
