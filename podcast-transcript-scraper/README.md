# podcast-transcript-scraper

This project uses browser automation to click through the HappyScribe web interface and download the transcript file.

## requirements

- Docker

## use

- Build and run docker container

`docker build --tag podcast-scraper .`

`docker run podcast-scraper:latest`

- copy `.env.example` to `.env` and replace variables

- To run the docker container locally on MacOS, you have to add the `/transcript` path to your docker -> preferences -> resources -> file sharing, like this:
  ![Docker MacOS Setup](https://github.com/JohannesHa/PodcastBookLibraryMonoRepo/blob/master/podcast-transcript-scraper/assets/docker-macos-setup.png?raw=true)
