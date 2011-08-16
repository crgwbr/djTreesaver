# djTreesaver Settings
# Gets appended to django.conf.settings
from django.conf import settings
import os

class TreesaverSettings():
    # Get Path
    path = os.path.realpath(os.path.dirname(__file__))
    
    # Append our templates folder
    TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS)
    TEMPLATE_DIRS.append(os.path.join(path, 'templates'))
    settings.TEMPLATE_DIRS = TEMPLATE_DIRS

    # Default Grid
    DEFAULT_GRID = "feature1"
    
settings.TREESAVER = TreesaverSettings()