FROM python:2.7-alpine

ENV LANG C.UTF-8

WORKDIR /apitests
ADD requirements.txt /apitests/
ADD src /apitests/

RUN ls /apitests
RUN apk add --no-cache git
RUN pip install -r /apitests/requirements.txt


ENV PYTHONPATH='/usr/lib/python2.7:/usr/lib/python2.7/site-packages:/apitests'
#ENV BCDC_API_KEY=
#ENV BCDC_URL=

ENTRYPOINT ["pytest", "/apitests", "-s", "-v"]
