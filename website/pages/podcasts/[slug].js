import { useRouter } from "next/router";
import ErrorPage from "next/error";
import Container from "@/components/container";
import PostBody from "@/components/post-body";
import MoreStories from "@/components/more-stories";
import Header from "@/components/header";
import PostHeader from "@/components/post-header";
import SectionSeparator from "@/components/section-separator";
import Layout from "@/components/layout";
import PostTitle from "@/components/post-title";
import Head from "next/head";
import { CMS_NAME } from "@/lib/constants";
import markdownToHtml from "@/lib/markdownToHtml";
import { getAllPodcastsForHome, getAllEpisodesForPodcast } from "@/lib/api";

export default function Podcast({ podcast }) {
  //   const router = useRouter();
  //   if (!router.isFallback && !podcast?.slug) {
  //     return <ErrorPage statusCode={404} />;
  //   }
  console.log("podcast: ", podcast);
  return (
    <>
      <Head>
        <title>Podcast Book Library - {podcast ? podcast.title : ""}</title>
      </Head>
      <div className="bg-gray-50 pt-16 pb-20 px-4 sm:px-6 lg:pt-24 lg:pb-28 lg:px-8">
        <div className="relative mx-auto max-w-4xl">
          <div>
            <h1 className="text-3xl leading-9 tracking-tight font-extrabold text-gray-900 sm:text-6xl sm:mb-10">
              {podcast ? podcast.title : ""}
            </h1>
          </div>

          {podcast && podcast.metadata.podcastepisodes ? (
            <div className="mx-auto">
              {podcast.metadata.podcastepisodes.map((episodePost) => {
                console.log("episodePost: ", episodePost);
                console.log(
                  "episodePost book recommendations: ",
                  episodePost.metadata.bookrecommendations
                );
                return (
                  <div>
                    {episodePost.metadata.bookrecommendations ? (
                      <div className="bg-white p-10 rounded-lg shadow-nice mt-10">
                        <p className="text-sm leading-5 text-gray-500">
                          Aired on {episodePost.metadata.publishedAt}
                        </p>
                        <h3 className="mt-2 text-2xl leading-7 font-semibold text-gray-900">
                          {episodePost.title}
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {episodePost.metadata.bookrecommendations.map(
                            (bookRecommendation) => {
                              return (
                                <div className="col-span-1">
                                  <a
                                    className="p-5"
                                    href={bookRecommendation.metadata.amazonurl}
                                  >
                                    <div>
                                      <img
                                        src={
                                          bookRecommendation.metadata.image.url
                                        }
                                        className="mx-auto shadow-xl block w-50 rounded-lg"
                                        width="65%"
                                        title={bookRecommendation.title}
                                        alt={bookRecommendation.title}
                                      ></img>
                                      <p className="text-center mt-5">
                                        {bookRecommendation.title}
                                      </p>
                                    </div>
                                  </a>
                                </div>
                              );
                            }
                          )}
                        </div>
                      </div>
                    ) : (
                      <div></div>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <></>
          )}
        </div>
      </div>
    </>
  );
}

export async function getStaticProps({ params, preview = null }) {
  const data = await getAllEpisodesForPodcast(params.slug);
  console.log("getAllEpisodesForPodcast: ", data);

  return {
    props: {
      preview,
      podcast: {
        ...data[0],
      },
    },
  };
}

export async function getStaticPaths() {
  const allPosts = (await getAllPodcastsForHome()) || [];
  return {
    paths: allPosts.map((post) => `/podcasts/${post.slug}`),
    fallback: true,
  };
}
