FROM python:3.9-slim

WORKDIR /st
COPY requirements.txt /st
RUN pip install -r requirements.txt

COPY . /st

EXPOSE 8501
CMD ["streamlit", "run", "app.py",  "--server.port=8501"]
