FROM dash_app_base

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src

COPY . /usr/src/

CMD ["python3", "/usr/src/app.py"]