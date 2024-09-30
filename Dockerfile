FROM python:3.11.0-slim
WORKDIR /app
COPY . /app
RUN apt update && apt install -y gcc
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit", "run", "app.py"]