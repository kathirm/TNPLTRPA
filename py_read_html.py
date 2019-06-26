import codecs
import sys, os

dirpath = os.getcwd()
print dirpath
var = sys.argv[1]
f=open("test.html").read().format(var=var)
print f
