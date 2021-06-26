import requests
from bs4 import BeautifulSoup

'''module originally authored by Shravan Kuchkula 7/13/2019'''

def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def minMax(a):
    '''Returns the index of negative and positive review.'''

    # get the index of least rated user review
    minpos = a.index(min(a))

    # get the index of highest rated user review
    maxpos = a.index(max(a))

    return minpos, maxpos


def getReviews(soup):
    '''Function returns a negative and positive score for each review.'''

    # get a list of user scores
    user_review_ratings = [tag.previous_element for tag in
                           soup.find_all('span', attrs={'class': 'point-scale'})]

    # find the index of negative and positive review
    scoreList = list(map(int, user_review_ratings))
    n_index, p_index = minMax(scoreList)

    # get the review tags
    user_review_list = soup.find_all('a', attrs={'class': 'title'})

    # get the negative and positive review tags
    n_review_tag = user_review_list[n_index]
    p_review_tag = user_review_list[p_index]

    # return the negative and positive review link
    n_review_link = "https://www.imdb.com" + n_review_tag['href']
    p_review_link = "https://www.imdb.com" + p_review_tag['href']

    return n_review_link, p_review_link


def getReviewText(review_url):
    '''Returns the user review text given the review url.'''

    # get the review_url's soup
    soup = getSoup(review_url)

    # find div tags with class text show-more__control
    tag = soup.find('div', attrs={'class': 'text show-more__control'})

    return tag.getText()