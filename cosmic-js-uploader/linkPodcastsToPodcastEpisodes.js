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
node linkPodcastsToPodcastEpisodes.js ID_OF_PODCAST_ON_COSMIC
*/

// get id of podcast on Cosmic via Command line
const args = process.argv.slice(2);
const podcastID = args[0];

try {
  bucket
    .getObjects({
      query: {
        type: "podcast-episodes",
      },
    })
    .then((podcastEpisodes) => {
      console.log("inside callback of get podcast episodes");
      const filteredForPodcastID = podcastEpisodes.objects.filter((episode) => {
        let addToList = false;
        episode.metadata.podcasts
          ? (addToList = episode.metadata.podcasts.id == podcastID)
          : (addToList = false);
        return addToList;
      });
      console.log("after filter podcasts");

      const episodeIds = filteredForPodcastID.map((episode) => episode.id);
      const episodeIdsString = episodeIds.join(",");
      console.log("after adding everyhitn to strings");

      // call Edit Metafield Endpoint directly via REST API because the editMetafield() API function is broken
      var options = {
        method: "PATCH",
        url:
          "https://api.cosmicjs.com/v2/buckets/podcast-book-recommendation-site-production/objects/" +
          podcastID +
          "/metafields/podcastepisodes",
        headers: {
          Authorization: "Bearer " + process.env.COSMIC_BUCKET_WRITE_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          value: episodeIdsString,
        }),
      };

      request(options, function (error, response) {
        if (error) throw new Error(error);
        console.log(response.body);
      });
    })
    .catch((error) => {
      console.log("Error while getting Podcast Episodes: ", error);
    });
} catch (e) {
  console.log("Catch an error: ", e);
}
