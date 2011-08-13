"""
=======================
epuby

A simple Python library to read/extract html
from epub files.

=======================

Authors:
  Craig Weber (owner)
  Started on Tue Jul 19, 2011
"""

import urllib2
import os
from zipfile import ZipFile
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

EPUB_PREFIX = 'OEBPS'

class Document():
    def __init__(self, filename=None, file_obj=None):
        # Open Document
        self.orig = None
        if filename:
            self.orig = open(filename, 'rB')
        elif file_obj:
            self.orig = file_obj
        else:
            raise Exception('Please supply either filename, url, or file_obj as a kwarg.')
        # Load Manifest
        self.contents = ZipFile(self.orig, 'r')
        self.manifest = self.get_manifest()
        self.extracted = None
        
    def extract(self, extract_path, filter_func=lambda name: True):
        """ 
        Extract contents into path. Returns namelist of files.
        Filter is an optional kwarg to limit extracted files using filter() """
        namelist = self.contents.namelist()
        namelist = filter(filter_func, namelist)
        # Extract all files
        self.contents.extractall(extract_path, namelist)
        self.extracted = extract_path
        return namelist
        
    def get_manifest(self):
        """ Get Manifest (wrapped in BeautifulStoneSoup) """
        namelist = self.get_namelist()
        for name in namelist:
            if name.endswith('.opf'):
                manifest_name = name
                break
        manifest = self.contents.open(manifest_name)
        return BeautifulStoneSoup(manifest.read())
        
    def open(self, filename):
        if not filename.startswith(EPUB_PREFIX):
            filename = os.path.join(EPUB_PREFIX, filename)
        return self.contents.open(filename)
        
    def get_namelist(self, filter_func=lambda name: True):
        namelist = self.contents.namelist()
        namelist = filter(filter_func, namelist)
        return namelist
        
    def get_uuid(self):
        """ Get UUID as a string """
        uuid_id = self.manifest.find('package')['unique-identifier']
        uuid_tag = self.manifest.find(id=uuid_id).contents[0]
        try:
            return uuid_tag.split(":")[:1:-1][0]
        except:
            return uuid_tag
        
    def get_cover(self):
        """ Get cover image as a file like object """
        return self.contents.open(self.get_cover_path())
        
    def get_cover_path(self):
        """ Get cover image path """
        cover_path = self.manifest.find('meta', {'name':'cover'})['content']
        cover_path = self.manifest.find(id=cover_path)['href']
        if cover_path.startswith(EPUB_PREFIX):
            return cover_path
        return os.path.join(EPUB_PREFIX, cover_path)
        
    def get_title(self):
        return self.manifest.find('dc:title').contents[0]
        
    def get_chapters(self):
        """
        Returns list of all filenames in the manifest
        to get the filename, access the href attribute of
        each item in the list.
        """
        ids = self.manifest.findAll('itemref', idref=lambda idref: idref != 'cover')
        chapters = map(lambda tag: self.manifest.find(id=tag['idref'])['href'], ids)
        return chapters