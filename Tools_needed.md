External tools that can be used for image shrinking.
====================================================

JPEG:
* jpegtran (http://jpegclub.org/jpegtran/; included in libjpeg-progs package
  on Ubuntu)
* Jpegoptim (http://www.kokkonen.net/tjko/projects.html)
* cjpeg-dssim (https://github.com/technopagan/cjpeg-dssim): find best quality
	setting for images using jpegoptim
* imgmin (https://github.com/rflynn/imgmin): another optimizer of jpeg quality
	setting
* mozjpeg (https://github.com/mozilla/mozjpeg)

GIF (used only for optimizing animated GIFs):
* Gifsicle (http://www.lcdf.org/gifsicle/)

PNG:
* OptiPNG (http://optipng.sourceforge.net/)
* AdvanceCOMP PNG (http://advancemame.sourceforge.net/doc-advpng.html)
* Pngcrush (http://pmt.sourceforge.net/pngcrush/)
* zopfli-png (https://github.com/subzey/zopfli-png)
* lossy: pngnq-s9 (http://sourceforge.net/projects/pngnqs9/)
* lossy: pngquant (https://pngquant.org/)

SVG:
* SVGCleaner (https://github.com/RazrFalcon/SVGCleaner)
* SVGO (https://github.com/svg/svgo)


Installable packages
--------------------

Following lists are not complete.


Ubuntu packages are:
* libjpeg-progs
* jpegoptim
* gifsicle
* optipng
* advancecomp
* pngcrush

CentOS packages are:
* jpegtran: libjpeg
* jpegoptim: can't find rpm on internet
* gifsicle: gifsicle package on repoforge
* optipng: optipng package in EPEL
* advancecomp: advancecomp package on repoforge
* pngcrush: pngcrush package on repoforge

Brew for MacOSX:
* jpeg
* jpegoptim
* mozjpeg
* gifsicle
* optipng
* advancecomp
* pngcrush
* pngquant

Alternative on MacOSX:
Install imageoptim (http://imageoptim.com) and then symlink from /usr/bin/
to all the required packages:
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/advpng
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/gifsicle
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/jpegoptim
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/jpegtran
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/optipng
sudo ln -s /Applications/ImageOptim.app/Contents/MacOS/pngcrush

