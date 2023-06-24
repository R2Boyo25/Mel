FROM python:3.11.4-slim-bookworm
RUN mkdir /mel/; mkdir /bot
COPY . /mel/
RUN DEBIAN_FRONTEND=noninteractive apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-venv
RUN python3 -m venv /bot/venv
RUN /bot/venv/bin/python -m pip install --no-cache-dir -r /mel/requirements.txt.example
CMD python3 /mel/bot.py /bot