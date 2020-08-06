import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/running/current.nhn"

response = requests.get(url)

soup = BeautifulSoup(response.text,"html.parser")

movie_list = soup.select("dt[class=tit] > a")

cut_movie=[]
count=0
for i in movie_list:
    link = i.get("href").split('code=')[1]
    name = i.text
    cut_movie.append({"title":name, "code":link})
    count+=1


headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=ET35ULQSGT7V4; NRTK=ag#20s_gr#2_ma#0_si#0_en#0_sp#0; ASID=7d8801ba00000173222173040000005f; _fbp=fb.1.1594080518895.593955966; NaverSuggestUse=use%26unuse; _ga=GA1.1.1742802988.1596162534; _ga_7VKFYR6RV1=GS1.1.1596162534.1.1.1596162555.39; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nx_ssl=2; BMR=s=1596630572413&r=https%3A%2F%2Fm.post.naver.com%2Fviewer%2FpostView.nhn%3FvolumeNo%3D28914002%26memberNo%3D1972782%26vType%3DVERTICAL&r2=https%3A%2F%2Fsearch.naver.com%2Fsearch.naver%3Fwhere%3Dnexearch%26sm%3Dtab_lve.ag20sgrpma0si0en0sp0%26ie%3Dutf8%26query%3D%25EC%25BB%25A8%25EB%25B2%2584%25EC%258A%25A4; page_uid=UyqFUwprvmsssbb0vKhssssssLV-217256; JSESSIONID=0F4A8391C2FC66B5416E5FEBE5ACB984; csrf_token=5483ea43-7397-4558-a299-7826a4972f28',
}



#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=189069&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false', headers=headers)
all_review=[]
for movie in cut_movie:
    movie_code = movie['code']
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    # print(response)

    review_soup = BeautifulSoup(response.text,"html.parser")

    review_list = review_soup.select("body > div > div > div.score_result > ul > li")

    for review in review_list:
        score = review.select_one("div[class=star_score] > em").text
        reple = review.select_one('div[class=score_reple] > p').text.strip().replace("\t","").replace("\n","").replace("\r","")
        
        one_review ={"score":score, "reple":reple}
        all_review.append(one_review)
        
print(all_review)

