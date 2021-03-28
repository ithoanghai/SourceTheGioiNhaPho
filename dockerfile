FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get -qq update \
    && apt-get -y install openssh-server gdal-bin
RUN mkdir -p /webapp \
    && mkdir -p ~/.ssh && mkdir /var/run/sshd \
    && echo 'root:docker' | chpasswd \
    && echo "export VISIBLE=now" >> /etc/profile

# SSH login fix
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/\#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i '/\#AuthorizedKeysFile/c\AuthorizedKeysFile     .ssh/authorized_keys/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
# RUN useradd --create-home appuser
# USER appuser