"""
Literally don't ever run this. It erases all the data kept in the system as it sets things up. If you've already
got data (such as if you're piggybacking off the stuff we provided) don't touch this, our Thanos will death-snap all of our data
along with your petty souls.
"""
from human_backend import init_data_files


init_data_files()
