FROM python:rc-buster

COPY entrypoint.sh /entrypoint.sh
COPY data.csv /data.csv
RUN bash -c "chmod +x /entrypoint.sh && python -m pip install boto3"

ENTRYPOINT ["/entrypoint.sh"] 
