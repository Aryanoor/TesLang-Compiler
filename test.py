from consts import dictionary
import re
test = "int i=10;"

for pattern in dictionary:
    if re.search(pattern=pattern['REGEX'], string=test):
        print(f"{pattern['VALUE']} {pattern['TOKEN']}")