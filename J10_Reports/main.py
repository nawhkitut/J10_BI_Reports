from lxml import etree,objectify
from zipfile import ZipFile
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--path', help='the path',required=True)
parser.add_argument('--level', help='the level',required=True)
parser.add_argument('--func', help='the function',required=True)
args = parser.parse_args()
namespaces = {}

def extract(path,level):
  print("---extracting---",path)
  with ZipFile(path,mode='r') as zipObj:
    zipObj.extractall(path=args.path+level)

def write(root,path):
  etree.ElementTree(root).write(path+'layout.xml',pretty_print=True)

def re_namespaces(root):
  for k,v in root.nsmap.items():
    if not k:
      namespaces['prefix'] = v

def remove_link_from_excel(href):
  link = href.attrib['formula']
  if link.find('ISEXPORTTYPE') > -1:
    print("ada")
    return link
  else:
    return '=IF(ISEXPORTTYPE("table/html");'+link[1:]+';NA())'

def parse_xml(xmlFile):
  tree = etree.parse(xmlFile+"layout.xml")
  root = tree.getroot()
  re_namespaces(root)
  details = root.find(".//prefix:details",namespaces)
  hrefs = (details.findall(".//prefix:style-expression",namespaces))

  for href in hrefs:
    href.attrib['formula'] = remove_link_from_excel(href)
  write(root,xmlFile)

def main():
  if args.func == "excel":
    level = "first_level"
    if args.level == 2:
      level = "second_level"
    extract(args.path+level+".prpt",level)
    parse_xml(args.path+level+"/")

if __name__ == "__main__":
  main()
