FROM python:3.12-alpine

#set working directory inside the container
WORKDIR /app

# copy only the test file
COPY test.py /app/test.py

# run tests on container start
CMD ["python","/app/test.py"]
