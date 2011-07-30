from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.conf import settings
from images import Image, Grid
from PIL import Image as ImageCalc
import os
import models

# Serve image at specified size
def serve_image(request, filename, width=None, height=None, root=settings.MEDIA_ROOT):
    width, height = int(width), int(height)
    # Sanitize file path
    filename = filename.replace("/../", "/")
    filename = filename.replace("//", "/")
    while filename.startswith(os.sep):
        filename = filename[1:]
    # open with PIL
    image = Image.open(filename, root=root)
    if width:
        # Scale height
        if not height:
            height = image.scale_height(width)
        resized = image.resize(width, height)
    else:
        resized = image.image
    # Return the response
    response = HttpResponse(mimetype="image/jpg")
    resized.save(response, "JPEG")
    return response
    
# Crops an image to the right size, instead of distorting
def serve_crop(request, filename, width, height, root=settings.MEDIA_ROOT):
    width, height = int(width), int(height)
    filename = filename.replace("/../", "/")
    filename = filename.replace("//", "/")
    while filename.startswith(os.sep):
        filename = filename[1:]
    image = Image.open(filename, root=root)
    image = image.image.transform((width, height), ImageCalc.EXTENT, (0, 0, image.image.size[0], image.image.size[1]))
    # Return the response
    response = HttpResponse(mimetype="image/jpg")
    image.save(response, "JPEG")
    return response

# Serve a solid black image at the specified size
def black(request, width, height):
    width, height = int(width), int(height)
    black = ImageCalc.new("RGB", (width, height))
    # Return the response
    response = HttpResponse(mimetype="image/png")
    black.save(response, "PNG")
    return response

# Redirect to cover of issue    
def view_issue(request, issue):
    article = models.Issue.objects.get(id=issue).articles.all()[0]
    return redirect('djTreesaver.views.issue_cover', issue=issue)

# Serve article
def view_article(request, issue, slug):
    article = models.Article.objects.get(slug=slug, issue__pk=issue)
    return render_to_response('article.html', {'article':article}, context_instance=RequestContext(request))

# Serve issue toc
def issue_toc(request, issue):
    issue = models.Issue.objects.get(id=issue)
    return render_to_response('toc.html', {'issue':issue}, context_instance=RequestContext(request))

# Serve Cover Image Grid
def issue_cover(request, issue):
    cover_image = models.Issue.objects.get(id=issue).cover
    return render_to_response('cover.html', {'cover':cover_image}, context_instance=RequestContext(request))

# Treesaver Resources File, containing grids and metadata
def resources(request, issue):
    context = {
        'grids' : models.Grid.objects.all(),
        'publication' : models.Issue.objects.get(id=issue).publication,
    }
    return render_to_response('resources.html', context, context_instance=RequestContext(request))

    