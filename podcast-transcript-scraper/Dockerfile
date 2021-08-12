FROM alpine:latest

# Get all the prereqs
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk
RUN wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk
RUN apk add glibc-2.30-r0.apk
RUN apk add glibc-bin-2.30-r0.apk

# And of course we need Firefox if we actually want to *use* GeckoDriver
RUN apk add firefox-esr

RUN apk add --no-cache bash

# Then install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
RUN tar -zxf geckodriver-v0.28.0-linux64.tar.gz -C /usr/bin
RUN geckodriver --version

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi


COPY . .

WORKDIR /

RUN chmod 755 /

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "pipeline.py"]