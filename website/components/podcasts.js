import PodcastItem from "./podcast-item";

export default function Podcasts({ allPodcasts }) {
  return (
    <div className="bg-white">
      <div className="max-w-7xl mx-auto py-12 px-4 text-center sm:px-6 lg:px-8 lg:py-24">
        <div className="space-y-8 sm:space-y-12">
          <div className="space-y-10 sm:mx-auto sm:max-w-xl sm:space-y-4 lg:max-w-5xl">
            <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
              The Podcasts
            </h2>
          </div>
          <ul className="mx-auto grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 md:gap-x-6 lg:max-w-5xl lg:gap-x-12 lg:gap-y-12 xl:grid-cols-4">
            {allPodcasts.map((podcastItem) => (
              <PodcastItem
                imageUrl={podcastItem.metadata.image.url}
                podcastName={podcastItem.metadata.name}
                slug={podcastItem.slug}
              />
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
