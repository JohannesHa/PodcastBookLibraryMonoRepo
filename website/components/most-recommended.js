import MostRecommendedItem from "./most-recommended-item";

export default function MostRecommended() {
  return (
    <div className="bg-white">
      <div className="mx-auto py-12 px-4 max-w-7xl sm:px-6 lg:px-8 lg:py-24">
        <div className="space-y-12">
          <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
            Most Recommended Books
          </h2>
          <ul className="space-y-12 lg:grid lg:grid-cols-5 lg:items-start lg:gap-x-8 lg:gap-y-12 lg:space-y-0">
            <MostRecommendedItem
              imageName="thebeginningofinfinity.jpeg"
              amazonUrl="https://amzn.to/3d8pyby"
              bookName="The Beginning of Infinity"
            />
            <MostRecommendedItem
              imageName="1984.jpeg"
              amazonUrl="https://amzn.to/2MjL16f"
              bookName="1984"
            />
            <MostRecommendedItem
              imageName="atlasshrugged.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="Atlas Shrugged"
            />
            <MostRecommendedItem
              imageName="contact.jpeg"
              amazonUrl="https://amzn.to/3lOTvOn"
              bookName="Contact"
            />
            <MostRecommendedItem
              imageName="dune.jpeg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="Dune"
            />
            <MostRecommendedItem
              imageName="infinitejest.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="Infinite Jest"
            />
            <MostRecommendedItem
              imageName="anewkindofscience.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="A New Kind of Science"
            />
            <MostRecommendedItem
              imageName="thewarofart.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="The War of Art"
            />
            <MostRecommendedItem
              imageName="life30.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="Life 3.0"
            />
            <MostRecommendedItem
              imageName="themasterandmagherita.jpg"
              amazonUrl="https://amzn.to/2INAFdg"
              bookName="The Master and Margarita"
            />
          </ul>
        </div>
      </div>
    </div>
  );
}
