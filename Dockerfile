FROM python:3.7.9

WORKDIR /zezinho
COPY apps /zezinho/apps
COPY bop /zezinho/bop
COPY static /zezinho/static
COPY templates /zezinho/templates
COPY manage.py /zezinho

COPY requirements.txt /zezinho

RUN pip install -r requirements.txt

CMD [ "/usr/local/bin/python", "manage.py", "runserver" ]