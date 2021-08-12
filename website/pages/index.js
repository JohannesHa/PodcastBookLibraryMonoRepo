import Container from "@/components/container";
import MoreStories from "@/components/more-stories";
import HeroPost from "@/components/hero-post";
import Intro from "@/components/intro";
import Layout from "@/components/layout";
import HeroHeader from "@/components/hero-header";
import Podcasts from "@/components/podcasts";
import MostRecommended from "@/components/most-recommended";

import { getAllPodcastsForHome } from "@/lib/api";
import Head from "next/head";
import { CMS_NAME } from "@/lib/constants";

export default function Index({ allPodcasts }) {
  return (
    <>
      <Head>
        <title>Podcast Book Library</title>
      </Head>
      <HeroHeader />
      <Podcasts allPodcasts={allPodcasts} />
      {/* <MostRecommended /> */}
    </>
  );
}

export async function getStaticProps({ preview }) {
  const allPodcasts = (await getAllPodcastsForHome(preview)) || [];
  console.log("allPodcasts ", allPodcasts);
  allPodcasts.map((podcast) => {
    console.log("podcast Episodes: ", podcast.metadata.podcastepisodes);
  });
  return {
    props: { allPodcasts },
  };
}
