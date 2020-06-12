import time
import math
import redis
from flask import Flask
from flask import render_template

# Setup the application
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379,
                    charset="utf-8", decode_responses=True)


# Get the list from cache
def get_from_cache():
    retries = 5
    while True:
        try:
            return cache.lrange('numbers', 0, -1)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


# Push a number onto the cache
def push_onto_cache(number):
    retries = 5
    while True:
        try:
            cache.lpush('numbers', number)
            return
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


# This method determines if a number is prime or not
def is_number_prime(number):
    # 2 is the only even prime number
    if number == 2:
        return True

    # 0, 1, and even numbers are not primes
    if number % 2 == 0 or number <= 1:
        return False

    sqr = int(math.sqrt(number)) + 1

    for divisor in range(3, sqr, 2):
        if number % divisor == 0:
            return False

    return True


# Route for /isPrime/<number>
@app.route('/isPrime/<int:number>')
def is_prime_route(number):
    if is_number_prime(number):
        push_onto_cache(number)
        return '{} is prime'.format(number)
    else:
        return '{} is not prime'.format(number)

# Route for /primesStored
@app.route('/primesStored')
def primes_stored_route():
    # Get the numbers list from redis
    numbers = get_from_cache()

    # Return the numbers list in a formatted html document
    return render_template('list.html', numbers=numbers)
