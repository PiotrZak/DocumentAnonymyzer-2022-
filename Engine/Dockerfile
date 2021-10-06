FROM python:3.8

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
# RUN python -m spacy download pl_core_news_lg

ENTRYPOINT ["python"]

EXPOSE 5000
CMD ["hello.py"]