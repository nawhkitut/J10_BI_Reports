from lxml import etree,objectify
from zipfile import ZipFile
import os
import argparse
from os.path import basename
import sys

#
#
filters = [
  'kaedah_perolehan_filter'
]

headers_param = {
  "acat_param":[
    "acat1","acat2","acat3","acat4","acat5"
  ],
  "bontot_param":[
    "param_1","param_2"
  ]
} #

#
#
namespaces = {}
folder = [
  "datasources","META-INF","resources"
]

def append_valid_link(value):
  return "DRILLDOWN(&quot;local-sugar&quot;; NA();"+value+")"

def generate_param(k,v,last):
  return "&quot;"+k+"&quot;; ["+v+"] " if last else "&quot;"+k+"&quot;; ["+v+"] | "

def generate_filter_string(filters):
  #&quot;sk_pejabat_atas_jkr_param&quot;; [sk_pejabat_atas_jkr]
  filter_string = ""
  for f in filters:
    filter_string = filter_string + "&quot;"+f+"&quot;; ["+f+"] | "
  return filter_string
    
def gen(total,filters,headers_param):
  generated_list = [""]*total
  generated_filter_string = generate_filter_string(filters)

  for i in range(len(generated_list)):
    generated_list[i] = generated_filter_string

  headers_index = 0
  for h in headers_param:
    last_index = True if headers_index  == len(headers_param)-1 else False
    h_param_loop = 0
    for t in range(total):
      temp =  generate_param(h,headers_param[h][h_param_loop],last_index)
      generated_list[t] = generated_list[t] + temp
      if h_param_loop >= len(headers_param[h])-1:
        h_param_loop = 0
      else:
        h_param_loop = h_param_loop + 1
    headers_index = headers_index + 1

  for link in generated_list:
    print(append_valid_link(link))

  return generated_list
    
def create_style_expression_tag(formula):
  ns = etree.Element('style-expression')
  ns.attrib['style-key'] = "href-target"
  ns.attrib['formula'] = formula
  return ns

def re_namespaces(root):
  for k,v in root.nsmap.items():
    if k == 'style':
      namespaces['style'] = v
    if k == 'core':
      namespaces['core'] = v
    if not k:
      namespaces['prefix'] = v

def add_link(href,formula):
  ns = create_style_expression_tag(formula)
  href.insert(-1,ns)
  return href

def parse_xml(path):
  tree = etree.parse(path+"layout.xml")
  root = tree.getroot()
  re_namespaces(root)
  details = root.find(".//prefix:group",namespaces)
  fields = details.findall(".//prefix:*[@core:field]",namespaces)
  generated_urls = gen(len(fields),filters,headers_param)
  for field in range(len(fields)):
    fields[field] = add_link(fields[field],generated_urls[field])

def main():
  parse_xml("test")


if __name__ == "__main__":
  main()