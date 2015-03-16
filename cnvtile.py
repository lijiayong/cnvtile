import png
import tile
import window
import png_gen
import os


def gen_png(tilespans_list, cnv_table, output_name):
    """Generate a png based on the list of tilespans and the cnv hash table.
    
    Args:
        tilespans_list (list): e.g. [(0, 10534), (10510, 10823), ...]
        cnv_table (dictionary): a table of cnv windows of a given chromosome, 
            with assembly ids as keys, 
            e.g. {'GS000009920-ASM': [(10000,177417,'hypervariable'), (), ...], ... }
            """
    
    asm_ids_list = sorted(cnv_table.keys())        
    path_png_codes_list = []
    
    for tilespan in tilespans_list:
        tile_colors_list = []
        for asm_id in asm_ids_list:
            landed_cnv_windows = window.get_landed_windows(tilespan, 
                                            cnv_table[asm_id])
            tile_color = png_gen.color_of_landed_windows(landed_cnv_windows)
            tile_colors_list.append(tile_color)    
        # Convert the color codes list to a form to be used by the png module.
        tile_png_codes = png_gen.get_tile_png_codes(tile_colors_list)
        path_png_codes_list.append(tile_png_codes)
        
    juxtaposed_png_code = png_gen.juxtapose_png_codes(path_png_codes_list)
    x_num = len(juxtaposed_png_code[0])/3; y_num = len(juxtaposed_png_code)
    
    with open(output_name, 'wb') as f:
        w = png.Writer(x_num, y_num)
        w.write(f, juxtaposed_png_code)
        
        
def gen_path_png(pathid, output_dir='pngs_by_path/'):
    """Given pathid, generate the png named pathid.png.
    
    Args:
        output_dir (string): the directory of the output"""
    
    tilespans_list = tile.get_tilespans_list(pathid)    
    chromosome = tile.get_path_chromosome(pathid)    
    asm_ids_list = window.get_assembly_ids_list()    
    # Prepare the table of cnv windows of the fixed chromosome, with assembly 
    # ids as keys, e.g.,
    # {'GS000009920-ASM': [(10000,177417,'hypervariable'), (), ...], ... }
    cnv_table = {}
    for asm_id in asm_ids_list:
        cnv_table[asm_id] = window.get_cnv_list(asm_id, chromosome)
        
    gen_png(tilespans_list, cnv_table, output_dir + pathid + '.png')
    
    
def gen_all_pngs(output_dir='pngs_by_path/'):
    """General all pngs, each one named pathid.png.
    
    Args:
        output_dir (string): the directory of the output"""
    
    chromosomes_hash = tile.get_chromosomes_hash()
    asm_ids_list = window.get_assembly_ids_list()
    
    for chromosome in chromosomes_hash:
        pathids_list = chromosomes_hash[chromosome]
        for pathid in pathids_list:
            tilespans_list = tile.get_tilespans_list(pathid)            
            # Prepare the table of cnv windows, with assembly ids as keys, e.g.,
            # {'GS000009920-ASM': [(10000,177417,'hypervariable'), (), ...], ... }
            cnv_table = {}
            for asm_id in asm_ids_list:
                cnv_table[asm_id] = window.get_cnv_list(asm_id, chromosome)
                
            gen_png(tilespans_list, cnv_table, output_dir + pathid + '.png')
            

import argparse
# passing arguments
parser = argparse.ArgumentParser()
parser.add_argument("--allpaths", action="store_true", help="generate pngs of all paths")
parser.add_argument("--path", help="generate png of the given path")
parser.add_argument("--pngdir", default='pngs_by_path/', 
        help="specify the directory of the output png files (default: pngs_by_path/)")
        
args = parser.parse_args()
output_dir = args.pngdir
cmd = 'mkdir ' + output_dir
if args.allpaths:
    os.system(cmd)
    gen_all_pngs(output_dir)
if args.path:
    os.system(cmd)
    gen_path_png(args.path, output_dir)
