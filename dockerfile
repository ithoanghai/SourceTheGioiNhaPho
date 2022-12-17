FROM python:3
# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app
RUN mkdir -p /app \
    && mkdir -p ~/.ssh && mkdir /var/run/sshd \
    && echo 'root:docker' | chpasswd \
    && echo "export VISIBLE=now" >> /etc/profile
# Install dependencies

RUN pip install --upgrade pip
RUN pip install gunicorn gevent
RUN apt update
RUN apt-get -qq update \
    && apt-get install -y python3-pip python3-dev python3-django\
    && apt-get -y install openssh-server gdal-bin\
    && apt-get -y --no-install-recommends install apt-utils \
    && apt-get -y install curl libgdal-dev \
    && apt-get -y install nodejs yarn\
    && apt-get -y install libpq-dev gcc\
    && apt-get -y install binutils libgeos-dev\
    && apt-get -y install gettext

# SSH login fix
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/\#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i '/\#AuthorizedKeysFile/c\AuthorizedKeysFile     .ssh/authorized_keys/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt install -y nodejs yarn
COPY package.json /app
RUN npm install

# Copy project
COPY . /app
RUN useradd --create-home appuser
USER appuser