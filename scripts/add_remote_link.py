from lxml import etree,objectify
import argparse
from base_xml import namespaces, get_base_report , re_namespaces_report , write
from base_zip import compress,extract
#=DRILLDOWN("remote-sugar"; "http://test:8080/pentaho"; {"sk_pejabat_jkr_param"; [sk_pejabat_jkr] | "pejabat_filter"; [pejabat_filter] | "projek_filter"; [projek_filter] | "rmk_filter"; [rmk_filter] | "ibs_filter"; [ibs_filter] | "kategori_perbelanjaan_filter"; [kategori_perbelanjaan_filter] | "kaedah_perolehan_filter"; [kaedah_perolehan_filter] | "lokasi_tapak_filter"; [lokasi_tapak_filter] | "index_param"; ([index_param]+1) | "kaedah_perlaksanaan_filter"; NA() | "::pentaho-path"; "/public/J10_Reports/Planning_Reports/Projek_Mengikut_Kategori_ACAT/first_level.prpt" | "Year From"; NA() | "kategori_perbelanjaan"; [kategori_perbelanjaan] | "sk_pejabat_atas_jkr_param"; [sk_pejabat_jkr] | "rmk"; [rmk] | "Year To"; NA() | "jenis_perolehan"; [jenis_perolehan] | "sk_pejabat_atas"; [sk_pejabat_jkr] | "projek"; [projek] | "ibs"; [ibs] | "sk_pejabat"; [sk_pejabat_jkr] | "pejabat"; [pejabat]})

parser = argparse.ArgumentParser()
parser.add_argument('--path', help='Path for the report',required=True)
parser.add_argument('--remote', help='string',required=True)

args = parser.parse_args()

def change_to_local(href,domain):
    formula = href.attrib['formula']
    formula = formula.replace("remote-sugar","local-sugar")
    formula = formula.replace(domain,"NA()")
    #formula = formula.replace('\"'+domain+'\"',"NA()")

    return formula
    

def change_to_remote(href,domain):
    formula = href.attrib['formula']
    formula = formula.replace("local-sugar","remote-sugar")
    formula = formula.replace("NA()",domain,1)
    #formula = formula.replace('\"'+domain+'\"',"NA()")

    return formula
    

def find_all_href_target(base):
    return base.findall(".//prefix:style-expression[@style-key='href-target']",namespaces)

if __name__ == "__main__":
    if args.path[-1] != '/':
        args.path = args.path+"/"

    extract(args.path+"first_level.prpt",args.path+"first_level")

    full_path = args.path+'first_level/layout.xml'
    root , base = get_base_report(full_path) 
    hrefs = find_all_href_target(base)
    for href in hrefs:
        if args.remote is not None:
            href.attrib['formula'] = change_to_remote(href,args.remote)
        else:
            change_to_local(href,args.remote)

    write(root,full_path)
    compress(args.path+"first_level/",args.path+"first_level.prpt")

