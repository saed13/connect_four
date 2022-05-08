FROM python:3.8-slim AS base

WORKDIR /app
RUN pip3 install -U pip

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

###############################
FROM base AS prod
#RUN python3 -m behave features
RUN python3 -m unittest

ENTRYPOINT ["python3"]
CMD ["app.py"]




