def color_of_landed_windows(cnv_windows_list, normal_color=[255,255,255], 
                                abnormal_color=[255,165,0], 
                                inconclusive_color=[190,190,190]):
    """Return the color corresponding to the union of all cnv types of
    a list of cnv windows ({cnv_window[2] for cnv_window in cnv_windows_list}).
    
    Args:
        cnv_windows_list (list): a list of the form [(begin, end, cnv_type), ...]
        normal_color (list): a png color code. 
        abnormal_color (list): a png color code.
        inconclusive_color (list): a png color code.
    Return:
        string: the color code of corresponding to the set of all cnv types. 
            The set of all cnv types is considered normal it is {'='}, 
            abnormal if it contains '+' or '-', and inconclusive otherwise. 
            Note that empty set is inconclusive."""
        
        
    cnv_type_set = {cnv_window[2] for cnv_window in cnv_windows_list}
    
    if cnv_type_set == {'='}:
        color_code = normal_color
    else:
        if '+' in cnv_type_set or '-' in cnv_type_set:
            color_code = abnormal_color
        else:
            color_code = inconclusive_color
            
    return color_code
    
    
def get_tile_png_codes(tile_colors_list, empty_tile_color=[190,190,190]):
    """Return the 14x14 pixels codes for generating png.
    
    Args:
        tile_colors_list (list): e.g., [[255,255,255], [255,165,0], ...], 
            where each element is the color code of an assembly id.
            The length of the list is less than or equal to 14x14=196
        empty_tile_color (list): an RGB coordinate that is not covered by
            the color_codes_list. The empty tiles are appended to the
            color_codes_list.
    Return:
        list: a (14x3)x(14) list, e.g., [[255,255,255, 255,165,0, ...], 
                                         [190,190,190, 255,165,0, ...],
                                         ...]"""
    
    empty_list = [empty_tile_color for x in range(196
                                            -len(tile_colors_list))]
    total_list = tile_colors_list + empty_list    
    tile_png_codes = []
    
    for y in range(14):
        row = []
        for x in range(14):
            row.extend(total_list[14 * y + x])
        tile_png_codes.append(row)
                                            
    return tile_png_codes
    

def juxtapose_png_codes(png_codes_list, frame_color=[190,190,190], 
                    empty_tile_color=[190,190,190], tiles_wrap_num=3600):
    """Return the juxtaposition of a list of png color codes.
    
    Args:
        png_codes_list (list): a list of tile png codes, each element of the
            list is a (14x3)x(14) list. See the output of get_tile_png_codes
        frame_color (list): png code of the frame
        tiles_wrap_num (int): the width of the each row in terms of the 
            number of tiles.
    Return:
        list: the juxtaposition of the list of png codes"""
    
    num_of_tiles = len(png_codes_list)
    num_of_tile_rows = num_of_tiles // tiles_wrap_num + 1
    
    
    # Append the png_codes_list with empty tiles to achieve a multiple of
    # tiles_wrap_num of tiles
    num_of_empty_tiles = tiles_wrap_num * num_of_tile_rows - num_of_tiles
    empty_tile = [[190,190,190] * 14 for y in range(14)]
    empty_tiles_list = [empty_tile for x in range(num_of_empty_tiles)]
    png_codes_list.extend(empty_tiles_list)
    
    horizontal_frame = frame_color * (tiles_wrap_num*14 + tiles_wrap_num + 1)
    # Initialize with horizontal_frame
    juxtaposed_png_code = [horizontal_frame]
    
    for tile_row in range(num_of_tile_rows):
        for y in range(14):
            begin = tile_row * tiles_wrap_num
            end = (tile_row+1) * tiles_wrap_num
            y_row = frame_color[:]
            for png_code in png_codes_list[begin: end]:
                y_row.extend(png_code[y]+frame_color)
            juxtaposed_png_code.append(y_row)
        # Add horizontal_frame after a tile row (14 pixel rows)
        juxtaposed_png_code.append(horizontal_frame)

    return juxtaposed_png_code
