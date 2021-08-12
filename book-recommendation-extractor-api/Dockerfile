FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python3 setup-amazon-api.py install
EXPOSE 5000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]