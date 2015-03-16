import os

def download_cnv_data():
    """Download the Copy Number Variation data from Personal Genome Project
    via PGP public bucket on Google Clound Storage."""
    
    cnv_dir = 'cnvSegmentsDiploidBeta/'
    os.system('mkdir ' + cnv_dir)
    with open('cnvSegmentsDiploidBeta_list') as f:
        for line in f:
            cmd = 'gsutil cp ' + line.strip() + ' ' + cnv_dir
            os.system(cmd)
            
def download_coord_data():
    """Download the hg19 coordinates (split by path) from Curoverse."""
    
    link = ('https://workbench.qr1hi.arvadosapi.com/collections/'
    'b6331bea18718d2e39c193ba449c055c+131/tileid_hg19_split_by_path.tar.gz'
    '?disposition=attachment&size=104970070')
    os.system('wget ' + link)
    os.system('tar -xzf tileid_hg19_split_by_path.tar.gz') 
            
            
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--cnv", help="download cnv data", action="store_true")
parser.add_argument("--coord", help="download hg19 coordinates data", action="store_true")
args = parser.parse_args()
if args.cnv:
    download_cnv_data()
if args.coord:
    download_coord_data()
