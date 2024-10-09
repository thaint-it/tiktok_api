# Pull base image
FROM python:3.11

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY ./requirements.txt .

COPY pub_key.pem /usr/src/pub_key.pem
COPY privkey.pem /usr/src/privkey.pem

RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . .

# Make entrypoint executable
RUN chmod +x ./docker-entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
