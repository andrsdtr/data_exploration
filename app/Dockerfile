FROM python:3
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
ADD data /usr/src/app/data
CMD ["python", "app.py"]