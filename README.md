Mangafox Download Script
========================

About
-----
This is the updated version of https://github.com/techwizrd/MangaFox-Download-Script written by techwizrd. I updated the script so it's working with the new MangaFox site, replaced urllib with requests, beautifulsoup with beautifulsoup4 (New find_all method) and cleaned up the output.

Original "About" text:

    Mangafox Download Script is a manga downloader similar to my old Onemanga Download Script (although onemanga.com shut down). It works by downloading each individual page and parsing it for the image url. Then it downloads all the images.
    I created this because I prefer reading manga with the use of a viewer like Comix. I also prefer keeping manga on my hard drive in case I am not connected to the internet.


Dependencies
------------

  * Python 2.6 and up (not tested with Python 3)
  * BeautifulSoup4 (pip install beautifulsoup4)
  * [Python-Requests](http://docs.python-requests.org/)

Usage
-----
To download an entire series

    ~ $ python mfdl.py [MANGA_NAME]

To download a specific chapter (downloads wrong chapter if a manga has a strange numbering scheme like starting with 0)

    ~ $ python mfdl.py [MANGA_NAME] [CHAPTER_NUMBER]

To download a range of manga chapter (same caveats as above):

    ~ $ python mfdl.py [MANGA_NAME] [RANGE_START] [RANGE_END]

Examples
--------
Download all of Yureka::

    ~ $ python mfdl.py Yureka

Download Yureka chapter 165:

    ~ $ python mfdl.py Yureka 165

Download Yureka chapters 160-170:

    ~ $ python mfdl.py Yureka 160 170

Notes
-----
Please do not overuse and abuse this and destroy Mangafox. If you've got some cash, why not donate some to them and help them keep alive and combat server costs? I really would not like people to destroy Mangafox because of greedy downloading. Use this wisely and don't be evil.
