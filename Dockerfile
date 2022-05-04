FROM python:3.8-slim AS base

WORKDIR /app
RUN pip install -U pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

###############################
FROM base AS prod
RUN python -m unittest

ENTRYPOINT ["python3"]
CMD ["app.py"]
##############################
FROM base AS dev
ENTRYPOINT ["python3"]
CMD ["app.py"]



