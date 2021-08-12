const MostRecommendedItem = ({ imageName, bookName, amazonUrl }) => {
  return (
    <li>
      <a href={amazonUrl}>
        <div className="space-y-4 sm:gap-6 sm:space-y-0 lg:gap-8">
          <div className="aspect-w-3 aspect-h-2 sm:aspect-w-3">
            <img
              className="object-cover shadow-lg rounded-lg mb-4"
              src={`media/sampleImages/books/${imageName}`}
              alt=""
            />
            <div className="sm:col-span-1">
              <div className="space-y-4">
                <div className="text-lg leading-6 font-medium space-y-1">
                  <h3>{bookName}</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </a>
    </li>
  );
};

export default MostRecommendedItem;
