"""
.bals to .csv converter
"""
import argparse
from json import dumps as json_dumps
import pandas as pd

def _main():
	# For the command line parser.
	parser = argparse.ArgumentParser(description='.bals to .csv converter')
	parser.add_argument('input_file', type=str, help='Input .bals file')
	parser.add_argument('-o', '--output', dest='output_file', type=str, help='Output filename')
	args = parser.parse_args()

	with open(args.input_file, "r") as file:
	    contents = file.readlines()

	json_contents = {
		"Index": [], "Number": [], "Name": [], "Chain": [], 
		"InterDG": [], "InterDDG": [], "NormTerDDG": [], 
		"IntraDG": [], "IntraDDG": [], "NormTraDDG": [], 
		"ChainAtoms": [] }

	for line in contents:
		if line.startswith("#"): continue

		value = line[0:6].strip()
		try: json_contents["Index"].append(int(value))
		except: pass

		value = line[6:13].strip()
		try: json_contents["Number"].append(int(value))
		except: pass

		value = line[13:18].strip()
		try: json_contents["Name"].append(str(value))
		except: pass

		value = line[18:24].strip()
		try: json_contents["Chain"].append(str(value))
		except: pass

		value = line[24:36].strip()
		try: json_contents["InterDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[36:48].strip()
		try: json_contents["InterDDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[48:60].strip()
		try: json_contents["NormTerDDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[60:72].strip()
		try: json_contents["IntraDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[72:84].strip()
		try: json_contents["IntraDDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[84:96].strip()
		try: json_contents["NormTraDDG"].append(str(round(float(value), 4)))
		except: pass

		value = line[96:107].strip()
		try: json_contents["ChainAtoms"].append(int(value))
		except: pass

	json_contents = json_dumps(json_contents)

	# Save as .json
	json_file = args.input_file.replace(".bals", ".json")
	file = open(json_file, "w")
	file.write(str(json_contents))

	# Save as .csv
	with open(json_file, encoding='utf-8') as file:
		df = pd.read_json(file)
	csv_file = args.input_file.replace(".bals", ".csv")
	df.to_csv(csv_file, encoding='utf-8', index=False)

if __name__ == "__main__":
	_main()
