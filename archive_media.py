#!/usr/bin/python
# Copy media files from a source into a given directory.
# Name them according to their date of creation.
# Put them in a directory based on the month.

import sys, os, glob, time, string

config = {
    "mediaSets": [
        {
        "parse" : 1,
        "delSrc" : 0,
        "srcDir" : "test",
        "destDir": "output/test",
        "tags" : "test"
        },
        {
        "parse" : 0,
        "delSrc" : 0,
        "srcDir" : "import/rob",
        "destDir": "output/rob",
        "tags" : "rajf"
        }
    ],
    "extensions" : (".png",".jpg",".jpeg",".gif",".mov",".mpg",".mpeg",".wmv",".avi"),
    "move" : 0
}

def parseFolder(srcPath):
    files = []
    for ROOT,DIR,FILES in os.walk(srcPath):
        for file in FILES:
            if file.endswith(config["extensions"]):
                files.append(os.path.join(ROOT,file))
    return files

def parseFile(file, destPath, tags):
    fileName = os.path.splitext(os.path.basename(file))[0]
    ext = os.path.splitext(file)[1]
    t = time.gmtime(os.path.getmtime(file))
    year = time.strftime("%Y",t)
    month = time.strftime("%m",t)
    day = time.strftime("%d",t)
    newName = "{0}-{1}-{2}-{3}[{4}]{5}".format(fileName, year, month, day, tags,ext)
    destPath = os.path.join(destPath, year + "/" + month + "/" + newName)
    writeFile(file, destPath)

def writeFile(file, destPath):

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
    if config["move"]:
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
                parseFile(f, destPath, media["tags"])

    # srcPath = os.path.join(os.path.dirname(__file__),srcDir)
    # destPath = os.path.join(os.path.dirname(__file__),destDir)
    #
    # srcfiles = []
    #
    # for ROOT,DIR,FILES in os.walk(srcPath):
    #     for file in FILES:
    #         if file.endswith(config["extensions"]):
    #             # print os.path.join(ROOT,file)
    #             srcfiles.append(os.path.join(ROOT,file))
    #             print DIR
    #
    # for i in srcfiles:
    #     # print i
    #     fileName = os.path.splitext(os.path.basename(i))[0]
    #     ext = os.path.splitext(i)[1]
    #     t = time.gmtime(os.path.getmtime(i))
    #     newname = time.strftime("%Y_%m_%d-%H_%M_%S",t) + ext
    #     monthdir = os.path.join(destPath, newname[:7])
    #     yearDir = os.path.join(destPath, newname[:4])
    #
    #     print fileName
    #     print newname

        # if not os.path.isdir(monthdir):
        #     print "Creating new dir", yearDir
        #     os.mkdir(monthdir)
        # fullnewname = string.lower(os.path.join(monthdir,newname))
        #
        # # if file already exists, we add a suffix
        # testname = fullnewname
        # suffnum = 1
        # while os.path.exists(testname):
        #         testname = "%s.%02d" % (fullnewname, suffnum)
        #         suffnum += 1
        # if testname != fullnewname:
        #         fullnewname = testname
        #
        # print i,"->",fullnewname
        # if config["move"]:
        #         os.rename(i, fullnewname)
        # else:
        #         s = open(i,"rb")
        #         d = open(fullnewname, "wb")
        #         while 1:
        #             b = s.read()
        #             if not b: break
        #             d.write(b)
        #         d.close()
        #         s.close()

if __name__ == "__main__":
    init()
