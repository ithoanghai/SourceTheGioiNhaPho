FROM python:3
#ENV PYTHONUNBUFFERED=1
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -qq update \
    && apt-get -y install openssh-server gdal-bin\
    && apt-get -y --no-install-recommends install apt-utils \
    && apt-get -y install curl libgdal-dev \
    && apt-get -y install nodejs yarn
RUN pip install gunicorn gevent
RUN apt update
RUN apt install gettext -y

RUN mkdir -p /webapp \
    && mkdir -p ~/.ssh && mkdir /var/run/sshd \
    && echo 'root:docker' | chpasswd \
    && echo "export VISIBLE=now" >> /etc/profile
WORKDIR /app

# SSH login fix
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/\#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i '/\#AuthorizedKeysFile/c\AuthorizedKeysFile     .ssh/authorized_keys/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

COPY requirements.txt manage.py package.json ./
COPY requirements.txt manage.py package.json /app
RUN pip install -r requirements.txt
RUN npm install

# install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs yarn

COPY . /app
#RUN useradd --create-home appuser
#USER appuser