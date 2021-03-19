FROM python:3.8

RUN apt update && apt install -y libffi-dev libnacl-dev python3-dev
RUN python3 -m pip install -U discord.py

RUN mkdir /cah
WORKDIR /cah

COPY main.py /cah/
COPY white.txt /cah/
COPY black.txt /cah/
COPY token.txt /cah/
CMD ["python", "main.py"]
