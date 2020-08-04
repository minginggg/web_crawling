import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/running/current.nhn"

response = requests.get(url)

soup = BeautifulSoup(response.text,"html.parser")

movie_list = soup.select("dt[class=tit] > a")

cut_movie=dict()
count=0
for i in movie_list:
    link = i.get("href").split('code=')[1]
    name = i.text
    cut_movie[count] = {"title":name, "code":link}
    count+=1

print(cut_movie)