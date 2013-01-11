#!/usr/bin/python

'''Mangafox Download Script by Kunal Sarkhel <theninja@bluedevs.net>'''

import sys
import os
import requests
import glob
import shutil
from zipfile import ZipFile
from bs4 import BeautifulSoup

URL_BASE = "http://mangafox.me/"
WORKING_DIR = os.getcwd()

def get_page_soup(url):
    """Download a page and return the soup"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return soup

def get_chapter_urls(manga_name):
    """Get the chapter list for a manga"""
    url = "{0}manga/{1}?no_warning=1".format(URL_BASE, manga_name.lower())
    print "Source: " + url
    soup = get_page_soup(url)
    chapters = []
    links = soup.find_all('a',{"class": "tips"},href=True)

    for link in links:
        chapters.append(link['href'])

    if(len(links) == 0):
        print "Warning: Manga either unable to be found, or no chapters - please check the url above";
    return list(set(chapters)) # ugly yo-yo code to remove duplicates


def get_page_numbers(chapter):
    """Return the list of page numbers from the parsed page"""
    raw = chapter.find_all('select', {'class': 'm'})[0]
    raw_options = raw.find_all('option')
    pages = []
    for html in raw_options:
        pages.append(html['value'])
    pages.pop()
    return pages


def get_chapter_image_urls(url_fragment):
    """Find all image urls of a chapter and return them"""
    print "Getting chapter URLs"
    url_fragment = os.path.dirname(url_fragment) + "/"
    chapter_url = url_fragment
    chapter = get_page_soup(chapter_url)
    pages = get_page_numbers(chapter)
    image_urls = []
    for page in pages:
        print "[Page: {0}] Getting URL from {1}{2}".format(page.zfill(2), url_fragment, page)
        page_soup = get_page_soup(chapter_url + page + ".html")
        images = page_soup.find_all('img', {'id': 'image'})
        image_urls.append(images[0]['src'])
    return image_urls


def get_chapter_number(url_fragment):
    """Parse the url fragment and return the chapter number."""
    return ''.join(url_fragment.rsplit("/")[3:-1])


def download_urls(image_urls, manga_name, chapter_number):
    """Download all images from a list"""
    num = 1
    os.makedirs("{0}/{1}/".format(manga_name, chapter_number))
    for url in image_urls:
        filename = "/{0}/{1}/{2:03}.jpg".format(manga_name,
                                                 chapter_number,
                                                 num)
        download_path_with_filename = WORKING_DIR + filename
        r = requests.get(url)
        if r.status_code == 200:
            print "Downloading image #{0} - {1}KB".format(num.zfill(2), len(r.content)/1024)
            with open(download_path_with_filename, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
        num = num + 1


def makecbz(dirname, chapter_number):
    """Create CBZ files for all files in a directory."""
    dirname = os.path.abspath(dirname)
    zipname = dirname + '.cbz'
    images = glob.glob(dirname + "/*.jpg")
    myzip = ZipFile(zipname, 'w')
    for filename in images:
        print "Adding {0} to CBZ archive: ".format(chapter_number)
        myzip.write(filename)
    myzip.close()


def download_manga_range(manga_name, range_start, range_end):
    """Download a range of a chapters"""
    print "Getting chapter urls"
    chapter_urls = get_chapter_urls(manga_name)
    chapter_urls.sort()
    for url_fragment in chapter_urls[int(range_start)-1:int(range_end)+1]:
        chapter_number = get_chapter_number(url_fragment)
        print("===============================================")
        print("Chapter " + chapter_number)
        print("===============================================")
        image_urls = get_chapter_image_urls(url_fragment)
        download_urls(image_urls, manga_name, chapter_number)
        download_dir = WORKING_DIR + "/{0}/{1}".format(manga_name, chapter_number)
        makecbz(download_dir, chapter_number)
        shutil.rmtree(download_dir)
    cleanup_error_html(WORKING_DIR)


def download_manga(manga_name, chapter_number=None):
    """Download all chapters of a manga"""
    manga_name.replace (" ", "_")
    print "Assuming name is: " + manga_name
    chapter_urls = get_chapter_urls(manga_name)
    chapter_urls.sort()
    if chapter_number:
        url_fragment = chapter_urls[int(chapter_number)-1]
        chapter_number = get_chapter_number(url_fragment)
        print("===============================================")
        print("Chapter " + chapter_number)
        print("===============================================")
        image_urls = get_chapter_image_urls(url_fragment)
        download_urls(image_urls, manga_name, chapter_number)
        download_dir = WORKING_DIR + "/{0}/{1}".format(manga_name, chapter_number)
        makecbz(download_dir, chapter_number)
        shutil.rmtree(download_dir)
    else:
        for url_fragment in chapter_urls:
            chapter_number = get_chapter_number(url_fragment)
            print("===============================================")
            print("Chapter " + chapter_number)
            print("===============================================")
            image_urls = get_chapter_image_urls(url_fragment)
            download_urls(image_urls, manga_name, chapter_number)
            download_dir = WORKING_DIR + "/{0}/{1}".format(manga_name, chapter_number)
            makecbz(download_dir, chapter_number)
            shutil.rmtree(download_dir)
        cleanup_error_html(WORKING_DIR)

def cleanup_error_html(filepath):
    if os.path.exists(filepath + "/page.html"):
        os.remove("page.html")


if __name__ == '__main__':
    if len(sys.argv) == 4:
        download_manga_range(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        download_manga(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        download_manga(sys.argv[1])
    else:
        print("USAGE: mfdl.py [MANGA_NAME]")
        print("       mfdl.py [MANGA_NAME] [CHAPTER_NUMBER]")
        print("       mfdl.py [MANGA_NAME] [RANGE_START] [RANGE_END]")
