FROM python:3.10-slim
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY setup.py ./

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install libmagic-dev
RUN apt-get -y install python3-magic

RUN pip install --upgrade pip
RUN pip install pur
RUN pur -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "views:app", "--host", "0.0.0.0", "--port", "8089"]
