FROM openjdk:slim
COPY --from=python:3 / /

WORKDIR /usr/src/app

# Prepare Minecraft - Matrix bridge
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# # Prepare MC server
# COPY server.jar ./
# RUN java -jar server.jar --nogui

COPY src/ ./src/
COPY main.py ./

COPY LICENSE.md ./
COPY config.yaml ./

# Buffer Python's stdout for debugging during runtime
ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
