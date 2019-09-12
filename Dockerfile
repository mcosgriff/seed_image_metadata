FROM python:3.7.4

COPY run.sh /
COPY app.py /
COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./run.sh"]
