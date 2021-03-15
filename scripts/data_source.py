from lxml import etree,objectify
from zipfile import ZipFile
import os
import argparse
from os.path import basename
from base_xml import namespaces, get_base_ds , re_namespaces_ds,write

class DataConnection:
    
    props = dict()

    def populate_data(self,dc):
        self.driver = dc.find('data:driver',namespaces)
        self.url = dc.find('data:url',namespaces)
        properties = dc.find('data:properties',namespaces)
        self.props['user'] = properties.find('data:property[@name="user"]')
        self.props['password'] = properties.find('data:property[@name="password"]')
        self.props['port'] = properties.find('data:property[@name="::pentaho-reporting::port"]')
        self.props['name'] = properties.find('data:property[@name="::pentaho-reporting::name"]')
        self.props['database_name'] = properties.find('data:property[@name="::pentaho-reporting::database-name"]')
        self.props['hostname'] = properties.find('data:property[@name="::pentaho-reporting::hostname"]')
        self.props['database_type'] = properties.find('data:property[@name="::pentaho-reporting::database-type"]')
    
    def save(self):
        write(self.root,self.path)

    def __init__(self,path):
        root,base = get_base_ds(path)
        self.path = path
        self.root = root 
        self.populate_data(base)


if __name__ == "__main__":
    pass    

