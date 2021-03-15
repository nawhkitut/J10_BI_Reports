from lxml import etree,objectify
from zipfile import ZipFile
import os
import argparse
from os.path import basename
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='Path for the report',required=True)

args = parser.parse_args()
namespaces = {}
folder = [
  "datasources","META-INF","resources"
]

def get_files_in_path(dir):
  file_paths = []
  for root, directories, files in os.walk(dir): 
    for filename in files: 
      filepath = os.path.join(root, filename) 
      file_paths.append(filepath) 
  return file_paths 

def cleanup(path):
  pass

def compress(path):
  file_paths = get_files_in_path(path)
  with ZipFile(args.path+'first_level.prpt','w') as zip:
    for file in file_paths:
      temp = file.split(os.sep)[-2]
      if temp in folder:
        zip.write(file,temp+"/"+basename(file))
      else:
        zip.write(file,basename(file))

def extract(path,level):
  with ZipFile(path,mode='r') as zipObj:
    zipObj.extractall(path=args.path+level)

def write(root,path):
  etree.ElementTree(root).write(path+'layout.xml',pretty_print=True)

def re_namespaces(root):
  for k,v in root.nsmap.items():
    if k == 'style':
      namespaces['style'] = v
    if k == 'core':
      namespaces['core'] = v
    if not k:
      namespaces['prefix'] = v

def create_style_expression_tag(min_width):
  ns = etree.Element('style-expression')
  ns.attrib['style-key'] = "min-width"
  ns.attrib['formula'] = '=IF(ISEXPORTTYPE("table/html");'+str(min_width)+';NA())'
  return ns

def style_element_style(style):
  min_width = 0
  ss = style.find('style:spatial-styles',namespaces)
  if ss is not None:
    min_width = ss.attrib['min-width'] if 'min-width' in ss.attrib else 0
  return create_style_expression_tag(min_width)

def remove_width_label(band):
  pass

def insert_new_node(new,sibling):

  if new is not None:
    sibling.addnext(new)

def remove_width_band(band):
  for b in band:
    new = None
    if "band" in b.tag:
      if len(b.findall(".//style-expression[@style-key='min-width']",namespaces)) <= 0:
        new = remove_width_band(b)
        insert_new_node(new,b)

    elif "label" in b.tag:
      if len(b.findall(".//style-expression[@style-key='min-width']",namespaces)) <= 0:
        es = b.find('style:element-style',namespaces)
        new = style_element_style(es)
        insert_new_node(new,es)

    elif "style" in b.tag:
      if len(b.findall(".//style-expression[@style-key='min-width']",namespaces)) <= 0:
        new = style_element_style(b)
        insert_new_node(new,b)
      
  return band


def remove_width_from_excel_field(field):
  min_width = 0
  for f in field.find('style:element-style',namespaces).findall('style:spatial-styles',namespaces):
    if f is not None:
      min_width = (f.attrib['min-width'])
  if len(field.findall(".//style-expression[@style-key='min-width']",namespaces)) <= 0:
    ns = etree.Element('style-expression')
    ns.attrib['style-key'] = "min-width"
    ns.attrib['formula'] = '=IF(ISEXPORTTYPE("table/html");'+str(min_width)+';NA())'
    field.insert(-1,ns)
  return field
  

def remove_link_from_excel(href):
  link = href.attrib['formula']
  if href.attrib.get('style-key') is not None and href.attrib.get('style-key') == 'href-target':
    if link.find('ISEXPORTTYPE') > -1:
      return link
    else:
      return '=IF(ISEXPORTTYPE("table/html");'+link[1:]+';NA())'
  else:
    return link

def parse_xml(xmlFile):
  tree = etree.parse(xmlFile+"layout.xml")
  root = tree.getroot()
  re_namespaces(root)
  details = root.find(".//prefix:group",namespaces)
  hrefs = details.findall(".//prefix:style-expression[@style-key='href-target']",namespaces)
  attrb = details.findall(".//prefix:*[@core:field]",namespaces)
  header = details.find(".//prefix:group-header",namespaces).find('.//prefix:root-level-content',namespaces)
  for href in hrefs:
    href.attrib['formula'] = remove_link_from_excel(href)
  for attr in attrb:
    attr = remove_width_from_excel_field(attr)
  for h in header:
    header = remove_width_band(h)
  write(root,xmlFile)
  

def main():
  if args.path[-1] != '/':
    args.path = args.path+"/"
  level = "first_level"
  extract(args.path+level+".prpt",level)
  parse_xml(args.path+level+"/")
  compress(args.path+level+"/")

if __name__ == "__main__":
  main()
