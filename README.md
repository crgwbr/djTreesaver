# djTreesaver

## Introduction

djTreesaver is a plugin Django app that makes publishing content to Treesaver.js quick and easy.  It includes all the required models, views, and templates for creating a Treesaver publication.  It even allows you to upload epub files and automatically convert them into Treesaver documents.

## Requirements

    django :: https://www.djangoproject.com/
    BeautifulSoup :: http://www.crummy.com/software/BeautifulSoup/
    PIL :: http://www.pythonware.com/products/pil/
    Sass :: http://sass-lang.com/

## Installation

1. Copy the djTreesaver directory into your Django Project.

2. Make sure `MEDIA_ROOT` and `MEDIA_URL` are set correctly in your settings.py file.  djTreesaver will create 3 sub directories here to store uploaded files: epubs, grids, and images.  epubs stores uploaded epub files.  grids stores uploaded article grid html files and the associated Sass file.  images contains image files that are linked to an article.

3. Add djTreesaver to your installed apps tuple

        INSTALLED_APPS = (
	    ...
	    'djTreesaver',
	    ...
	)
	
4. Add the djTreesaver urls file to your urls.py file

        urlpatterns = patterns('',    
	    # djTreesaver
	    (r'^treesaver/', include('djTreesaver.urls')),
	    ...
	)
	
5. From the Django Admin Site, upload a Treesaver grid by using the DjTreesaver -> Grids form.  You can use one of the example grids in the djTreesaver/example_grids/ directory.  You can read more about grids here: http://treesaverjs.com/
	
## Usage

*Converting an Epub*

From the Django Admin Site, upload an epub to DjTreesaver -> Epub form.  Select a publication to categorize the epub.  For example, if you upload Minority Report by Philip K. Dick, you might want to select a publication called Science Fiction or Classics.  If the Epub is an issue of a periodical, the publication should be the name of the periodical.

Once the epub is uploaded and saved, you'll find issue in DjTreesaver -> Issue's.  Take note of the issue's primary key and navigate to `/treesaver/issue/<pk>/`, for example, `/treesaver/issue/1/`.  

*Manually creating an issue*

Manually creating a Treesaver issue is almost as easy as uploading an epub:

    from djTreesaver.models import Image, Publication, Issue, Article
    from django.core.files.base import ContentFile
    from django.core.urlresolvers import reverse
    
    haxor_monthly = Publication(name="Haxor Monthly")
    haxor_monthly.save()

    july_cover = Image()
    july_cover.image.save('/some/dir/tory/', ContentFile(file_object.read()))
    july_cover.alt = "Alt Text"
    july_cover.title = "Title Text"
    july_cover.save()

    july_issue = Issue()
    july_issue.title = "Awesomeness"
    july_issue.uuid = "0000-0000-0000-0000"
    july_issue.publication = haxor_monthly
    july_issue.cover = july_cover
    july_issue.save()

    an_image = Image()
    an_image.image.save('/some/dir/tory/', ContentFile(file_object.read()))
    an_image.alt = "Alt Text"
    an_image.title = "Title Text"
    an_image.save()

    an_article = Article()
    an_article.title = "Hello World"
    an_article.slug = "hello-world"
    an_article.author = "Craig Weber"
    an_article.issue = july_issue
    an_article.content = article_html_content_string
    an_article.images.add(an_image)  # ManyToManyField
    an_article.save()
    
    # Link to the issue like this
    issue_url = reverse('djTreesaver.views.view_issue', kwargs={'issue':july_issue.pk,})

## Credits
Thanks to Filipe Fortes and Bram Stein for Treesaver :: http://treesaverjs.com/

Seasons is created and developed by Scott Kellum in collaboration with the Treesaver team :: http://treesaver.net/

Digininja Skin / Chrome style for Seasons by Craig Weber :: http://crgwbr.com

djTreesaver for Django by Craig Weber :: http://crgwbr.com
