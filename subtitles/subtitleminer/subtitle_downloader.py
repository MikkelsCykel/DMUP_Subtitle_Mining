from subtitleminer.auxillary import DB, Log, System
import urllib2
from time import sleep
import re
import requests
import zipfile
from BeautifulSoup import BeautifulSoup
import os


class SubtitleDownloader(object):

    system = System()
    db = DB()
    log = Log()

    @classmethod
    def fetch_download_url_from_html(cls, hdr, links, returnName):
        """


        :rtype : object
        :param hdr:
        :param links:
        :return:
        """
        req2 = urllib2.Request(links[0], headers=hdr)
        html = urllib2.urlopen(req2).read()
        soup = BeautifulSoup(html)
        # Find download link in html using the soup
        download_link = soup.find(
            'table',
            {'class': 'table'}
        ).findAll('tr')[1].find('a',
                                {'class': re.compile(r'\bbtn\b')}).get('href')

        return download_link

    @classmethod
    def download_subtitle_in_srt_from_movie_name(cls, name):

        """

        :rtype : object
        """
        url = cls.system.generate_subtitle_url_from_movie_name(name=name)
        print url
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                          'AppleWebKit/537.11 (KHTML, like Gecko)'
                          'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,\
                       application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

        regex = '<link>(.*)<'

        try:

            req = urllib2.Request(url, headers=hdr)
            xml = urllib2.urlopen(req).read()

            links = [l for l in re.findall(regex, xml) if len(l) > 25]

            download_link = cls.fetch_download_url_from_html(hdr, links)

            download_link = cls.fetch_download_url_from_html(hdr, links)

            zip_name = cls.__download_zipped_subtitle(url=download_link)

            srt_name = cls.__extract_srt_from_zip_file(file_name=zip_name)

            return srt_name

        except Exception as e:
            cls.log.writeToLog(message=e, where="Download error from :" + name)
            return 0

    @classmethod
    def __download_zipped_subtitle(cls, url):

        try:
            # generate a random name for each to avoid race conditions
            name = '../data/subtitles/%s.zip'\
                   % (cls.system.generateRandomAlphanumericString(length=15))
            # fetch zip and save to file
            r = requests.get(url)
            with open(name, "wb") as code:
                code.write(r.content)
            return name
        except Exception as e:
            cls.log.writeToLog(message=e, where="Download zipped error from :"
                                                + url)
            return 0

    @classmethod
    def __extract_srt_from_zip_file(cls, file_name):
        try:
            binaries = open(file_name, 'rb')
            zip_file = zipfile.ZipFile(binaries)
            inner_files = zip_file.namelist()

            # TODO: add suport for .SUB
            srt_name = [x for x in inner_files if x[-3:] == 'srt'][0]
            # escape filename in order to insert into DB later
            # srt_name_escaped =
            # cls.system.remove_illegal_search_chars(srt_name)
            zip_file.extract(srt_name, path="../data/subtitles/")
            binaries.close()
            # rename file to fit DB insert name
            # os.rename(srt_name, srt_name_escaped)
            os.remove(file_name)
            return srt_name
        except Exception as e:
            cls.log.writeToLog(message=e, where="extract zipped error from :"
                                                + file_name)
            sleep(120)
            return 0
