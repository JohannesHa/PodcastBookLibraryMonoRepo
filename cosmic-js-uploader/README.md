# CosmicJSUploader

Processes all transcripts by calling the book recommendation extractor API and then uploads all podcast episodes as well as the book recommendations to CosmicJS

## Examples for using

- Example podcast episode upload command:

```
node uploadPodcastEpisodes.js PODCAST_ID_ON_COSMIC ./transcripts/1_lex_fridman/
```

- Example Link Podcast to Podcast Episodes command:

```
node linkPodcastsToPodcastEpisodes.js PODCAST_ID_ON_COSMIC
```

- Example book recommendation upload command:

```
node uploadBookRecommendations.js PODCAST_ID_ON_COSMIC 1_lex_fridman
```

- Example book recommendation upload command:

```
node linkPodcastEpisodeToBookRecommendations.js
```

**Important:**
The Book Recommendation Extractor API is only callable from white-listed IPs.
