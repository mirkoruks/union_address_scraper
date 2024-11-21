FROM python:3.12.5

RUN mkdir /home/app
RUN mkdir /home/app/data

WORKDIR /home/app

COPY main.py union_scraper.py requirements.txt ./

RUN pip install -r requirements.txt 

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean   

CMD ["python", "main.py"]