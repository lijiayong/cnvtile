CNV Tile
========

CNV Tile is a command line tool for visualizing Copy Number Variation of human genomes.

### Download Data Command
```
optional arguments:
  -h, --help  show this help message and exit
  --cnv       download cnv data
  --coord     download hg19 coordinates data
```
  
#### Examples
	$ python download_data.py --cnv --coord


### CNV Tile Command
```
optional arguments:
  -h, --help       show this help message and exit
  --allpaths       generate pngs of all paths
  --path PATH      generate png of the given path
  --pngdir PNGDIR  specify the directory of the output png files (default: pngs_by_path/)
```
  
#### Examples
	$ python cnvtile.py --path=00a -pngdir=my_pngs
	$ python cnvtile.py --allpaths
