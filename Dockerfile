FROM python:2.7
MAINTAINER dan.leehr@duke.edu

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client libmysqlclient-dev \
		postgresql-client libpq-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
COPY handoverservice/settings.docker /usr/src/app/handoverservice/settings.py

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
