FROM continuumio/anaconda3

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
  python -m pip install -U channels && \
  npm install -g yarn && \
  yarn global add add @vue/cli
WORKDIR /home/bandue/
