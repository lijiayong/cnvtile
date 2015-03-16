import commands

def get_path_chromosome(pathid, coord_dir='tileid_hg19_split_by_path/'):
    """Return the chromosome where the given path lies.
    
    Args:
        pathid (string): e.g., '35e'' (see tileid_hg19_split_by_path/
            for the list of all pathids)
        coord_dir (string): the directory of the coordinates    
    Return:
        string: the chromosome where the given path lies, chr1, ... chr22, 
            chrX, chrY, chrM"""
    
    with open(coord_dir + pathid + '.csv') as f:
        first_line = f.readline()
        
    # Example line:
    # 000.00.000.000,hg19 chr1 0-24 10534
    # Entry 1 is chromosome.
    chromosome = first_line.split(' ')[1]
    return chromosome
    
    
def get_chromosomes_hash(coord_dir='tileid_hg19_split_by_path/'):
    """Return the hash table of the form {'chr1': ['000', '001', ...], 'chr2':...}.
    
    Args:
        coord_dir (string): the directory of the coordinates
    """
    
    output_string = commands.getoutput('ls ' + coord_dir)
    output_list = output_string.split('\n')
    
    chromosomes_table = {}
    for line in output_list:
        pathid = line.replace('.csv', '')
        chromosome = get_path_chromosome(pathid)
        if chromosome not in chromosomes_table:
            chromosomes_table[chromosome] = [pathid]
        else:
            chromosomes_table[chromosome].append(pathid)
                
    return chromosomes_table
    
    
def get_tilespans_list(pathid, coord_dir='tileid_hg19_split_by_path/'):
    """Return the hash table (dictionary) of the given path.
    
    Args:
        pathid (string): e.g., 35e (see ./tileid_hg19_split_by_path/
            for the list of all pathids)
        coord_dir (string): the directory of the coordinates
    Return:
        dictionary: the dictionary of the form {tileid: (begin, end), ...},
            where (begin, end) is the span of the tile in hg19 coordinates
    """
    
    tilespans_list = []
    with open(coord_dir + pathid + '.csv') as f:
        for line in f:
            # Each line is of the form '118.00.001.000,hg19 chr6 2301520 2303204'
            # or sometimes at the beginning 
            # '000.00.000.000,hg19 chr1 0-24 10534',
            # or at the end
            # '35e.00.022.000,hg19 chrM 16278 16571+24'.
            line_entries = line.split(' ')
            
            begin_str = line_entries[2]
            # Take out the '-' if present.
            begin = int(begin_str.split('-')[0])
                
            end_str = line_entries[3] 
            # Take out the '+' if present.
            end = int(end_str.split('+')[0])
                
            tilespans_list.append((begin, end))
    
    return tilespans_list
