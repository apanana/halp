FROM ubuntu:16.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
	python2.7 \
	python-dev \
	python-pip \
	wget \
	lp-solve \
	liblpsolve55-dev \
	git

RUN pip install --upgrade pip 
RUN pip install setuptools
RUN pip install \
	pytest==3.0.2 \
	networkx \
	numpy==1.11.0 \
	scipy==0.17.0

# To build image:
# cd <halp_root_dir>
# docker build . -t halp
# To run: 
# docker run -it -v <full_path_to_halp>:<full_path_to_halp> halp bash
