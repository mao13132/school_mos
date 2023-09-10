FROM ubuntu
LABEL authors="mao1313"

WORKDIR app

COPY requirements.txt requirements.txt

RUN apt upgrade

RUN apt-get update && apt-get install -y unzip

RUN apt -f install -y
RUN apt-get update && apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip
RUN unzip chromedriver-linux64.zip && rm chromedriver-linux64.zip
RUN chmod +x chromedriver
RUN mv chromedriver /usr/local/bin/chromedriver


RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install -r requirements.txt
RUN pip3 install pyvirtualdisplay selenium

COPY . .


CMD ["python3", "main.py"]