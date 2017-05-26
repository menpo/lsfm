FROM ubuntu:latest

SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y wget
Run apt-get install -y libjpeg8-dev
Run apt-get install -y freeglut3-dev
Run apt-get install -y libxrandr-dev
Run apt-get install -y libxinerama-dev
Run apt-get install -y libxcursor-dev
Run apt-get install -y libsuitesparse-dev

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/anaconda
RUN rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH "$PATH:~/anaconda/bin"
RUN ~/anaconda/bin/conda create -yn lsfm -c menpo python=3.5 lsfm

ENTRYPOINT /bin/bash --init-file <(echo "source activate lsfm;")
