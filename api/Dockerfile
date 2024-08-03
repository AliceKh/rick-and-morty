FROM python:3.9

EXPOSE 8000

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

HEALTHCHECK CMD curl -f http://localhost:8000/healthcheck || exit 1

ENTRYPOINT ["fastapi"]
CMD ["run", "main.py", "--port", "8000"]