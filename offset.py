import argparse
import glob
import re

summary = ("adds the specified offset (in seconds, default +0.009) to all .sm "
   "and .ssc files found in the specified directories and their subdirectories")
filetypes = {"ssc", "sm"}
find = r"(#OFFSET:)([-+]?\d+\.\d+)(;)"
replace = r"\g<1>{:.3f}\g<3>"

parser = argparse.ArgumentParser(description=summary)
parser.add_argument("directory", nargs="*")
parser.add_argument("--offset", type=float, default=0.009)
parser.add_argument("--ignore", choices=filetypes, action="append", default=[])
parser.add_argument("--noprompt", action="store_true")
args = parser.parse_args()

for ext in filetypes - set(args.ignore):
   filepaths = []
   for dir in args.directory:
      filepaths.extend(glob.glob("{}/**/*.{}".format(dir, ext), recursive=True))
      print("Found {} .{} files under {}".format(len(filepaths), ext, dir))
   for path in set(filepaths):
      with open(path, "r+", encoding="utf-8", newline="\n") as file:
         contents = file.read()
         try:
            oldoffset = float(re.search(find, contents).group(2))
         except:
            print("Could not read offset of {}".format(path))
            continue
         newoffset = args.offset + oldoffset
         detail = ("offset of {} from {:.3f} to {:.3f} ({:+.3f})"
            .format(path, oldoffset, newoffset, args.offset))
         if args.noprompt or input("Change {}? [y/n] ".format(detail)).lower() == "y":
            contents = re.sub(find, replace.format(newoffset), contents)
            file.seek(0)
            file.write(contents)
            print("Changed {}".format(detail))