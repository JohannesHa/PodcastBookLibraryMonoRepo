require("dotenv").config();
const csv = require("csv-parser");
const fs = require("fs");

// Use the Cosmic.bucket method to connect to your Bucket.
const Cosmic = require("cosmicjs")();
const bucket = Cosmic.bucket({
  slug: process.env.COSMIC_BUCKET_SLUG,
  read_key: process.env.COSMIC_BUCKET_READ_KEY,
  write_key: process.env.COSMIC_BUCKET_WRITE_KEY,
});

/*
command:
node uploadPodcastEpisodes.js ID_OF_PODCAST_ON_COSMIC PATH_TO_TRANSCRIPTS_OF_PODCAST
*/

// get id of podcast on Cosmic via Command line
const args = process.argv.slice(2);
const podcastID = args[0];
// get path to transcripts via Command line
const transcriptsPath = args[1];

(async function () {
  const stream = fs
    .createReadStream(transcriptsPath + "metadata.csv")
    .pipe(csv())
    .on("data", async (row) => {
      const filename = row.fileName.split("/").pop();

      const params = {
        title: row.title,
        type: "podcast-episodes",
        metafields: [
          {
            title: "Title",
            key: "title",
            type: "text",
            value: row.title,
          },
          {
            title: "EpisodeId",
            key: "episodeId",
            type: "text",
            value: row.episodeId,
          },
          {
            title: "PublishedAt",
            key: "publishedAt",
            type: "date",
            value: new Date(row.publishedAt).toISOString().split("T")[0],
          },
          {
            title: "EpisodeFileName",
            key: "episodefilename",
            type: "text",
            value: filename,
          },
          {
            title: "BookRecommendations",
            key: "bookrecommendations",
            type: "objects",
            object_type: "book-recommendations",
            value: "61145e7a09c90000092fdf91",
          },
          {
            title: "Podcasts",
            key: "podcasts",
            type: "object",
            object_type: "podcasts",
            value: podcastID,
          },
        ],
      };

      try {
        stream.pause();
        await bucket.addObject(params).catch((err) => {
          console.log("Error while uploading podcast episode");
          console.log(err);
        });
      } catch (err) {
        console.log("Error in Try of adding object");
      } finally {
        stream.resume();
      }

      await new Promise((r) => setTimeout(r, 10000));
    })
    .on("end", () => {
      console.log("CSV file successfully processed");
    });
})();
