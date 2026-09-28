# pull official base image
FROM python:3.14.2-slim-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install net-cat for entrypoint, no need for gcc nor postgresql since we use psycopg-binary
RUN apt-get update \
  && apt-get -y install netcat-traditional \
  && apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# new
# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . .

# new
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]