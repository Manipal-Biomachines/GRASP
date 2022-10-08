> ***Peptide sequence mutator through Alanine Scanning***

l=l [PEP_MOD Image]

## Table of contents

-  [Description](#description)
-  [Usage](#usage)
-  [Contributing](#contribution)
-  [License](#license)

# About

> *For more information, refer to this page on our wiki: **https://2022.igem.wiki/mit-mahe/software***

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

Protein engineering is the process of modifying a protein through substitution, Insertion, or deletion so that it can exhibit certain characteristics and properties that we desire. During the process of designing our peptide, we came across the problem of having a very large sample set of substitutions through trial and error. However, even after this we could not guarantee an increase in affinity as compared to the original peptide as needed in our case. To overcome this problem, we designed this software which will provide all the most probable mutations that increase the binding affinity.

Furthermore, we explored other point mutation softwares for our problem; however, they only took surface information into consideration. We decided to take ddG value of a residue as the parameter for mutation which give an increase in the accuracy of the mutation.

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

## Flags

-g

-a

-o

-d

-g

-a

-l

-c

# Method

## ddG threshold

We take ddG value of each residue derived from BUDE alanine scan as a parameter to do mutations. To make these mutations we set a threshold ddG range for each residue (in our case, 0 to 1). Only if the ddG value lies between this range will it be mutated.

## Significance of Cartesian product

*Cartesian Product*: The Cartesian Product of sets $A$ and $B$ is defined as the set of all ordered pairs $(x, y)$ such that $x$ belongs to $A$ and $y$ belongs to $B$. 
For example, if $A = {1, 2}$ and $B = {3, 4, 5}$, then the Cartesian Product of A and B is ${(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)}$. 

Originally, during a test run, the computational time that the software took for making 3 mutation positions was 2 hours 20 mins.
After incorporating the cartesian product into the mutator, the time reduced to 11 mutation positions in 10 seconds.

## Algorithm

We first create a Mutater object, which support the following three formats:

1. Wild type amino acid, the position of the Amino acid, and the Mutant type it needs to be replaced with.
2. Just the Wild type amino acid and its position, without the Mutant type. This can act as the template to create new Mutater objects.
3. Just the position in the sequence.

### Alanine scanning

The Alanine scanning results from BUDE Alanine scan are parsed through which results in a position array over which mutations are possibly required.

### Group mutations

The sequence is taken as a template over which a special array is constructed, with the following steps:

1. Iterate over the sequence and get the wild type amino acid at each stage.
2. Retain the wild type if mutation isn't required at this position. This could result when the position doesn't want to be mutated, or when the position is present in the *mutation lock array*.
3. If a mutation is required in the current position, replace the position with an array of all the possible amino acids within the same group. This step is important to achieve *Conserved mutations.*

### Cartesian product

The special array is then passed to the `itertools.product()` function, which evaluates the Cartesian product on the elements of the special array. This results in an `iterable object`  that contains all the final sequences, which is then stored in the text file.

### Random sample

A trivial random sampler is implemented using `random.sample()` on the sequences array, and then stored in a text file.

# Contribution

l=l [Guildlines and future scope of the project]

l=l Involving a Monte Carlo approach of sampling

## Authors and acknowledgement

iGEM MIT_MAHE 2022

## License

This project is licensed under the Creative Commons Attribution 4.0 International.
[Learn more](http://choosealicense.com/licenses/cc-by-4.0/)
