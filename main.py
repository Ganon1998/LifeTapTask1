import itertools
import numpy as np
import pandas as pd
from imdbHelpers import *


def getMovieReviews(soupOfSite):

    # find all a-tags with class:None
    movie_tags = soupOfSite.find_all('a', attrs={'class': None})

    # filter the a-tags to get just the titles
    movie_tags = [tag.attrs['href'] for tag in movie_tags
                  if tag.attrs['href'].startswith('/review') & tag.attrs['href'].endswith('/')]

    # remove duplicates
    movie_tags = list(dict.fromkeys(movie_tags))

    base_url = "https://www.imdb.com"
    movie_links = [base_url + tag + '?ref_=tt_urv' for tag in movie_tags]


    # get all movie review texts
    movie_review_list = [getReviewText(str(i)) for i in movie_links]

    movie_review_list = list(itertools.chain(*movie_review_list))

    # label each review with negative or positive
    review_sentiment = np.array(['negative', 'positive'] * (len(movie_review_list) // 2))

    # construct a dataframe
    df = pd.DataFrame({'user_review_permalink': movie_links,
                       'user_review': movie_review_list, 'sentiment': review_sentiment})
    return df


def main():
    TitanicURL = "https://www.imdb.com/title/tt0120338/reviews?ref_=tt_ov_rt"
    reqs = requests.get(url=TitanicURL)
    soupObj = BeautifulSoup(reqs.text, 'html.parser')

    reviews = getMovieReviews(soupObj)

    return reviews


if __name__ == '__main__':
    main()