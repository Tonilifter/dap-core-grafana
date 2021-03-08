FROM daplatform0101pcr.azurecr.io/python-base:latest

RUN mkdir app

WORKDIR app

COPY . .

ENV PIP_CONFIG_FILE=pip.conf

RUN pip install -r requirements.txt

RUN rm pip.conf

EXPOSE 80

CMD ["python", "landing_api_entrypoint.py"]