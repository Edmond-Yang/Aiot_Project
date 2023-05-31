# use the official lightweight Python image
FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./settings/requirements.txt

# Set the environment variable for service account key file path
RUN apt-get update && apt-get install -y curl
RUN curl -o ./cloud_sql_proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.3.0/cloud-sql-proxy.linux.amd64
RUN while [ ! -f /app/cloud_sql_proxy ]; do sleep 1; done
RUN chmod +x cloud_sql_proxy

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/settings/southern-tempo-387713-d30e2f27945c.json"
RUN ./cloud_sql_proxy southern-tempo-387713:asia-east1:sql=tcp:3306 -credential_file=$GOOGLE_APPLICATION_CREDENTIALS &

EXPOSE 8080

CMD  python main.py