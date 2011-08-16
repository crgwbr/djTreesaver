from django.conf import settings
from django.conf.urls.defaults import *
import os

# Activate Custom Settings
from djTreesaver import settings as ts_settings

path = os.path.realpath(os.path.dirname(__file__))

urlpatterns = patterns('',
    # Files
    url(r'^treesaver.css$', 'django.views.static.serve', { 'document_root':os.path.join(path, 'css'),    'path':'treesaver.css', }),
    url(r'^treesaver.js$',  'django.views.static.serve', { 'document_root':os.path.join(path, 'static'), 'path':'treesaver.js', }),
    url(r'^ui.js$',         'django.views.static.serve', { 'document_root':os.path.join(path, 'static'), 'path':'ui.js', }),
    url(r'^static/(?P<path>.+)$', 'django.views.static.serve', { 'document_root':os.path.join(path, 'static')}),
    
    # Images
    url(r'^thumb/(?P<width>[0-9]+)/(?P<height>[0-9]+)/(?P<filename>.+)$', 'djTreesaver.views.serve_crop'),
    url(r'^img/(?P<width>[0-9]+)/(?P<height>[0-9]+)/black/$',             'djTreesaver.views.black'),
    url(r'^img/(?P<width>[0-9]+)/(?P<height>[0-9]+)/(?P<filename>.+)$',   'djTreesaver.views.serve_image'),
    url(r'^img/(?P<width>[0-9]+)/(?P<filename>.+)$',                      'djTreesaver.views.serve_image'),
    url(r'^img/(?P<filename>.+)$',                                        'djTreesaver.views.serve_image'),
    
    # Views
    url(r'^issue/(?P<issue>[0-9]+)/$',               'djTreesaver.views.view_issue'),
    url(r'^issue/(?P<issue>[0-9]+)/ts-cover.html$',  'djTreesaver.views.issue_cover'),
    url(r'^issue/(?P<issue>[0-9]+)/toc.html$',       'djTreesaver.views.issue_toc'),
    url(r'^issue/(?P<issue>[0-9]+)/resources.html$', 'djTreesaver.views.resources'),
    url(r'^issue/(?P<issue>[0-9]+)/(?P<slug>[0-9a-zA-Z\.\_\-\/]+)$', 'djTreesaver.views.view_article'),
)
