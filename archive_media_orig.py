#!/usr/bin/python
# Copy image files from a source into a photo directory.
# Name them according to their date of creation.
# Put them in a directory based on the month.

import sys, os, glob, time, string

def copyfiles(srcdir, destdir, pattern, move=0):
    srcfiles = glob.glob(os.path.join(srcdir, pattern))
    for i in srcfiles:
        ext = os.path.splitext(i)[1]
        t = time.gmtime(os.path.getmtime(i))
        newname = time.strftime("%Y_%m_%d-%H_%M_%S",t) + ext
        monthdir = os.path.join(destdir, newname[:7])
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
        if move:
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

def main():
    srcdir = "/Users/xxxx/Desktop/temp/pics/import"
    destdir = "/Users/xxxx/Desktop/temp/pics/output"
    if len(sys.argv) > 1:
        srcdir = sys.argv[1]
    if len(sys.argv) > 2:
        destdir = sys.argv[2]
    copyfiles(srcdir, destdir, "*.jpg*", move=1)
    copyfiles(srcdir, destdir, "*.JPG*", move=1)


if __name__ == "__main__":
    main()
