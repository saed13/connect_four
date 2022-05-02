FROM python:3.8-slim AS base

WORKDIR /app
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

###############################
FROM base AS prod
RUN python -m unittest

CMD python user_interface/RunGame.py
##############################
FROM base AS dev
CMD python user_interface/RunGame.py



