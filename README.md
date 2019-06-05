# NetCDF Scrubber

Brian Rose, brose@albany.edu

A utility to scan a directory structure for netcdf data files,
extract metadata from those files,
and write out the metadata into a .csv file for use in cataloging.

Usage:

```
python netcdf_scrubber.py input_path output_csv_file
```

`input_path` is the top level of the directory structure to be searched

`output_csv_file` is the desired path and file name for the .csv format output file

This script extracts two types of metadata from the files:
    - global attributes
    - attributes of the data variable
    
It is designed to work with CMIP5 output, for which each data variable is packaged in a unique file.

The data variable is identified from the filename. This won't work correctly if the filenames
don't follow standard CMIP5 conventions.

Dependencies:
    - python 3
    - pandas
    - xarray
    
Internally this builds a pandas.DataFrame object to hold all the metadata.
Creating output in formats other than .csv would be trivial since pandas can readily convert to other formats.

