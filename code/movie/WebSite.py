import requests
from bs4 import BeautifulSoup


# 逻辑要重新写，从movie的detail页面去获取movie的详细信息
def get_movies(url):
    # print(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    schedule = soup.find("div", id="theatersArea")
    print(schedule)

    # for movies_content in soup.find_all(id="cinemas"):
        # print("===========\n" + movies_content.__str__())
        # print(type(movies_content))
        # print(movies_content.__sizeof__())

         # print("*** " + movies_content)
    # movie_items = soup.find_all("li", class_="cinema")
    # movie_list = []
    # for i in movie_items:
    #     # print(i)
    #     movie = Movie()
    #     movie.name = i.select('span[itemprop="name"]')[0].text
    #     movie.mtrcbRating = i.select('.mtrcbRating')[0].text
    #     movie.image = i.find("meta", itemprop="image", content=True)["content"]
    #     movie.genre = i.select('.genre')[0].text
    #     movie.running_time = i.select('.running_time')[0].text
    #
    #     for director in i.select('span[itemprop="director"]'):
    #         # print("---", director)
    #         movie.directors.append(director.text)
    #     print("movie : ", movie)
    #     movie_list.append(movie)
    #
    # return movie_list









