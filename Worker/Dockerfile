FROM python:3.10.6
ENV PYTHONUNBUFFERED True
WORKDIR /worker
COPY main.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","main.py"]