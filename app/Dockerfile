FROM chdavid/rapid:latest as rapid
COPY . ./tst/

RUN apt-get -y update && apt-get install -y python3-pip

RUN pip3 install --user fastapi uvicorn boto3 flask requests

EXPOSE 5000

WORKDIR tst/

CMD ["python3", "rapid_app.py"]
#CMD  /bin/bash
