import subprocess

#imagemagick converter
#windows: magick mogrify
#linux: convert
def imagemagick(filename, targetformat):
    try:
        subprocess.run(["magick","mogrify","-format",targetformat,filename])
    except:
        splitname = filename.split(".")

        noext = ""

        for i in range(len(splitname)-1):
            noext += splitname[i]

        subprocess.run(["convert",filename,noext+"."+targetformat])