# Rodando backend
FROM python:3.10.5

WORKDIR /gerenciador/backend

COPY . /gerenciador

RUN pip install --no-cache-dir --upgrade -r /gerenciador/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
