> ***Peptide sequence mutator through Alanine Scanning***

l=l [PEP_MOD Image]

## Table of contents

-  [Description](#description)
-  [Usage](#usage)
-  [Contributing](#contribution)
-  [License](#license)

# About

> *For more information, refer to our page on our wiki: **https://2022.igem.wiki/mit-mahe/software***

l=l [GIF animation]

## Description

The software mainly comprises of the following modules:

1. **Alanine Scan ddG values**
   BUDE Alanine scan is employed to obtain ddG values of each residue present in the input.

2. **Conservative mutations**

   Conserved mutation is a process in which mutations are made within the same type of residues.

   *For example*: Hydrophobic residues are replaced by hydrophobic residues. In our case we delved deeper into this by replacing it w.r.t to charge as well.

3. **Random sampler**
   We select certain samples from the huge sequence list recieved as the output to reduce users work load. The selection happening is completely random.

## Features

1. **Command Line Interface (CLI)**
   We can use the software locally on command prompt.

2. **Integrable modules**

   While running the software we can include different functions and libraries of python and basically run the software on different python environments.

3. **Mutation lock**
   To prevent the remutation of an already modified residue we put that part of the sequence into a mutation lock.

4. **Aggrescan**

   A BASH scipt is been included which takes the output and prepends FASTA headers to each sequence in the text file.

## Background

l=l [About Protein Engineering]

l=l [This is wrong, need to change] During peptide design and engineering, there's the issue of dealing with infinitely long sample set of the substitutions that could be make to increase the affinity. In order to solve this problem we looked into many open-source softwares that could do point mutations for us but the drawback with those was that they only took information of the residues into consiederation. This would lead to conformational and possibly fuctional changes in the peptide.

## Available current alternatives

l=l PhageModifier

https://2018.igem.org/Team:IISc-Bangalore/Software

# Installation

## Linux/Unix

1. Open terminal and go to a directory where you want to installation files to be downloaded to.

   ```shell
   cd path_to_directory
   ```

2. Clone the repository

   ```shell
   git clone https://gitlab.igem.org/2022/software-tools/mit-mahe.git
   ```

## macOS

1. Install Homebrew, if not already installed.

```shell
brew install 
```

2. 
3. 

## Windows

l=l

## Install dependencies

l=l

## Compilation from source

l=l

# Usage

l=l

**Input**: A docked structure of a receptor and a ligand.

**Output** Text file containing all the possible sequences of mutations. Additionally a text file of randomly sampled mutations is also created.

# Contribution

l=l [Guildlines and future scope of the project]

## Authors and acknowledgement

iGEM MIT_MAHE 2022

## License

This project falls under the MIT license.
