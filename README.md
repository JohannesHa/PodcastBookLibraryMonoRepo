# Podcast Book Library

## Demo

A demo of the project can be visited at:

[https://podcast-book-recommendation-website-new.vercel.app/](https://podcast-book-recommendation-website-new.vercel.app/)

## Repo structure

This repo is a mono repo, organized by "projects":

- `./nlp`: Jupyter Notebook scripts to train the model + spaCy training and test set
- `./book-recommendation-extractor-api`: FastAPI Deployment of SpaCy Model. You can call it to get Book Recommendations (with all the Amazon information)
- `./podcast-transcript-scraper`: Selenium scraper that connects to Airtable to receive new added Podcasts and goes to Happyscribe to scrape Podcast transcript
  - Uploads them to S3
  - Runs dockerized on DigitalOcean
- `./website`: Website to show the Book Recommendations
  - Based on Next.js + React + TailwindCSS + CosmicJS boilerplate
- `./cosmic-js-uploader`: Scripts to upload Book Recommendations to Content Management System
  - Also includes all the transcript files + metadata

All projects have their own README file that explains how to install and run the different projects.
