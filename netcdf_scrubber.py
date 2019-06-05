"""
netcdf_scrubber.py

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
    - pandas
    - xarray
    
Internally this builds a pandas.DataFrame object to hold all the metadata.
Creating output in formats other than .csv would be trivial since pandas can readily convert to other formats.

Brian Rose
brose@albany.edu
"""
import os, sys
import xarray as xr
import pandas as pd

top_path = sys.argv[1]
output_path = sys.argv[2]

datalist = []

print('Searching for *.nc files within ', top_path)
for root, dirs, files in os.walk(top_path):
    for name in files:
        fullpath = os.path.join(root, name)
        if name.endswith('nc'):  # identify netcdf files by their extension...
            print(fullpath)
            ds = xr.open_dataset(fullpath)  # could wrap this with a try/except
            s = pd.Series(ds.attrs)  # global attributes as a pandas Series object
            s.name = fullpath
            for varname in ds.data_vars:
                if name.startswith(varname):  
                    # the CMIP data files usually have the variable name at the start of the file name
                    s['variable'] = varname  # Add a new field with the variable short name
                    # and add all the metadata from the data variable
                    for name, value in ds[varname].attrs.items():
                        s[name] = value
            datalist.append(s)

metadata = pd.DataFrame(datalist)  # Make a DataFrame object from the list of individual Series objects
print('Writing output to ', output_path)
metadata.to_csv(output_path)  # By default this uses ', ' as the separator and leaves missing values blank