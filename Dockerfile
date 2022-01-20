FROM python:3.9

WORKDIR /app

COPY utils utils
COPY monte_carlo.py monte_carlo.py
COPY solvers solvers
COPY game game
COPY config/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "monte_carlo.py"]
