"""
Include pdb chains.
"""
import sys
import argparse

def _main():
	# For the command line parser.
	parser = argparse.ArgumentParser(description='Modify pdb chains')
	parser.add_argument('input_file', type=str, help='Input .pdb file')
	parser.add_argument('chains', type=list, help='List of chains to be included')
	parser.add_argument('-o', '--output', dest='output_file', type=str, help='Output filename')
	args = parser.parse_args()

	with open(args.input_file, "r") as file:
	    contents = file.readlines()
	
	# If --output not specified, use input_file filename.
	output_file = args.output_file if args.output_file else args.input_file.replace(".pdb", "_chains.pdb")
	new_contents = []

	chains = args.chains
	chains.append("_") # So that last pop doesn't make the list empty.
	chain = chains.pop(0)

	for line in contents:
		if line.startswith("TER") | line.startswith("END"): chain = chains.pop(0)
		new_line = line if not line.startswith("ATOM") else line[:21] + chain + line[22:]
		try: new_contents.append(new_line)
		except: pass
	
	# Save output.
	new_contents = "".join(new_contents)
	file = open(output_file, "w")
	file.write(new_contents)

if __name__ == "__main__":
	_main()
