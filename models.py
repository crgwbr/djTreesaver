# *-* coding: iso-8859-1 *-*

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from datetime import datetime
import os
import epub
import images
import css
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


class Grid(models.Model):
    class_id = models.SlugField(max_length=200)
    upload_grid = lambda cls, filename: os.path.join('grids', '%s.grid' % filename)
    html = models.FileField(upload_to=upload_grid, help_text="File containing the HTML for the Grid.")
    upload_sass = lambda cls, filename: os.path.join('grids', '%s.sass' % filename)
    sass = models.FileField(upload_to=upload_sass, help_text="File containing the SASS for the Grid.")
    
    @classmethod
    def compile_sass(cls):
        grids = cls.objects.all()
        css.compile_sass(grids)
        
    def save(self):
        self.compile_sass()
        models.Model.save(self)
        
    def __unicode__(self):
        return self.class_id


class Image(models.Model):
    image = models.ImageField(upload_to="images")
    alt   = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
        
    def figure(self, grid=images.Grid(78, 16)):
        print self.image.path
        figure_calc = images.Image.open(str(self.image))
        return figure_calc.figure(grid, alt=self.alt, title=self.title)
    
    def __unicode__(self):
        return "%s" % self.image


class Publication(models.Model):
    name = models.CharField(max_length=200)
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
        
        
class Issue(models.Model):
    title = models.CharField(max_length=200)
    uuid = models.CharField(max_length=200)
    cover = models.ForeignKey(Image)
    publication = models.ForeignKey(Publication, related_name="issues")
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    @classmethod 
    def from_epub(cls, epub_document, publication):
        document = epub.Document(file_obj = epub_document)
        # Create instance and save
        issue = cls()
        issue.title = document.get_title()
        issue.uuid = document.get_uuid()
        issue.publication = publication
        # Process Cover
        cover_image = Image(alt="Cover", title="Cover")
        cover_image.image.save(os.path.join(issue.uuid, document.get_cover_path()), ContentFile(document.get_cover().read()))
        cover_image.save()
        issue.cover = cover_image
        issue.save()
        # Process Articles
        def file_is_good(name):
            if name.startswith(epub.EPUB_PREFIX):
                for ext in ('.xhtml', '.html', '.htm'):
                    if name.endswith(ext) and not ('cover.' in name): # Exclude the cover
                        return True
            return False
        articles = document.get_chapters()
        for filename in articles:
            article = document.open(filename)
            slug = filename.replace('%s/' % epub.EPUB_PREFIX, '')
            Article.process_epub_document(article.read(), slug, issue, document)
        issue.save()
        return issue
        
    def delete(self):
        for article in self.articles.all():
            article.images.all().delete()
        models.Model.delete(self)
    
    def __unicode__(self):
        return self.title
        
        
class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, help_text="Used in the article url")
    author = models.CharField(max_length=200, null=True, blank=True)
    issue = models.ForeignKey(Issue, related_name="articles")
    content = models.TextField(help_text="Article Content in Html")
    #is_markdown = models.BooleanField(help_text="Is the content in Markdown formatting?")
    images = models.ManyToManyField(Image, null=True, blank=True)
    grid = models.ForeignKey(Grid, null=True, blank=True)
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    @classmethod
    def process_epub_document(cls, html, slug, issue, epub_document):
        article = cls()
        soup = BeautifulSoup(html)
        article.title = soup.find('title').contents[0].encode('utf-8')
        # Fix unicode crap
        article.title = article.title.replace("-", "&ndash;")
        article.title = article.title.replace("—", "&mdash;")
        article.title = article.title.replace("”", "&quot;")
        article.title = article.title.replace("“", "&quot;")
        article.title = article.title.decode('ascii', 'ignore')
        # Save data
        article.slug = slug
        article.issue = issue
        article.content = html
        article.save()
        # Images
        namelist = epub_document.get_namelist()
        for tag in soup.findAll('img'):
            image = Image()
            find_img = lambda path: path.endswith(tag['src'])
            image_file = filter(find_img, namelist)
            if len(image_file) > 0:
                image.image.save(os.path.join(issue.uuid, image_file[0]), ContentFile(epub_document.open(image_file[0]).read()))
                image.alt = tag.get('alt', '')
                image.title = tag.get('title', '')
                image.save()
                article.images.add(image)
        article.save()
        return article
        
    # Returns thumbnail url
    def toc_image(self):
        try:
            image = self.images.all()[0]
        except:
            return reverse('djTreesaver.views.black', kwargs={'width':40, 'height':40})
        return reverse('djTreesaver.views.serve_crop', kwargs={'width':40, 'height':40, 'filename':str(image)})
        
    def get_markup(self):
        markup = BeautifulSoup(self.content)
        # Remove inline images
        [image.extract() for image in markup.findAll('img')]
        # Convert <b> to <h3>
        subheads = list(markup.findAll('p', 'ss'))
        subheads.extend(markup.findAll('p', 'st'))
        for subhead in markup.findAll('p', 'ss'):
            text = unicode(subhead.renderContents(), 'utf-8')
            new_header = unicode("<h3>%s</h3>", 'utf-8') % text
            subhead.replaceWith(new_header)
        return markup.body.renderContents()
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.issue.publication)
        
class Epub(models.Model):
    epub_file = models.FileField(upload_to="epubs", help_text="Upload an Epub Doc to be converted into a Treesaver Issue")
    publication = models.ForeignKey(Publication)
    issue = models.ForeignKey(Issue, null=True, blank=True)
    
    created  = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def save(self):
        if self.issue:
            self.issue.delete()
        issue = Issue.from_epub(self.epub_file, publication=self.publication)
        issue.save()
        self.issue = issue
        models.Model.save(self)
        
    def delete(self):
        if self.issue:
            self.issue.delete()
        models.Model.delete(self)
        
    def __unicode__(self):
        return "%s - %s" % (self.publication, self.pk)
        
        