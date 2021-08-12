Based on this repository: https://github.com/vercel/next.js/tree/canary/examples/cms-cosmic

### A statically generated website using Next.js, React, Cosmic and TailwindCSS

## Demo

[https://podcast-book-recommendation-website-new.vercel.app/](https://podcast-book-recommendation-website-new.vercel.app/)

## Deploy your own

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/git/external?repository-url=https://github.com/JohannesHa/PodcastBookRecommendationWebsiteNEW&project-name=podcast-book-recommendation-website&env=COSMIC_BUCKET_SLUG,COSMIC_READ_KEY,COSMIC_PREVIEW_SECRET&envDescription=Required%20to%20connect%20the%20app%20with%20Cosmic&envLink=https://vercel.link/cms-cosmic-env)

## Configuration

Set each variable on `.env.local`:

- `COSMIC_BUCKET_SLUG` should be the **Bucket slug** key under **Basic Settings**.
- `COSMIC_READ_KEY` should be the **Read Key** under **API Access**.
- `COSMIC_PREVIEW_SECRET` can be any random string (but avoid spaces) - this is used for [Preview Mode](https://nextjs.org/docs/advanced-features/preview-mode).

Your `.env.local` file should look like this:

```bash
COSMIC_BUCKET_SLUG=...
COSMIC_READ_KEY=...
COSMIC_PREVIEW_SECRET=...
```

### Run Next.js in development mode

```bash
npm install
npm run dev

# or

yarn install
yarn dev
```

The website should be up and running on [http://localhost:3000](http://localhost:3000)!
