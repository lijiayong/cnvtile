CNV Tile
========

CNV Tile is a command line tool for visualizing Copy Number Variations of human genomes.
It highlights the portions of 174 sample genomes from Personal Genome Project which have
Copy Number Variations, according to the tile coordinates of the reference genome (hg19). 

### Download Data Command
	Download the Copy Number Variation data from Personal Genome Project via PGP 
	public bucket on Google Cloud Storage 
	(require gsutil, see https://cloud.google.com/storage/docs/gsutil_install).
	Download the hg19 coordinates (split by path) from Curoverse.

```
name:
	download_data.py

arguments:
	-h, --help  show this help message and exit
	--cnv       download cnv data
	--coord     download hg19 coordinates data
```
  
#### Examples
	$ python download_data.py --cnv --coord


### CNV Tile Command
	Generate png files that highlight the tiles of sample genomes from Personal
	Genome Project that have Copy Number Variation.

```
name:
	cnvtile.py
	
arguments:
	-h, --help       show this help message and exit
	--allpaths       generate pngs of all paths
	--path PATH      generate png of the given path
	--pngdir PNGDIR  specify the directory of the output png files (default: pngs_by_path/)
```
  
#### Examples
	$ python cnvtile.py --path=00a -pngdir=my_pngs
	$ python cnvtile.py --allpaths
