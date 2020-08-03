FROM ruby:2.7.1-slim-buster
RUN apt update && \
    rm -rf /var/lib/apt/lists/* && \
    gem install aws-sdk
COPY ./src /app/
WORKDIR /app/
CMD [ "ruby", "create_queue.rb" ]
