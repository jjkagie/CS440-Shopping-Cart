FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --break-system-packages requests
RUN pip install mysql-connector-python
COPY . .
EXPOSE 5004
CMD ["python", "cart.py"]