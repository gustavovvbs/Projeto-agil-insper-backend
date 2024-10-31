FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["gunicorn", "app/run.py:app", "-b", "0.0.0.0:5000", "-w", "4", "--reload"]