from lxml import etree,objectify
from base_xml import namespaces, get_base_report , re_namespaces_report , write
import sys
import argparse
from base_zip import compress,extract

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='Path for the report',required=True)

args = parser.parse_args()

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

def insert_new_node(new,sibling):
  if new is not None:
    sibling.addnext(new)

def remove_width_header(band):
  for b in band:
    min_width = b.findall(".//style-expression[@style-key='min-width']",namespaces)
    new = None
    if "band" in b.tag:
      if len(min_width) <= 0:
        new = remove_width_header(b)
        insert_new_node(new,b)
    elif "label" in b.tag:
      if len(min_width) <= 0:
        es = b.find('style:element-style',namespaces)
        new = style_element_style(es)
        insert_new_node(new,es)
    elif "style" in b.tag:
      if len(min_width) <= 0:
        new = style_element_style(b)
        insert_new_node(new,b)
  return band

def remove_width_fields(field):
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

def link_only_for_html(href):
  formula = href.attrib['formula']
  if href.attrib.get('style-key') is not None and href.attrib.get('style-key') == 'href-target':
    if formula.find('ISEXPORTTYPE') > -1:
      return formula
    else:
      return '=IF(ISEXPORTTYPE("table/html");'+formula[1:]+';NA())'
  else:
    return formula

def get_hrefs(base):
  return base.findall(".//prefix:style-expression[@style-key='href-target']",namespaces)
def get_fields(base):
  return base.findall(".//prefix:*[@core:field]",namespaces)
def get_header(base):
  return base.find(".//prefix:group-header",namespaces).find('.//prefix:root-level-content',namespaces)

if __name__ == "__main__":
  if args.path[-1] != '/':
      args.path = args.path+"/"
  full_path = args.path+'5.3.7_PLN_lvl1/layout.xml'
  extract(args.path+"5.3.7_PLN_lvl1.prpt",args.path+"5.3.7_PLN_lvl1")
  root , base = get_base_report(full_path)
  hrefs = get_hrefs(base)
  attrb = get_fields(base)
  header = get_header(base)
  for href in hrefs:
    href.attrib['formula'] = link_only_for_html(href)
  for attr in attrb:
    attr = remove_width_fields(attr)
  for h in header:
    header = remove_width_header(h)
    write(root,full_path)
  write(root,full_path)
  compress(args.path+"5.3.7_PLN_lvl1/",args.path+"5.3.7_PLN_lvl1.prpt")
  
