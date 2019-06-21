FROM python:2.7-alpine

ENV LANG C.UTF-8

WORKDIR /apitests

COPY . /apitests

RUN cd /apitests && pip install -r /apitests/requirements.txt && pip install twine && python setup.py sdist bdist_wheel
RUN  python -m twine upload dist/*
