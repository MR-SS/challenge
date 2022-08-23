FROM python:3.8-slim

RUN apt-get update && apt-get install -y
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Add a user with userid 8877 and name nonroot
RUN useradd  -u 8877 nonroot



WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#Run Container as nonroot
USER nonroot
COPY . .



# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]