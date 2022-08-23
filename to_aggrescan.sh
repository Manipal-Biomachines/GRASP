#!/bin/bash

# Adds FASTA headers to every sequence in sequences.txt

file="$1"
new_file="${file//.txt/_aggrescan.txt}"
echo "Creating ${new_file}"
touch "${new_file}"

# Erase file.
cat > "${new_file}" <<EOF
EOF

i=1
while read line; do
	cat >> "${new_file}" <<EOF
> Sequence_$i
${line}
EOF
i=$((i+1))
done < "${file}"
