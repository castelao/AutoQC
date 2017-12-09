FROM ubuntu:16.04

# configure environment for install
RUN apt-get update
RUN apt-get install -y git nano wget bzip2

# install AutoQC and all deps
RUN git clone https://github.com/IQuOD/AutoQC
WORKDIR /AutoQC
RUN sed -i -e 's/sudo //g' install.sh
RUN source install.sh

# set default environment variables
ENV OCEANSDB_DIR /AutoQC/data/