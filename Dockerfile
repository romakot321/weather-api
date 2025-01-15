FROM python:3.13 AS PackageBuilder
COPY ./requirements.txt ./requirements.txt
RUN pip3 wheel -r requirements.txt


FROM python:3.13-slim
EXPOSE 80

# Setup user
ENV UID=2000
ENV GID=2000

RUN groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init --shell /bin/bash -u "${UID}" -g "${GID}" python

USER python
WORKDIR /home/python

RUN mkdir ./wheels
COPY --from=PackageBuilder ./*.whl ./wheels/
RUN pip3 install ./wheels/*.whl --no-warn-script-location

COPY setup.py ./
COPY ./app ./app
RUN pip3 install .

ENV PATH="$PATH:/home/python/.local/bin"
CMD python3 -c "__import__('app.db.base').db.base.run_init_models()" && \
    gunicorn app.main:fastapi_app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
