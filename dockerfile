FROM python:3
# Set environmental variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN pip install --upgrade pip
RUN pip install gunicorn gevent
#RUN npm install
RUN apt update
RUN apt install -y nodejs yarn
RUN apt-get -qq update \
    && apt-get install -y python3-pip python3-dev python3-django\
    && apt-get -y install openssh-server gdal-bin\
    && apt-get -y --no-install-recommends install apt-utils \
    && apt-get -y install curl libgdal-dev \
    && apt-get -y install nodejs yarn\
    && apt-get -y install libpq-dev gcc\
    && apt-get -y install binutils libgeos-dev\
    && apt-get -y install gettext

RUN mkdir -p /app \
    && mkdir -p ~/.ssh && mkdir /var/run/sshd \
    && echo 'root:docker' | chpasswd \
    && echo "export VISIBLE=now" >> /etc/profile
# SSH login fix
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i 's/\#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -i '/\#AuthorizedKeysFile/c\AuthorizedKeysFile     .ssh/authorized_keys/' /etc/ssh/sshd_config \
    && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Copy project
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

#RUN useradd --create-home appuser
#USER appuser