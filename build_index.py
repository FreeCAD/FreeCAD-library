#!/usr/bin/env python

# ************************************************************************
# * Copyright (c) 2022 Yorik van Havre <yorik@uncreated.net>             *
# *                                                                      *
# * This program is free software; you can redistribute it and/or modify *
# * it under the terms of the GNU Lesser General Public License (LGPL)   *
# * as published by the Free Software Foundation; either version 2 of    *
# * the License, or (at your option) any later version.                  *
# * for detail see the LICENCE text file.                                *
# *                                                                      *
# * This program is distributed in the hope that it will be useful,      *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# * GNU Library General Public License for more details.                 *
# *                                                                      *
# * You should have received a copy of the GNU Library General Public    *
# * License along with this program; if not, write to the Free Software  *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# * USA                                                                  *
# *                                                                      *
# ************************************************************************

"""This script produces an index.html file and an images/ folder which
shows and allows to download the contents of the library"""

import os
import zipfile
import hashlib
import urllib.request
import urllib.parse

# path definitions
homefolder = os.path.abspath(os.curdir)
imagefolder = "thumbnails"
htmlfile = os.path.join(homefolder, "index.html")
baseurl = "https://github.com/FreeCAD/FreeCAD-library/blob/master/"
excludelist = ["thumbnails"]

# icons
defaulticon = os.path.join(imagefolder, "freecad-document.svg")
gridicon = os.path.join(imagefolder, "icon-grid.svg")
listicon = os.path.join(imagefolder, "icon-list.svg")
stepicon = os.path.join(imagefolder, "icon-grey.svg")
brepicon = os.path.join(imagefolder, "icon-blue.svg")
stlicon = os.path.join(imagefolder, "icon-green.svg")
collapseicon = os.path.join(imagefolder, "icon-right.svg")
expandicon = os.path.join(imagefolder, "icon-down.svg")

# html template
template = """<html>
    <head>
        <title>FreeCAD Library</title>
        <style>
body {
    font-family: Arial,sans;
    color: black;
    background: white;
}
a:link, a:visited {
    color: black;
    text-decoration: none;
}
img {
    width: 16px;
}
h1, h2, h3, h4, h5, h6, .h7, .h8, .h9 {
    clear: both;
    margin: 0;
    cursor: pointer;
    font-size: 1em;
}
.collapsable {
    border-left: 1px solid grey;
    padding-left: 8px;
    margin-left: 5px;
}
.cards {
    margin: 0;
}
.card {
    float:left;
    width: 128px;
    margin: 4px;
}
.icon {
    width: 128px;
}
.hicon {
    width: 12px;
    margin-right: 4px;
}
.name {
    clear: left;
    float: left;
    overflow-wrap: break-word;
    width: 128px;
}
.links {
    float: left;
}
.fullwidth {
    width: 100% !important;
}
.smallicon {
    width: 16px !important;
    margin-right: 8px;
    float: left !important;
}
.largetext {
    clear: none !important;
    width: auto !important;
    margin-right: 8px;
}
.hidden {
    display: none;
}
.iconselected {
    border: 2px solid black;
}
        </style>
        <script>
function seticon() {
    collection = document.getElementsByClassName("card");
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.remove("fullwidth")
    }
    collection = document.getElementsByClassName("icon");
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.remove("smallicon")
    }
    collection = document.getElementsByClassName("name");
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.remove("largetext")
    }
    icon_icon = document.getElementById("icon_icon");
    icon_icon.classList.add("iconselected")
    icon_grid = document.getElementById("icon_grid");
    icon_grid.classList.remove("iconselected")
}
function setgrid() {
    collection = document.getElementsByClassName("card");
    for (let i = 0; i < collection.length; i++) {
      collection[i].classList.add("fullwidth")
    }
    collection = document.getElementsByClassName("icon");
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.add("smallicon")
    }
    collection = document.getElementsByClassName("name");
    for (let i = 0; i < collection.length; i++) {
        collection[i].classList.add("largetext")
    }
    icon_icon = document.getElementById("icon_icon");
    icon_icon.classList.remove("iconselected")
    icon_grid = document.getElementById("icon_grid");
    icon_grid.classList.add("iconselected")
}
function collapse(elt) {
    ndiv = elt.parentElement.nextSibling.nextSibling;
    if (ndiv.classList.contains("hidden")) {
        elt.src = "<!--expandicon-->";
        ndiv.classList.remove("hidden");
    } else {
        elt.src = "<!--collapseicon-->";
        ndiv.classList.add("hidden");
    }
}
        </script>
    </head>
    <body>
        <div class="nav">
            <a id="icon_icon" class="navicon iconselected" href="#" title="icon view" onclick="seticon()">
                <img src="<!--gridicon-->"/>
            </a>
            <a id="icon_grid" class="navicon" href="#" title="list view" onclick="setgrid()">
                <img src="<!--listicon-->"/>
            </a>
        </div>
<!--contents-->
    </body>
</html>"""


