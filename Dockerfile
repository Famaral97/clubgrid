FROM python:3.10 AS build

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.10

WORKDIR /app

# Copy the dependencies from the first stage
COPY --from=build /usr/local /usr/local

# Copy the rest of the application code
COPY . /app

EXPOSE 5000

ENV FLASK_APP=app.py

CMD alembic upgrade head ; python3 -m flask run --host=0.0.0.0