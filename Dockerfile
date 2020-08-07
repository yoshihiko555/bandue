FROM continuumio/anaconda3

WORKDIR /home/bandue/server

RUN apt-get update && apt-get install -y --no-install-recommends \
  net-tools \
  sudo \
  bzip2 \
  curl \
  gcc \
  git \
  python3-dev \
  vim \
  && \
  apt-get clean && \
  pip install --upgrade pip && \
  conda update -n base conda && \
  conda update --all && \
  conda install -c conda-forge nodejs=10.13.0 && \
  conda clean --all -y && \
  conda install -c anaconda django && \
  conda install -c conda-forge django-filter && \
  conda install -c conda-forge djangorestframework && \
  conda install -c conda-forge djangorestframework-jwt && \
  conda install -c conda-forge django-cors-headers && \
  conda install -c conda-forge django-webpack-loader && \
  conda install -c anaconda python-memcached && \
  conda install -c anaconda psycopg2 && \
  conda install -c conda-forge whitenoise && \
  conda install -c anaconda gunicorn && \
  python -m pip install -U channels && \
  pip install channels_redis && \
  npm install -g yarn && \
  yarn global add add @vue/cli

COPY ./server .

RUN python manage.py collectstatic --noinput

MAINTAINER admin

ENV USER admin

RUN useradd -m ${USER}
RUN gpasswd -a ${USER} sudo
RUN echo "${USER}:test_pass" | chpasswd
USER ${USER}

CMD gunicorn server.wsgi:application --bind 0.0.0.0:$PORT