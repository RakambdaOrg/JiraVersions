FROM python:3.11

ARG UNAME=pythonuser
ARG UID=1000
ARG GID=100

RUN mkdir -p /usr/src/app
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && /usr/sbin/groupadd -g ${GID} -o ${UNAME} \
    && /usr/sbin/useradd -m -u ${UID} -g ${GID} -o -s /bin/bash ${UNAME} \
    && chown -R ${UNAME}:${UNAME} /usr/src/app

USER ${UNAME}
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY src/ /usr/src/app/

ENTRYPOINT ["/entrypoint.sh"]