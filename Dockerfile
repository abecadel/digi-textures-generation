FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
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
RUN conda create --name digi python=3.10

SHELL ["conda", "run", "--no-capture-output", "-n", "digi", "/bin/bash", "-c"]
RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
RUN conda install xformers -c xformers -y

COPY requirements.txt .
RUN pip install -r requirements.txt

#install stable diffusion
RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
WORKDIR stable-diffusion-webui
RUN mkdir repositories
RUN git clone https://github.com/CompVis/stable-diffusion.git repositories/stable-diffusion
RUN git clone https://github.com/CompVis/taming-transformers.git repositories/taming-transformers
RUN git clone https://github.com/sczhou/CodeFormer.git repositories/CodeFormer
RUN git clone https://github.com/salesforce/BLIP.git repositories/BLIP
RUN pip install -r repositories/CodeFormer/requirements.txt --prefer-binary
RUN pip install -r requirements.txt --prefer-binary


#install controlnet
WORKDIR /app
RUN git clone https://github.com/Mikubill/sd-webui-controlnet.git
