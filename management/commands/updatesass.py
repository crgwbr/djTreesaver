from django.core.management.base import BaseCommand, CommandError
from djTreesaver import css, models

class Command(BaseCommand):
    args = '<>'
    help = 'Recompiles the Seasons CSS Framework on-demand'

    def handle(self, *args, **options):
        self.stdout.write('Recompiling Sass to CSS...\n')
        grids = models.Grid.objects.all()
        css.compile_sass(grids)