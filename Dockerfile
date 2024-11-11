

FROM python:3.11.9
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 80
CMD [ "fastapi", "run", "src/main.py", "--port", "80" ]
