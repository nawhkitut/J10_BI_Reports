from lxml import etree,objectify
from zipfile import ZipFile
import os
import argparse
from os.path import basename
import sys

folder = [
  "datasources","META-INF","resources"
]

namespaces = {}

def get_files_in_path(dir):
  file_paths = []
  for root, directories, files in os.walk(dir): 
    for filename in files: 
      filepath = os.path.join(root, filename) 
      file_paths.append(filepath) 
  return file_paths 

def compress(path,fileName):
  file_paths = get_files_in_path(path)
  with ZipFile(fileName,'w') as zip:
    for file in file_paths:
      temp = file.split(os.sep)[-2]
      if temp in folder:
        zip.write(file,temp+"/"+basename(file))
      else:
        zip.write(file,basename(file))

def extract(path,extractPath):
  with ZipFile(path,mode='r') as zipObj:
    zipObj.extractall(path=extractPath)


def cleanup(path):
  pass