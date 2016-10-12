schoolbook2pdf
==============

Python script that takes educational eBooks from the German schoolbook publishers' "Digitale Schulbücher" platform and
converts them to PDF.

Note
----
This software is for demonstration purposes only and should not be used in any way that violates the publishers' Terms
and conditions. It is not affiliated with "Digitale Schulbücher" or any of the publishers.

Requirements
------------
- Windows OS for running the "Digitale Schulbücher" client. Tested on Windows 10.
- Linux OS (or a working setup for compiling `swftools` on Windows, not tested) for running this script. Tested on Ubuntu.

How to
------
**On your Windows OS**
- Install the "Digitale Schulbücher" client on your Windows machine and log in
- Download and open the book(s) you want to convert to PDF
- Navigate to one of the following folders (only one of them will exist on your system):
```
C:\Users\<user name>\AppData\Roaming\Digitale.Schulbucher\Local Store\users\<some user ID>\
C:\Program Files (x86)\Digitale Schulbücher\data\users\<some user ID>\
```
- Find the book you are looking for by going through the subfolders and looking at their respective `desc\thumb.png`
files
- Copy the subfolder to another folder that is accessible from your Linux OS

**On your Linux OS**
- Install dependencies
```
    sudo apt-get install build-essential g++ libfontconfig1-dev libfftw3-dev libzzip-dev libpoppler-dev libjpeg62-dev libgif-dev libpng12-dev git libfreetype6-dev libmotif-dev
```
- Download pdflib from [this site](http://www.pdflib.com/download/free-software/pdflib-lite-7/) and run
```
    ./configure
    make
    sudo make install
```
- Obtain and compile a modified version of the `swftools` package's `gfx2gfx` tool and add it to your `PATH`.
```
    git clone https://github.com/johan12345/swftools.git
    cd swftools
    ./configure
    make
    cd lib
    make
    cd ../src
    make gfx2gfx
    PATH=$PATH:$(pwd)
    cd ../..
```
- Download and run this script
```
    git clone https://github.com/johan12345/schoolbook2pdf.git
    python3 schoolbook2pdf/decrypter.py <book folder>
```

Known issues
------------
- Text is not selectable and searchable in the resulting PDF files. This is probably a limitation of `swftools`.
Workaround: Run OCR on the PDF, e.g. in Adobe Reader.
