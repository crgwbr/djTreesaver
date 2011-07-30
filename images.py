"""
Generates multiple image sizes for use with Treesaver

Authors:
  See __init__.py
"""

from PIL import Image as ImageCalc
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404
import os

class Grid():
    def __init__(self, column_width, gutter_width, image_widths=None):
        self.column = column_width
        self.gutter = gutter_width
        if not image_widths:
            image_widths = {
                'single' : 3,
                'double' : 6,
                'triple' : 9,
                'quad'   : 12,
            }
        self.sizes = image_widths
        
    def add_image_size(self, name, width):
        self.sizes[name] = width
        return self.widths()
        
    def widths(self):
        calc_pixels = lambda (key, value): (key, (value * self.column) + ((value-1) * self.gutter))
        return dict(map(calc_pixels, self.sizes.iteritems()))
        

class Image():
    def __init__(self, image, root, filename):
        self.image = image
        self.root = root
        self.filename = filename
        
    @classmethod
    def open(cls, filename, root=settings.MEDIA_ROOT):
        """ Instantiate from an existing file """
        path = os.path.join(root, filename)
        try:
            image = ImageCalc.open(path)
        except:
            raise Http404()
        return cls(image, root, filename)
        
    def resize(self, width, height):
        """ Resize an image and returns pixel data in a UTF-8 string """
        width, height = int(width), int(height)
        return self.image.resize((width, height), ImageCalc.ANTIALIAS)
        
    def scale_height(self, new_width):
        """ Returns scaled height for given width"""
        width, height = self.image.size
        aspect = float(height) / width
        return int(new_width) * aspect
        
    def scale_width(self, new_height):
        """ Returns scaled width for given height"""
        width, height = self.image.size
        aspect = float(width) / height
        return int(new_height) * aspect
    
    def figure(self, grid, zoomable=True, alt="", title=""):
        if zoomable:
            html = "<figure class=\"zoomable\">\n"
        else:
            html = "<figure>\n"
        
        assemble_img = lambda attrs: "  <img " + " ".join(map(lambda attr: '%s="%s"' % attr, attrs.iteritems())) + " />"
        def build_img_tag(item):
            print item
            cols, width = item
            height = self.scale_height(width)
            width, height = int(width), int(height)
            if width > self.image.size[0] or height > self.image.size[1]:
                return ""
            attrs = {
                'data-sizes'     : cols,
                'data-minWidth'  : width,
                'data-minHeight' : height,
                'data-src'       : reverse('djTreesaver.views.serve_image', kwargs={'filename':self.filename, 'height':height, 'width':width}),
                'width'          : width,
                'height'         : height,
                'alt'            : alt,
                'title'          : title,
            }
            return assemble_img(attrs)
        html = html + "\n".join(map(build_img_tag, grid.widths().iteritems())) + "\n</figure>"
        return html
        
