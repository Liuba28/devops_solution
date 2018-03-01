FROM python:2

ADD geoserver.py /

RUN pip install requests

RUN pip install geojson

CMD [ "python", "./geoserver.py" ]

 


