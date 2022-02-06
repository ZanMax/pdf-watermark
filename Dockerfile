FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq -y update && \
    apt-get install -q -y software-properties-common
RUN add-apt-repository ppa:libreoffice/ppa

RUN apt-get -qq -y update \
    && apt-get -q -y upgrade \
    && apt-get -q -y dist-upgrade \
    && apt-get -q -y install locales libreoffice libreoffice-writer psmisc curl \
    libreoffice-impress libreoffice-common fonts-opensymbol hyphen-fr hyphen-de \
    hyphen-en-us hyphen-it hyphen-ru fonts-dejavu fonts-dejavu-core fonts-dejavu-extra \
    fonts-droid-fallback fonts-dustin fonts-f500 fonts-fanwood fonts-freefont-ttf \
    fonts-liberation fonts-lmodern fonts-lyx fonts-sil-gentium fonts-texgyre \
    fonts-tlwg-purisa python3-dev python3-pip python3-uno python3-lxml python3-icu unoconv \
    libmpc-dev libgmp-dev libmpfr-dev build-essential poppler-utils \
    && apt-get -qq -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

ENV LANG='en_US.UTF-8'

EXPOSE 80
WORKDIR /app

COPY . ./
RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]