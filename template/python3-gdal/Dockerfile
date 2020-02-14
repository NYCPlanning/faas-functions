FROM openfaas/of-watchdog:0.7.2 as watchdog
FROM sptkl/cook:latest

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup --gid 888 app && useradd -g app app
RUN mkdir /home/app
RUN chown app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .
USER root
RUN pip3 install -r requirements.txt
USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt	.
RUN pip3 install --user -r requirements.txt

WORKDIR /home/app/

USER root
COPY function   function
RUN chown -R app:app ./
USER app

ENV fprocess="python3 index.py"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]