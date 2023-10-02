FROM openjdk:slim

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /usr/src/app

# Prepare Minecraft - Matrix bridge
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main.py ./

# Buffer Python's stdout for debugging during runtime
ENV PYTHONUNBUFFERED=1

CMD ["python3", "main.py"]
