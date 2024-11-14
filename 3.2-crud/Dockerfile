FROM python:3

WORKDIR /stocks_products

COPY ./stocks_products /stocks_products 

RUN pip install -r /stocks_products/requirements.txt

RUN python manage.py migrate

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]

