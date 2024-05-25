FROM python:3.11.4-slim-bookworm
RUN mkdir /mel/; mkdir /bot
COPY . /mel/
RUN python3 -m venv /bot/venv
RUN /bot/venv/bin/python -m pip install --no-cache-dir /mel
CMD [ "/bin/bash" "/bot/start.sh" ]