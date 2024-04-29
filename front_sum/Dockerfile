
FROM python:3.9


RUN pip install Flask psycopg2-binary


COPY front_sum.py .
COPY templates templates/


EXPOSE 9000

CMD ["python", "front_sum.py"]