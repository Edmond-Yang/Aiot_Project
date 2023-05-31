# use the official lightweight Python image
FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && apt-get install -y curl

# Allow statements and log messages to immediately appear in Knative logs
ENV PYTHONUNBUFFERED True

# Set the environment variable for service account key file path
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/settings/southern-tempo-387713-d30e2f27945c.json"


RUN curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.3.0/cloud-sql-proxy.linux.amd64

RUN chmod +x cloud_sql_proxy

RUN pip install --no-cache-dir -r ./settings/requirements.txt

EXPOSE 8080

CMD ./cloud_sql_proxy -instances=southern-tempo-387713:asia-east1:sql=tcp:3306 -credential_file=$GOOGLE_APPLICATION_CREDENTIALS & python main.py