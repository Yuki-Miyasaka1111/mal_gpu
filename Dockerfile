# ベースイメージ
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# 非対話モードでのタイムゾーン設定をスキップ
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

# Python 3.6と依存関係のインストール
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    wget \
    tar \
    git \
    && rm -rf /var/lib/apt/lists/*

# CUDAとcuDNNのインストールP
RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-toolkit-11-8 \
    libcudnn8 \
    libcudnn8-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /workspace

# requirements.txtをコンテナにコピー
COPY requirements.txt /workspace/

# requirements.txtからPythonパッケージをインストール
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# デフォルトのコマンド
CMD ["bash"]