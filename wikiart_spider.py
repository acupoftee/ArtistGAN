# Paintings for this beautiful experiment are from  https://www.wikiart.org/en/paintings-by-genre/ 
# 1000 images from each genre will be used
# Usually you'll need about 1000 images for a good GAN

import os
import urllib
import itertools
import bs4
import multiprocessing

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

# a list of tuples containing the name of the genre and the number of pages
# 1000 pages for each genre will make a goog GAN
# genres = [('portrait', 1000),
#         ('landscape', 1000),
#         ('genre-painting', 1000),
#         ('abstract', 1000),
#         ('landscape', 1000),
#         ('landscape', 1000),]

pages = 1000

genres = ['portrait',
'landscape',
'genre-painting',
'abstract',
'religious-painting',
'cityscape',
'sketch-and-study',
'figurative',
'illustration',
'still-life',
'design',
'nude-painting-nu',
'mythological-painting',
'marina',
'animal-painting',
'flower-painting',
'self-portrait',
'installation',
'photo',
'allegorical-painting',
'history-painting']

def get_paintings(count, genre):
    """Get a list of paintings to scrape using the website layout as of January 21, 2018"""
    try:
        url = "https://www.wikiart.org/en/paintings-by-genre/"+ genre_ "/" + str(count)
        soup = BeautifulSoup(urllib.request.urlopen(url), "lxml")
        complete = 0
        urls = []
        for item in str(soup.findAll()).split():
            if item == "data" or complete == 1:
                complete = 1
                if "}];" in item:
                    break
                if "https" in item:
                    link = "http" + item[6:-2]
                    urls.append(link)
                    count += 1
        return urls
    except Exception as e:
        print('Failed to find the following genre and pages: '+genre+str(count))

def download_images(link, genre):
    """Download and save images given its url"""
    item, file = link
    name = file.split('/')
    savename = ''
    if len(name) == 6:
        savename = genre+"/"+ name[4] + "+" + name[5].split('.')[0] + ".jpg"
    if len(name) == 5:
        savename = genre+"/"+ name[4].split('.')[0] + ".jpg"
    if len(name) == 7:
        savename = genre+"/"+ name[5] + "+" + name[6].split('.')[0] + ".jpg"
    
    print(genre + str(item) + "-------" + str(savename))

    try:
        urllib.request.urlretrieve(file, savename)
    except Exception:
        ofile = file
        file = urllib.parse.urlsplit(file)
        file = list(file)
        file[2] = urllib.parse.quote(file[2])
        file = urllib.parse.urlunsplit(file)
        try:
            urllib.request.urlretrieve(file,savename)
            print('Retrieved on the second try for ' + file)
        except Exception:
            print('Failed on the second try for ' + file)

def multitasker(genre):
    """Runs url retriever and image downlaoder in parallel"""
    pool = ThreadPool(multiprocessing.cpu_count() - 1)
    numbers = list(range(1,pages))
    old_results = pool.starmap(get_paintings, zip(numbers, itertools.repeat(genre)))
    pool.close()
    pool.join()

    # build url list with passing results
    new_results = []
    for j in results:
        if j:
            for i in j:
                new_results.append(i)
    
    pool = ThreadPool(multiprocessing.cpu_count() - 1)
    numbers = list(range(1,pages))
    old_results = pool.starmap(download_images, zip(enumerate(new_results), itertools.repeat(genre)))
    pool.close()
    pool.join()

if __name__ == "__main__":
    print("Commence download! Mwahaha...")
    for g in genres:
        if not os.path.exists("./"+g):
            os.mkdir(g)
        if not os.path.exists("./"+g+"/images"):
            os.mkdir(g+"/images/")
        multitasker(g)



    