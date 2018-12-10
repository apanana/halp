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

WORKDIR /tmp
RUN wget https://sourceforge.net/projects/lpsolve/files/lpsolve/5.5.2.0/lp_solve_5.5.2.0_dev_ux64.tar.gz
RUN wget https://sourceforge.net/projects/lpsolve/files/lpsolve/5.5.2.0/lp_solve_5.5.2.0_Python2.5_exe_ux64.tar.gz
RUN mkdir -p /tmp/lp_solve_dev
RUN tar -xvzf lp_solve_5.5.2.0_dev_ux64.tar.gz -C /tmp/lp_solve_dev
RUN tar -xvzf lp_solve_5.5.2.0_Python2.5_exe_ux64.tar.gz

WORKDIR /root/lpsolve
RUN mv /tmp/lp_solve_dev .
RUN mv /tmp/usr .

ENV LD_LIBRARY_PATH=/usr/local/lib:/root/lpsolve/lp_solve_dev/
ENV PYTHONPATH=/root/lpsolve/usr/lib/python2.5/site-packages

# To build image:
# cd <halp_root_dir>
# docker build . -t halp
# To run: 
# docker run -it -v <full_path_to_halp>:<full_path_to_halp> halp bash