def build_html(dirpath, level=1):

    """walks a directory and builds cards from its contents"""

    html = ""
    if os.path.isdir(dirpath):
        html += build_title(dirpath, level)
        if level > 1:
            offset = 5 + (level - 2) * 2
            html += '<div class="collapsable hidden">\n'
        nodes = os.listdir(dirpath)
        nodes = [node for node in nodes if node[0] != "."]
        nodes = [node for node in nodes if node not in excludelist]
        nodes = [os.path.join(dirpath, node) for node in nodes]
        dirs = [node for node in nodes if os.path.isdir(node)]
        dirs = sorted(dirs)
        files = [node for node in nodes if node.lower().endswith(".fcstd")]
        files = sorted(files)
        for fpath in dirs:
            html += build_html(fpath, level+1)
        if files:
            html += '<div class="cards">\n'
            for fpath in files:
                html += build_card(fpath)
            html += '</div>\n'
        if level > 1:
            html += '</div>\n'
    return html


def build_title(dirpath, level):

    """builds an html title from a path"""

    if level == 1:
        # do not print the first-level title
        return ""
    sl = str(level)
    sn = '<img class="hicon" src="'+collapseicon+'"/>'
    sn += os.path.basename(dirpath)
    if level < 7:
        title = '<h' + sl + ' onclick="collapse(this.children[0])">'
        title += sn + '</h' + sl + '>\n'
    else:
        title = '<div class="h' + sl + '" onclick="collapse(this.children[0])">'
        title += sn + '</div>\n'
    return title


def build_card(filepath):

    """builds an HTML card for a given file"""

    print("Building card for", filepath)
    html = ""
    if os.path.exists(filepath):
        basename = os.path.splitext(filepath)[0]
        name = os.path.basename(basename)
        iconpath = get_icon(filepath)
        raw = "?raw=true"
        fileurl = baseurl + clean_path(filepath) + raw
        html += '<div class="card">'
        html += '<a title="FCSTD version" href="' + fileurl + '">'
        html += '<img class="icon" src="' + clean_path(iconpath) + '"/>'
        html += '<div class="name">' + name + '</div>'
        html += '</a>'
        html += '<div class="links">'
        exts = {'STEP': (".stp", ".step", ".STP", ".STEP"),
                'BREP': (".brp", ".brep", ".BRP", ".BREP"),
                'STL':  (".stl", ".STL")}
        icons = {'STEP': stepicon,
                 'BREP': brepicon,
                 'STL': stlicon}
        for name, exts in exts.items():
            for ext in exts:
                if os.path.exists(basename + ext):
                    exturl = baseurl + clean_path(basename + ext) + raw
                    html += ' <a href="' + exturl
                    html += '" title="' + name + ' version">'
                    html += '<img src="' + icons[name] + '"/>'
                    html += '</a>'
                    break
        html += '</div>'  # links
        html += '</div>\n'  # card
    return html


def get_icon(filepath):

    """returns a thumbnail image path for a given file path"""

    iconname = get_hashname(filepath)
    iconurl = os.path.join(imagefolder, iconname)
    iconpath = os.path.join(homefolder, iconurl)
    try:
        zfile = zipfile.ZipFile(filepath)
    except Exception:
        return defaulticon
    if "thumbnails/Thumbnail.png" in zfile.namelist():
        data = zfile.read("thumbnails/Thumbnail.png")
        thumb = open(iconpath, "wb")
        thumb.write(data)
        thumb.close()
    else:
        return defaulticon
    if not os.path.exists(iconpath):
        return defaulticon
    return iconurl


def get_hashname(filepath):

    """creates a png filename for a given file path"""

    filepath = clean_path(filepath)
    return hashlib.md5(filepath.encode()).hexdigest()+".png"


def clean_path(filepath):

    """cleans a file path into subfolder/subfolder/file form"""

    if filepath.startswith(homefolder):
        # strip local part od the path
        filepath = filepath[len(homefolder):]
    filepath = filepath.replace("\\", "/")
    if filepath.startswith("/"):
        filepath = filepath[1:]
    filepath = urllib.parse.quote(filepath)
    return filepath


if __name__ == "__main__":
    html = build_html(homefolder)
    html = template.replace("<!--contents-->", html)
    html = html.replace("<!--listicon-->", listicon)
    html = html.replace("<!--gridicon-->", gridicon)
    html = html.replace("<!--collapseicon-->", collapseicon)
    html = html.replace("<!--expandicon-->", expandicon)
    with open(htmlfile, "w") as index:
        index.write(html)
    print("Saving", htmlfile, "... All done!")
