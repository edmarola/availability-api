FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /api

# Create and activate venv.
RUN python3 -m venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install the requirements.
COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy and install the project.
COPY . .
RUN pip install .

RUN cp .env.example .env

EXPOSE 8000

CMD gunicorn --bind=0.0.0.0:8000 "availapi:app"