#!/usr/bin/python
# Copy media files from a source into a given directory.
# Name them according to their date of creation.
# Put them in a directory based on the month.

import sys, os, glob, time, string, shutil

config = {
    "mediaSets": [
        {
        "parse" : 1,
        "move" : 1,
        "srcDir" : "test 2",
        "destDir": "output/test2",
        "tags" : "test2"
        },
        {
        "parse" : 1,
        "move" : 0,
        "srcDir" : "test",
        "destDir": "output/test",
        "tags" : "test"
        },
        {
        "parse" : 0,
        "move" : 0,
        "srcDir" : "import/rob",
        "destDir": "output/rob",
        "tags" : "rajf"
        }
    ],
    "extensions" : (".png",".jpg",".jpeg",".gif",".mov",".mpg",".mpeg",".wmv",".avi",".mp4")
}

def parseFolder(srcPath):
    files = []
    for ROOT,DIR,FILES in os.walk(srcPath):
        for file in FILES:
            if file.lower().endswith(config["extensions"]):
                files.append(os.path.join(ROOT,file))
    return files

def parseFile(file, destPath, move, tags):
    fileName = os.path.splitext(os.path.basename(file))[0]
    ext = os.path.splitext(file)[1]
    t = time.gmtime(os.path.getmtime(file))
    year = time.strftime("%Y",t)
    month = time.strftime("%m",t)
    day = time.strftime("%d",t)
    newName = "{0}--{1}-{2}-{3}[{4}]{5}".format(fileName, year, month, day, tags,ext)
    destPath = os.path.join(destPath, year + "/" + year + "-" + month + "/" + newName)
    writeFile(file, destPath, move)

def writeFile(file, destPath, move=0):

    # check folder exists
    folder=os.path.dirname(destPath)
    if not os.path.exists(folder):
		os.makedirs(folder)

    # if file already exists, we add a suffix
    testname = destPath
    suffnum = 1
    while os.path.exists(testname):
            testname = "%s.%02d" % (destPath, suffnum)
            suffnum += 1
    if testname != destPath:
            destPath = testname

    print file,"->",destPath
    if move:
            os.rename(file, destPath)
    else:
            s = open(file,"rb")
            d = open(destPath, "wb")
            while 1:
                b = s.read()
                if not b: break
                d.write(b)
            d.close()
            s.close()

def init():
    for media in config["mediaSets"]:
        srcPath = os.path.join(os.path.dirname(__file__),media["srcDir"])
        destPath = os.path.join(os.path.dirname(__file__),media["destDir"])
        if (media["parse"]):
            files = parseFolder(srcPath)
            for f in files:
                parseFile(f, destPath, media["move"], media["tags"])
            # Delete import dir and recreate new empty dir
            # if(media["delSrc"]):
            #     shutil.rmtree(srcPath)
            #     os.mkdir(srcPath)

init()
