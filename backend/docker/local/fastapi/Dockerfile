Arg PYTHON_VERSION=3.13.13

FROM python:${PYTHON_VERSION}-slim-bookworm AS python

# Stage 1: build dependency wheels (and basically python wheels are a precompiled binary package for python modules. They are used to install dependencies in a fster and more efficient way)
FROM python AS python-build-stage

# RUn command to build the docker container and first we are using apt which is the package manager for Debian and Ubuntu systems. "apt-get update" basically updating the package index using apt as the package
# manager to get the latest information about availble packages, then "apt get install" using this to install the packages on the container
# By default apt will install required dependencies which are a must have and recommended packages which are nice to have but are optional and suggested packages which are not required but recommended. and when we say "--noinstall-recommends -y" this flag is going to tell apt to installl only the required dependencies
# then the flag -y is going to automatically answer yes to any prompts for confirmation allowing the installation to proceed without manual intervention
# "build-essential" is a meta package in Debian or Ubuntu syatems that install everything needed to compile the software and in our case we need the buils essential in our dockerfile, because some python packages in our requirements like psycopg, async and potentially others are not pure python packages
# "libpq-dev" this is the development package that includes all necessary files for building Python packages that need to interact with Postgres like psycopg and async which are in our requirements.txt file
RUN apt-get update && apt-get install \
  --no-install-recommends -y \
  build-essential \
  libpq-dev

COPY ./backend/requirements.txt .

# Here we are creating the dependency and dependency wheels and remember the wheels are aprebuilt package format that install faster and are more efficient than source distributions and they don't require compilation during installation
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r requirements.txt \
    --no-cache-dir


# Stage 2: Python run stage
From python AS python-run-stage

# dir in our container where application shall live
ARG APP_HOME=/src
# This is the user who run the application
ARG APP_USER=fastapi
# This is going to be the group that the user belongs to
ARG App_GROUP=fastapi

# This prevent from writing .pyc files which are compiled bytecode files to our disk. This is useful for reducing the size of the final docker image
# PYTHONUNBUFFERED with the value one prevents python from buffering the output. This means that the output will be sent directly to the console or the terminal without any buffering thus allowing some real time output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo git bash-completion nano ssh \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r ${App_GROUP} && \
    useradd -r -g ${App_GROUP} -d ${APP_HOME} -m ${APP_USER}


RUN mkdir -p ${APP_HOME}/backend/app/logs && \
    chown -R ${APP_USER}:${APP_GROUP} ${APP_HOME}/backend/app/logs && \
    chmod 775 ${APP_HOME}/backend/app/logs

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY --chown=${APP_USER}:{APP_GROUP} ./backend/docker/local/fastapi/entrypoint.sh /entrypoint.sh

COPY --chown=${APP_USER}:{APP_GROUP} ./backend/docker/local/fastapi/start.sh /start.sh

COPY --chown=${APP_USER}:{APP_GROUP} ./backend/docker/local/fastapi/celery/worker/start.sh /start-celeryworker.sh

COPY --chown=${APP_USER}:{APP_GROUP} ./backend/docker/local/fastapi/celery/beat/start.sh /start-celerybeat.sh

COPY --chown=${APP_USER}:{APP_GROUP} ./backend/docker/local/fastapi/celery/flower/start.sh /start-flower.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh && \
    chmod +x /entrypoint.sh /start.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh

COPY --chown=${APP_USER}:${APP_GROUP} . ${APP_HOME}

USER ${APP_USER}

ENTRYPOINT [ "/entrypoint.sh" ]
