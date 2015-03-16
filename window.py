import commands

def prev(x, a, key=(lambda x: x)):
    """Given x and a list a = [a[0], a[1], ...] already sorted by the function
    key, return the index i such that key(a[i]) is the largest number 
    that is less than or equal to key(x).

    Note: the function returns -1 if key(x) is less than all key(a[i]).
    This function is modified based on bisect.bisect() from python library.      
    """

    lo = 0; hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if key(x) < key(a[mid]): 
            hi = mid
        elif key(x) == key(a[mid]):
            return mid
        else: lo = mid+1
    return lo-1


def get_landed_windows(tile, windows_list):
    """Given a tile represented as (begin, end), and a list of windows,
    each of the form (begin, end, info_string), return the list of 
    windows on which the tile lands, i.e., the list of windows that 
    intersect the given tile.
    
    Args:
        tile (tuple): (begin, end) of a tile
        windows_list (list): [(begin0, end0, info_string0), 
            (begin1, end1, info_string1), ...]. We assume that begin < end, 
            and end0 <= begin1 and so on
    Return:
        list: the sublist of windows_list whose elements intersect tilespan"""
        
    # init_index is the first candidate window on which the tile lands
    init_index = prev(tile, windows_list, key=(lambda x: x[0]))
    landed_windows = []
    
    # Check if indeed tile lands on windows_list[init_index]
    if init_index != -1 and tile[0] < windows_list[init_index][1]:
        landed_windows.append(windows_list[init_index])
        
    index = init_index + 1
    
    # Append the subsequent windows if they intersect the tile
    for window in windows_list[index:]:
        if tile[1] > window[0]:
            landed_windows.append(window)
        else: 
            break
    
    return landed_windows
    
    
def get_cnv_list(assembly_id, chromosome, cnv_dir='cnvSegmentsDiploidBeta/'):
    """Given the assembly_id and the chromosome, return the list of cnv windows.
    
    Args:
        assembly_id (string): e.g. GS000009920-ASM
        chromosome (string): chr1, ... chr22, chrX, chrY, chrM
        cnv_dir (string): the directory of the cnv files
    Return:
        list: the list of cnv windows, each of the form (begin, end, cnv_type),
            sorted by the zeroth entry"""
            
    filename = (cnv_dir + 'cnvSegmentsDiploidBeta-' + assembly_id + '.tsv')
    cnv_list = []
    with open(filename, 'r') as f:
        for line in f:
            # Example format:
            # chr1	10000	177417	106.4	1.24	N	hypervariable	0	0
    
            full_cnv = line.split('\t')
            # Entry 0 is chromosome
            if full_cnv[0] == chromosome:
                # Entry 1 is begin, entry 2 end, and entry 6 calledCNVType
                cnv_list.append((int(full_cnv[1]), int(full_cnv[2]), full_cnv[6]))
            elif len(cnv_list) > 0:
                break
                
    return cnv_list
    
    
def get_assembly_ids_list(cnv_dir='cnvSegmentsDiploidBeta/'):
    """Get assembly IDs from assembly_ids.txt
    
    Args:
        cnv_dir (string): the directory of the cnv files"""
    
    asm_ids_list = []
    output_string = commands.getoutput('ls ' + cnv_dir)
    output_list = output_string.split('\n')
    
    for line in output_list:
        # Example line:
        # cnvSegmentsDiploidBeta-GS000034217-ASM.tsv
        asm_id = line.split('-')[1] + '-ASM'
        asm_ids_list.append(asm_id)        
    
    return asm_ids_list
