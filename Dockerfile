FROM python:3.10

WORKDIR /Warelio

# Set PYTHONPATH to ensure imports work from this root
ENV PYTHONPATH="/Warelio"

COPY . .

RUN pip install -r req.txt --no-cache-dir

# just for documentation
EXPOSE 8001

# set permissions for shell scripts
RUN chmod +x /Warelio/entrypoint.sh \
    && chmod +x /Warelio/bashes/start_django.sh \
    && chmod +x /Warelio/bashes/start_pubsub_subscriber.sh

# st the entrypoint to the script
ENTRYPOINT ["/Warelio/entrypoint.sh"]