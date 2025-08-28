FROM ubuntu:22.04

# Устанавливаем переменные окружения для избежания вопросов при установке
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем и устанавливаем все зависимости
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    python3-dev \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses-dev \
    cmake \
    libffi-dev \
    libssl-dev \
    libtinfo6 \
    build-essential \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем buildozer БЕЗ принудительного обновления Cython
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir \
    buildozer \
    virtualenv \
    setuptools

# Устанавливаем нужную версию Cython через apt (если доступно)
RUN apt-get update && apt-get install -y cython3 || echo "Cython3 not available in apt, will use pip"

# Устанавливаем конкретную версию Cython через pip с флагом --ignore-installed
RUN pip3 install --no-cache-dir --ignore-installed Cython==0.29.33

# Создаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Указываем точку входа
CMD ["bash"]