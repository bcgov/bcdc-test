FROM python:2.7-alpine

ENV LANG C.UTF-8

WORKDIR /apitests

#ENV USER=${PYPI_USER}
#ENV PSWD=${PYPI_PSWD}

ADD requirements.txt /apitests/
COPY bcdc_apitests bcdc_apitests/
ADD setup.py /apitests/
ADD LICENSE /apitests/
ADD MANIFEST.in /apitests/
ADD README.md /apitests/

RUN ls -l /apitests/*
RUN echo "USER: " ${PYPI_USER}

RUN ls -l /usr/local/bin
#RUN apk add --no-cache git
RUN cd /apitests && pip install -r /apitests/requirements.txt && pip install twine && python setup.py sdist bdist_wheel
ENV PYTHONPATH='/usr/lib/python2.7:/usr/lib/python2.7/site-packages:/apitests'
#ECHO "USER:" ${USER}
#ENTRYPOINT ["python", "-m", "twine", "upload", "dist/*", "-p", $PYPI_PSWD, "-u", $PYPI_USER]
#ENTRYPOINT ["python", "-m", "twine", "upload", "dist/*"]
#ENTRYPOINT python -m twine upload dist/* -p $PYPI_PSWD -u $PYPI_USER --skip-existing 
RUN  python -m twine upload dist/* -p ${PYPI_PSWD} -u ${PYPI_USER} --skip-existing
