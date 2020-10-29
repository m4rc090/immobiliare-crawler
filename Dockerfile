FROM python:3.6-slim
ARG user
ARG password
ADD requirements.lock /
RUN pip install --upgrade --extra-index-url https://$user:$password@distribution.livetech.site -r /requirements.lock
ADD . /immobiliare-crawler
ENV PYTHONPATH=$PYTHONPATH:/immobiliare-crawler
WORKDIR /immobiliare-crawler/immobiliare_crawler/services
CMD python services.py
