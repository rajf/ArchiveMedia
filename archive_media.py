#!/usr/bin/python
# Copy media files from a source into a given directory.
# Name them according to their date of creation.
# Put them in a directory based on the month.

import sys, os, glob, time, string

config = {
    "dir": {
        "src": "test",
        "dest": "output"
    },
    "extensions" : (".png",".jpg",".jpeg",".gif",".mov",".mpg",".mpeg",".wmv",".avi"),
    "move" : 0
}

def copyfiles(srcDir=config["dir"]["src"], destDir=config["dir"]["dest"], move=config["move"]):

    srcPath = os.path.join(os.path.dirname(__file__),srcDir)
    destPath = os.path.join(os.path.dirname(__file__),destDir)

    srcfiles = []

    for ROOT,DIR,FILES in os.walk(srcPath):
        for file in FILES:
            if file.endswith(config["extensions"]):
                # print os.path.join(ROOT,file)
                srcfiles.append(os.path.join(ROOT,file))

    for i in srcfiles:
        print i
        ext = os.path.splitext(i)[1]
        t = time.gmtime(os.path.getmtime(i))
        newname = time.strftime("%Y_%m_%d-%H_%M_%S",t) + ext
        monthdir = os.path.join(destPath, newname[:7])
        if not os.path.isdir(monthdir):
            print "Creating new dir", monthdir
            os.mkdir(monthdir)
        fullnewname = string.lower(os.path.join(monthdir,newname))

        # if file already exists, we add a suffix
        testname = fullnewname
        suffnum = 1
        while os.path.exists(testname):
                testname = "%s.%02d" % (fullnewname, suffnum)
                suffnum += 1
        if testname != fullnewname:
                fullnewname = testname

        print i,"->",fullnewname
        if config["move"]:
                os.rename(i, fullnewname)
        else:
                s = open(i,"rb")
                d = open(fullnewname, "wb")
                while 1:
                    b = s.read()
                    if not b: break
                    d.write(b)
                d.close()
                s.close()

if __name__ == "__main__":
    copyfiles()
