# Book Recommendation Extractor API

A FastAPI deployment of the spaCy Model that you can call to get the book recommendations of a transcript (including the Amazon book information, such as the author, an image and the url).

- build docker image:

```bash
docker build -t fastapi:latest .
```

- run the docker image:

```bash
docker run -p 80:5000 fastapi:latest
```
