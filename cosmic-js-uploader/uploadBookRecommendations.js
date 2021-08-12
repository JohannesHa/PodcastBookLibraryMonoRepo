require("dotenv").config();
const csv = require("csv-parser");
const fs = require("fs");
const axios = require("axios");
var https = require("https");

// Use the Cosmic.bucket method to connect to your Bucket.
const Cosmic = require("cosmicjs")();
const bucket = Cosmic.bucket({
  slug: process.env.COSMIC_BUCKET_SLUG,
  read_key: process.env.COSMIC_BUCKET_READ_KEY,
  write_key: process.env.COSMIC_BUCKET_WRITE_KEY,
});

/*
command:
node uploadPodcastEpisodes.js ID_OF_PODCAST_ON_COSMIC FOLDER_NAME_OF_PODCAST
*/

// get id of podcast on Cosmic via Command line
const args = process.argv.slice(2);
const podcastID = args[0];
// get folder name of podcast via Command line
const podcastFolderName = args[1];

const transcriptsPath = "./transcripts/";
const s3BaseUrl =
  "https://podcast-transscripts.s3.eu-central-1.amazonaws.com/transcripts/";
const bookRecommendationExtractorUrl =
  "http://localhost:8000/nlp/id/book-recommendations";

// Returns a Promise that resolves after "ms" Milliseconds
const timer = (ms) => new Promise((res) => setTimeout(res, ms));

(async function () {
  fs.readdir(transcriptsPath + podcastFolderName, async (err, files) => {
    files.forEach(async (file, i) => {
      setTimeout(async () => {
        console.log("file before if: ", file);
        // Only process txt file
        if (file.includes(".txt")) {
          console.log("File: ", file);

          const s3FileUrl = s3BaseUrl + podcastFolderName + "/" + file;
          console.log("s3FileUrl: ", s3FileUrl);
          const payload = { s3Url: s3FileUrl };
          await timer(3000);
          const res = await axios.post(bookRecommendationExtractorUrl, payload);
          const data = res.data;
          console.log("data: ", data);

          data.forEach(async (bookRecommendation) => {
            var downloadImage = function (url, dest, cb) {
              // save image of amazon book and then upload it
              var imageFile = fs.createWriteStream(dest);
              var request = https
                .get(url, function (response) {
                  response.pipe(imageFile);
                  imageFile.on("finish", async function () {
                    imageFile.close(cb); // close() is async, call cb after close completes.
                  });
                })
                .on("error", function (err) {
                  // Handle errors
                  fs.unlink(dest); // Delete the file async. (But we don't check the result)
                  if (cb) cb(err.message);
                });
            };

            let imageFilename =
              bookRecommendation.title.replace(/\//g, "") + ".jpg";
            downloadImage(
              bookRecommendation.imageUrl,
              imageFilename,
              async () => {
                // upload image via Media API
                const filedata = fs.readFileSync("./" + imageFilename);
                const media_object = {
                  originalname: imageFilename,
                  buffer: filedata,
                };

                bucket
                  .addMedia({
                    media: media_object,
                    folder: "book-images",
                  })
                  .then(async (mediaResponse) => {
                    // upload book recommendation
                    const params = {
                      title: bookRecommendation.title,
                      type: "book-recommendations",
                      metafields: [
                        {
                          title: "Title",
                          key: "title",
                          type: "text",
                          value: bookRecommendation.title,
                        },
                        {
                          title: "Author",
                          key: "author",
                          type: "text",
                          value: bookRecommendation.authors[0],
                        },
                        {
                          title: "AmazonUrl",
                          key: "amazonurl",
                          type: "text",
                          value: bookRecommendation.amazonUrl,
                        },
                        {
                          title: "Image",
                          key: "image",
                          type: "file",
                          value: mediaResponse.media.name,
                        },
                        {
                          title: "EpisodeFileName",
                          key: "episodefilename",
                          type: "text",
                          value: file,
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

                    console.log("Params: ", params);

                    await bucket.addObject(params).catch((err) => {
                      console.log(
                        "Error while uploading book recommendation with params: ",
                        params
                      );
                      console.log(err);
                    });
                  })
                  .catch((err) => {
                    console.log(err);
                  });
              }
            );
          });
        }
      }, i * 10000);
    });
  });
})();
