import Link from "next/link";

export default function PodcastItem({ imageUrl, podcastName, slug }) {
  return (
    <li>
      <Link href={`/podcasts/${slug}`}>
        <a>
          <div className="space-y-4">
            <img
              className="mx-auto h-32 w-32 shadow-xl rounded-lg lg:w-56 lg:h-56"
              src={imageUrl}
              alt=""
            />
            <div className="space-y-2">
              <div className="text-sm font-medium lg:text-lg">
                <h3>{podcastName}</h3>
              </div>
            </div>
          </div>
        </a>
      </Link>
    </li>
  );
}
