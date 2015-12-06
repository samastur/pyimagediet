.. _exttools:

External tools needed for shrinking.
====================================

Tools
-----

JPEG:

* `jpegtran <http://jpegclub.org/jpegtran/>`_
* `Jpegoptim <http://www.kokkonen.net/tjko/projects.html>`_
* `zcjpeg-dssim <https://github.com/technopagan/cjpeg-dssim>`_ finds best quality setting for images using jpegoptim
* `imgmin <https://github.com/rflynn/imgmin>`_ is another optimizer of jpeg quality setting
* `mozjpeg <https://github.com/mozilla/mozjpeg>`_
* `JPEGmini <http://www.jpegmini.com>`_, an expensive commercial compressor


GIF:

* `Gifsicle <http://www.lcdf.org/gifsicle/>`_:
  used only for optimizing animated GIFs


PNG:

* `OptiPNG <http://optipng.sourceforge.net/>`_
* `AdvanceCOMP PNG <http://advancemame.sourceforge.net/doc-advpng.html>`_
* `Pngcrush <http://pmt.sourceforge.net/pngcrush/>`_
* `zopfli-png <https://github.com/subzey/zopfli-png>`_
* lossy: `pngnq-s9 <http://sourceforge.net/projects/pngnqs9/>`_
* lossy: `pngquant <https://pngquant.org/>`_


SVG:

* `SVGCleaner <https://github.com/RazrFalcon/SVGCleaner>`_
* `SVGO <https://github.com/svg/svgo>`_


Installable packages
--------------------

Most of above tools can be found already packaged in distributions
repositories. Here is a probably incomplete list known to the author
(contributions for other distributions or missing packages are very
welcome).


Linux
~~~~~

Packages for **Ubuntu**:

* libjpeg-progs (includes jpegtran)
* jpegoptim
* gifsicle
* optipng
* advancecomp
* pngcrush

Packages for **CentOS**:

* jpegtran: libjpeg
* jpegoptim: can't find rpm on internet
* gifsicle: gifsicle package on repoforge
* optipng: optipng package in EPEL
* advancecomp: advancecomp package on repoforge
* pngcrush: pngcrush package on repoforge


OS X
~~~~

Brew for OS X:

* jpeg
* jpegoptim
* mozjpeg
* gifsicle
* optipng
* advancecomp
* pngcrush
* pngquant


Alternative installation on OS X (limited only to tools that come with ImageOptim):
Install `ImageOptim <http://imageoptim.com>`_ and then symlink from `/usr/bin/`
to all the required packages:::

    ln -s /Applications/ImageOptim.app/Contents/MacOS/advpng
    ln -s /Applications/ImageOptim.app/Contents/MacOS/gifsicle
    ln -s /Applications/ImageOptim.app/Contents/MacOS/jpegoptim
    ln -s /Applications/ImageOptim.app/Contents/MacOS/jpegtran
    ln -s /Applications/ImageOptim.app/Contents/MacOS/optipng
    ln -s /Applications/ImageOptim.app/Contents/MacOS/pngcrush
