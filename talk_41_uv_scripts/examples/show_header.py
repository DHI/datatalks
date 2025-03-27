# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mikeio",
# ]
# ///
import mikeio
import sys
print(mikeio.open(sys.argv[1]))