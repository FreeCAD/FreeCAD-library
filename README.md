FreeCAD-library
===============

This repository contains a library of Parts to be used in FreeCAD. It is maintained by the community
of users of FreeCAD and is not part of the FreeCAD project, although it is made with the aim to be
used as a repository of parts by FreeCAD in the future.

Contributing to the library
---------------------------

If you made some interesting objects with FreeCAD, why not share them here? Others might find them
useful. The procedure is simple:

1. Create a github account for yourself
2. Fork this repository using the "Fork" button on the top right corner of this page
3. Follow the [github instructions](https://help.github.com/articles/fork-a-repo/) to clone your fork on your computer
4. Make all the changes you need, create more folders if necessary, and place your files in them
5. Upload (push) your changes to your fork on github (refer to the github help for instructions)
6. When your fork has been updated, you can submit a [pull request](https://help.github.com/articles/creating-a-pull-request/) to have your changes merged into the official library. A member of the community will review your proposed additions and accept the merge.

Each Part should be correctly named, and placed into subdirectories by family or type. They should also
be available in both .FcStd and .stp formats, and optionally in .stl format (because github lets you
visualize them). They should also be as simple as possible, and parametric
so users can easily change their dimensions. In the file properties of each .FcStd file, the author
should also be mentioned, and the license information if available.

**Note**: Please DO NOT use accented characters in your file names, thanks!!!

If you are interested in contributing to this library on a more long-term basis, please ask for write 
access to this repository on this FreeCAD forum thread: http://forum.freecadweb.org/viewtopic.php?f=19&t=4205

License
-------

All Parts in this repository are licensed under CC-BY 3.0 http://creativecommons.org/licenses/by/3.0/
Each Part is copyrighted by and should be attributed to its respective author(s).
See commit details to find the authors of each Part.

If you are uploading parts to this repository, please make sure you are the author of the model,
or otherwise that you have right to share it here under the CC-BY 3.0 license, and make sure the author
is mentioned in the commit message.

Install
-------

As the library is part of the [FreeCAD addons](https://github.com/FreeCAD/FreeCAD-addons), the easiest way
to install and keep the library updated is through the addons installer, where you will find it there
under the name 'parts_library'.

**Warning: the library is huge in size (+/- 1 Gb) and therefore might take a very long time to download**

There are currently two workarounds to this problem: 

1. You can download and install this library manually by following these steps:

* In FreeCAD, find which is your user **modules folder** by entering or pasting `App.getUserAppDataDir()+"Mod"` and your usr **macros folder** by entering `App.getUserMacroDir()` in the Python console (found under menu View->Panels)
* Download the library as a zip file using the green "clone or download" button in the top right corner of this page
* Unzip the zip file you just downloaded. You will get a "FreeCAD-library" folder
* Rename that folder from "FreeCAD-library" to "parts_library"
* Move that renamed folder to the **modules folder** location that we got above
* Inside the FreeCAD-library folder, you will find a PartsLibrary.FCMacro file. Copy that file to the **macros folder** that we got above
* Restart FreeCAD. The parts library will be installed, and the addons manager will recognize it as installed. You can launch and use the library by executing the PartsLibrary macro  from menu Macro -> Macros...

2. The [BIM addon](https://github.com/yorikvanhavre/BIM_Workbench) has a **Library** tool that features an experimental "online" option. With that option enabled, the BIM Library tool is able to access and use this library online, without the need to install it.

The library is a simple container for FreeCAD (.fcstd) and STEP (.stp) files. You can download it
anywhere and import its files in your FreeCAD projects. Inside the library, there is a FreeCAD
macro (PartsLibrary.FCMacro) that you can place in your FreeCAD macros folder. That macro creates 
a browser window inside FreeCAD, from which you can easily add the parts by double-clicking them.

![](http://www.freecadweb.org/wiki/images/c/c5/Parts-library.jpg)

Sharing your models from the macro
----------------------------------

The macro also allows a couple of other possibilities, such as adding new objects, and
sharing your objects with others. To share, you will need the python-git package
installed on your computer, and an online git repository you have permission to write to. The 
easiest way to obtain that is using the "fork" button on top of this github page.

Once you have made your fork, you will get an URL from it, that you can use in the macro's
config dialog. After that, once you have saved your models to the library, you can push them to
your online git repository, and, if you wish, make a pull request on this page to see your
models integrated to the official library.
