from lxml import etree,objectify
from zipfile import ZipFile
import os
import argparse
from os.path import basename
import sys

namespaces = {}
folder = [
  "datasources","META-INF","resources"
]

def re_namespaces_report(root):
  for k,v in root.nsmap.items():
    if k == 'style':
      namespaces['style'] = v
    if k == 'core':
      namespaces['core'] = v
    if not k:
      namespaces['prefix'] = v

#no need
def re_namespaces_ds(root):
  for k,v in root.nmap.items():
    if k == 'data':
      namespaces['data'] = v

def write(root,path):
  etree.ElementTree(root).write(path,pretty_print=True)

def get_base_report(xmlFile:str):
  tree = etree.parse(xmlFile) 
  root = tree.getroot()
  re_namespaces_report(root)
  base = root.find(".//prefix:group",namespaces)
  return root , base

def get_base_ds(xmlFile:str):
  tree = etree.parse(xmlFile)
  root = tree.getroot()
  re_namespaces_ds(root)
  base = root.find(".//data:connection",namespaces)
  return root,base
