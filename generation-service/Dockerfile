FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update
RUN apt-get install -y wget git libgl1 libglib2.0-0 ffmpeg build-essential curl libtbb-dev libopenexr-dev

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda update -n base -c defaults conda -y
RUN conda init
RUN conda create --name digi python=3.9

SHELL ["conda", "run", "--no-capture-output", "-n", "digi", "/bin/bash", "-c"]
RUN conda install pytorch=1.13.1 torchvision pytorch-cuda=11.7 -c pytorch -c nvidia
RUN pip install kaolin==0.13.0 -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-1.13.1_cu117.html

COPY requirements.txt .
RUN pip install -r requirements.txt
