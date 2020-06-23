FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP primer
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# Run all the tests first
#RUN pytest tests/

# Run the application if tests are good
CMD ["flask", "run"]