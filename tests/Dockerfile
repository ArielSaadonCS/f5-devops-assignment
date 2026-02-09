FROM python:3.12-alpine

#set working directory inside the container
WORKDIR /app

#copy test script into the image
COPY test.py /app/test.py

#run the test script when the container strats
CMD ["python","/app/test.py"]