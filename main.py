import requests
import os
from Utils.ScreenshotGen import get_screenshot

apiservers =['api1','api2','api3']

def getJson(url):
    print("Getting", url)
    i = 0
    while i < 5:
        i += 1
        try:
            r = requests.get(url)
            data = r.json()
            return data
        except:
            url=url.replace('api','api1').replace('api1','api2').replace('api2','api3').replace('api3','api').replace('api','api1')
            print("Retrying", i, url)
            continue
    
    raise Exception("Failed to get json", url)

def generateThumbnailsOfAnime(animeid):
    url ='https://api.anime-dex.workers.dev/anime/' + animeid
    data = getJson(url)['results']

    episodes = data['episodes']
    for episode in episodes:
        episodeid = episode[1]

        # checking if thumbnail already exists
        if os.path.exists(f"./Thumbnails/{animeid}/{episodeid}.jpg"):
            print("Skipping", episodeid)
            continue
        
        ss =get_screenshot(episodeid)

        # checking if anime folder exists
        if not os.path.exists(f"./Thumbnails/{animeid}"):
            os.makedirs(f"./Thumbnails/{animeid}")

        os.rename(ss, f"./Thumbnails/{animeid}/{episodeid}.jpg")
        print("Downloaded", episodeid)


# generateThumbnailsOfAnime('horimiya-dub')
        
def updateThumbnail(episodeid):
    animeid, episode = episodeid.split("-episode-")

    ss = get_screenshot(episodeid)

    # checking if anime folder exists
    if not os.path.exists(f"./Thumbnails/{animeid}"):
        os.makedirs(f"./Thumbnails/{animeid}")

    
    # checking if thumbnail already exists
    if os.path.exists(f"./Thumbnails/{animeid}/{episodeid}.jpg"):
        os.remove(f"./Thumbnails/{animeid}/{episodeid}.jpg")

    os.rename(ss, f"./Thumbnails/{animeid}/{episodeid}.jpg")
    print("Updated", episodeid)

# updateThumbnail('horimiya-episode-1')
    

def getPopularAnimes(page):
    url = 'https://api.anime-dex.workers.dev/gogoPopular/' + str(page)
    data = getJson(url)['results']
    
    for anime in data:
        try:
            animeid = anime['id']
            generateThumbnailsOfAnime(animeid)
        except:
            print("Failed to download", animeid)
            continue


if __name__ == '__main__':
    # Change gitignore
    content ='''*.pyc'''
    
    with open('.gitignore', 'w') as f:
        f.write(content)

    with open('PopularPagesDone.txt', 'r') as f:
        page = int(f.read())

    page += 1
    getPopularAnimes(page)

    with open('PopularPagesDone.txt', 'w') as f:
        f.write(str(page))

    print("Done")