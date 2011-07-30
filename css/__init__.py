#!/usr/bin/python

import os, sys
from subprocess import Popen, PIPE

path = os.path.realpath(os.path.dirname(__file__))

tmpl_marker = "{{ grids }}"

tmpl_path = os.path.join(path, 'seasons', 'style.template')
sass_path = os.path.join(path, 'seasons', 'style.sass')
css_path = os.path.join(path, 'treesaver.css')

# Compile SASS -> CSS
def compile_sass(grids):
    # Open Template
    sass_tmpl = open(tmpl_path, 'rU')
    rendered_sass = sass_tmpl.read()
    sass_tmpl.close()
    # Render
    grid_sass = ""
    for grid in grids:
        grid_sass = "%s\n\n%s" % (grid_sass, grid.sass.read())
    rendered_sass = rendered_sass.replace("{{ grids }}", grid_sass)
    # Write
    sass_tmpl = open(sass_path, 'w')
    sass_tmpl.write(rendered_sass)
    sass_tmpl.close()
    # Compile
    command = "sass --style compressed --update %s:%s" % (sass_path, css_path)
    stream = Popen(command, stdout=PIPE, shell=True)
    pipe = stream.communicate()
    if pipe[0] != None: print pipe[0].strip()
    if pipe[1] != None: print pipe[1].strip()