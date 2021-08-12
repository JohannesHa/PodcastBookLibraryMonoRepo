require("dotenv").config();
var request = require("request");

// Use the Cosmic.bucket method to connect to your Bucket.
const Cosmic = require("cosmicjs")();
const bucket = Cosmic.bucket({
  slug: process.env.COSMIC_BUCKET_SLUG,
  read_key: process.env.COSMIC_BUCKET_READ_KEY,
  write_key: process.env.COSMIC_BUCKET_WRITE_KEY,
});

/*
command:
node linkPodcastEpisodeToBookRecommendations.js
*/

try {
  // retrieve all Podcast Episodes
  bucket
    .getObjects({
      query: {
        type: "podcast-episodes",
        "metadata.bookrecommendations": ["61145e7a09c90000092fdf91"],
      },
      props:
        "title,metadata.bookrecommendations,metadata.episodefilename,metadata.podcasts.id,id",
      limit: 1,
    })
    .then((podcastEpisodes) => {
      console.log("podcastEpisodes: ", podcastEpisodes);

      podcastEpisodes.objects.forEach(async (podcastEpisode) => {
        // Go through all Book Recommendations and check if it has the Podcast ID + same Episode Filename
        let matchingBookRecommendationIds = [];

        console.log(
          "podcastEpisode.metadata.bookrecommendations: ",
          podcastEpisode.metadata.bookrecommendations
        );

        // retrieve all Book Recommendations
        await bucket
          .getObjects({
            query: {
              type: "book-recommendations",
              "metadata.episodefilename":
                podcastEpisode.metadata.episodefilename,
              //   "metadata.podcasts.id": podcastEpisode.metadata.podcasts.id,
            },
            props: "title,metadata.podcasts.id,metadata.episodefilename,id",
            limit: 10,
          })
          .then((bookRecommendations) => {
            console.log("bookRecommendations: ", bookRecommendations);
            bookRecommendations.objects.forEach(async (bookRecommendation) => {
              if (
                podcastEpisode.metadata.podcasts.id &&
                podcastEpisode.metadata.episodefilename &&
                podcastEpisode.metadata.podcasts.id ==
                  bookRecommendation.metadata.podcasts.id &&
                podcastEpisode.metadata.episodefilename ==
                  bookRecommendation.metadata.episodefilename
              ) {
                console.log(
                  "Found matching book recommendation for episode: " +
                    podcastEpisode.title +
                    " and book: " +
                    bookRecommendation.title
                );
                matchingBookRecommendationIds.push(bookRecommendation.id);
              }
            });
          })
          .catch((error) => {
            console.log("Error while getting Book Recommendations: ", error);
          });

        const bookRecommendationIdsString =
          matchingBookRecommendationIds.join(",");

        // call Edit Metafield Endpoint directly via REST API because the editMetafield() API function is broken
        var options = {
          method: "PATCH",
          url:
            "https://api.cosmicjs.com/v2/buckets/podcast-book-recommendation-site-production/objects/" +
            podcastEpisode.id +
            "/metafields/bookrecommendations",
          headers: {
            Authorization: "Bearer " + process.env.COSMIC_BUCKET_WRITE_KEY,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            value: bookRecommendationIdsString,
          }),
        };

        request(options, function (error, response) {
          if (error) throw new Error(error);
          console.log(response.body);
        });
      });
    })
    .catch((error) => {
      console.log("Error while getting Podcast Episodes: ", error);
    });
} catch (e) {
  console.log("Catch an error: ", e);
}
