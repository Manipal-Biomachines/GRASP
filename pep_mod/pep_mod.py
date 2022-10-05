"""Peptide modifications
"""
import random
import argparse
import re
import copy
import itertools
import cardinality
import pandas
from scipy.stats import norm


class BAlaS:
    """BUDE Alanine Scan: ddG values
    """
    def __init__(self):
        self.stable_df_bals = self.df_bals = self.df_ddg = None
        self.ddg_threshold = None
        self.positions = []


    def bals_read(self, bals2csv_file):
        """Accepts .csv files converted using bals2csv.py
        """
        self.df_bals = pandas.read_csv(bals2csv_file)
        self.df_bals.set_index(['Index'])

        self.df_bals = self.df_bals[['Number', 'Name', 'IntraDDG']]
        # print("DDG values:\n", self.ddg_bals)

        self.stable_df_bals = self.df_bals[self.df_bals['IntraDDG'] < 0]
        print("Stable DDG values:\n", self.stable_df_bals)

        return self.df_bals


    def replot_read(self, replot_csv_file):
        """Accepts .csv files from replot"""
        df_ddg = pandas.read_csv(replot_csv_file)
        df_ddg = df_ddg[['ResNumber', 'ResName', 'ddGs']]
        # print("DDG values:\n", df_ddg)

        self.df_ddg = df_ddg
        return df_ddg


    def replot_filter(self, mutation_lock=None, lower_threshold=0, upper_threshold=1):
        """Filter out based on ddG thresholds"""
        # Remove mutation_lock positions.
        df_ddg = self.df_ddg
        drop_positions = [int(x)-1 for x in mutation_lock]
        df_unlocked = df_ddg.drop(drop_positions)

        df_lower = df_unlocked[df_unlocked['ddGs'] > lower_threshold]
        ddg_threshold = df_lower[df_lower['ddGs'] < upper_threshold]
        print("DDG values for between", lower_threshold, 
            "and", upper_threshold, "kCal/mol:\n",
            ddg_threshold.sort_values('ddGs', ascending=True))

        self.ddg_threshold = ddg_threshold
        return ddg_threshold


    def replot_get_positions(self, count=5):
        """Get positions from filtered ddG thresholds"""
        ddg_threshold_sorted = self.ddg_threshold.sort_values('ddGs', ascending=True)
        df_res_number = ddg_threshold_sorted[['ResNumber']]
        df_res_number_clipped = df_res_number.head(count)
        df_res_number_clipped.reset_index()

        positions = []
        for _, res_number in df_res_number_clipped.iterrows():
            position = re.search(r'([0-9])+', str(res_number))[0]
            positions.append(position)

        print("B| Positions:", positions)
        self.positions = positions
        return positions


class MutationObject:
    """Mutation format
    """
    def __init__(self, sequence, mutation):
        self.wild_type = self.position = self.mutant_type = None
        self.sequence = sequence
        self.from_str(mutation)


    def from_str(self, mutation):
        """Convert mutation in string format to MutationObject.
        """
        position = re.search(r'([0-9])+', mutation)
        self.position = int(position[0]) if position is not None else self.position

        wild_type = re.search(r'^([A-Za-z])', mutation)
        self.wild_type = wild_type[0] if wild_type is not None else self.wild_type
        if self.wild_type is None:
            self.wild_type = self.sequence[self.position-1]

        mutant_type = re.search(r'([A-Za-z])$', mutation)
        self.mutant_type = mutant_type[0] if mutant_type is not None else self.mutant_type


    def new_mutant_type(self, mut_ty):
        """Create a new MutationObject with a differnt mutant_type attribute.
        """
        new_obj = copy.copy(self)
        new_obj.mutant_type = mut_ty
        return new_obj


    def to_str(self):
        """Convert MutationObject to string format.
        """
        mutant_type = self.mutant_type if self.mutant_type else ''
        mut_str = self.wild_type + str(self.position) + mutant_type
        return mut_str


class Mutater:
    """Mutater: groups, ddg, dipeptide
    """
    def __init__(self, sequence, mutations=None, mutation_lock=None):
        self.groups = {
            'polar_uncharged': ['S', 'T', 'C', 'N', 'Q'],
            'positively_charged': ['K', 'R', 'H'],
            'negatively_charged': ['D', 'E'],
            'nonpolar_aliphatic': ['G', 'A', 'V', 'L', 'M', 'I'],
            'nonpolar_aromatic': ['F', 'Y', 'W']
        }
        self.sequence = sequence
        self.mutations = mutations
        self.mutation_lock = mutation_lock
        self.sequential_mutations = self.sequences_consumable = None
        self.sequences = None


    def append_mutation(self, mut_obj):
        """Append input mutation object to self.mutations
        """
        self.mutations.append(mut_obj)


    def by_groups(self):
        """Returns mutation arrays based on group mutations
        """
        groups = self.groups
        print("G| Original sequence:", self.sequence)

        sequential_mutations = list(self.sequence)
        for mutation in self.mutations:
            print("G| Mutation:", mutation.to_str())
            if mutation.position in self.mutation_lock:
                print("G| Skipping locked position", mutation.position)
                continue
            if mutation.wild_type == 'P':
                print("G| Skipping Proline mutation at", mutation.position)
                continue
            if mutation.mutant_type:
                sequential_mutations[mutation.position-1] = [mutation.mutant_type]
            else:
                # Recognise the group of the mutation.
                for group_type, group in groups.items():
                    if mutation.wild_type in group_type:
                        print("G| => Type:", group_type)
                        possible_muts = copy.copy(group)
                        possible_muts.remove(mutation.wild_type)
                        sequential_mutations[mutation.position-1] = possible_muts
                        break
        self.sequential_mutations = sequential_mutations
        return sequential_mutations


    def to_sequences(self):
        """P&C of new_mutations. nCr approach.
        Choose r mutation positions at a time, out of n mutations.
        Implemented using the Cartesian product."""
        try:
            seqs = [x for x in itertools.product(*self.sequential_mutations)]
            self.sequences_consumable = False
        except: # pylint: disable=bare-except
            seqs = itertools.product(*self.sequential_mutations)
            self.sequences_consumable = True
        print("S| Converted mutations to sequences format")

        self.sequences = seqs
        return seqs


    def show_sequences(self):
        """Print self.sequences"""
        for sequence in self.sequences:
            sequence = "".join(sequence)
            print(sequence)


    def save_sequences(self, file):
        """Save self.sequences to a file"""
        with open(file, "w", encoding='utf8') as opened_file:
            for sequence in self.sequences:
                line = "".join(sequence)
                opened_file.write(f"{line}\n")
        print("S| Saved sequences to", file)


    def remove_dipeptides(self):
        """Remove dipeptides from self.sequences"""
        check_dipeptide = lambda seq: re.search(r"(.)\1", str(seq))
        get_all_dipeptides = lambda seq: re.finditer(r"(.)\1", seq)

        try:
            seqs = [x for x in itertools.filterfalse(check_dipeptide, map("".join, self.sequences))]
            self.sequences_consumable = False
        except: # pylint: disable=bare-except
            seqs = itertools.filterfalse(check_dipeptide, map("".join, self.sequences))
            self.sequences_consumable = True
        print("S| Removed dipeptides from sequences")

        self.sequences = seqs
        return sequences


    def by_intein_sequences(self):
        """[SKIPPED]
        """


    def by_cleavage_sites(self):
        """[SKIPPED]
        """
        # def intein_matches(sequence):
        # inteins = ["CRAZY_SEQUENCE", "ANOTHER_SEQUENCE"]
        # # Put the source as a dictionary or an array, preferably.

        # print("Inteins?: " + str(intein_matches(sequence)))
        # for intein in inteins:
        #   match = str(sequence).find(intein)
        #   return not match


    def by_charge_criterion(self):
        """[SKIPPED]
        """


    def randomise(self):
        """At random positions
        """
        # [TODO]
        # for mutation_position in range(len(sequence)):
        #   sequences = groups_mutations(sequence, [str(mutation_position)])

        # mutation_positions = range(0, len(sequence))
        # new_mutation_positions = []
        # for position in map(str, mutated_positions):
        #   new_mutation_positions.append(str(position))
        # mutated_positions = new_mutation_positions
        # sequences = groups_mutations(sequence, mutation_positions)


    def random_sampler(self, choose=5):
        """Random sampling through random.
        Chooses 5 sequences by default.
        """
        seqs = []
        for seq in map("".join, self.sequences):
            seqs.append(seq)

        try:
            seqs = random.sample(seqs, choose)
            print("S| Sampled", choose, "sequences")
        except: # pylint: disable=bare-except
            pass


        self.sequences = seqs
        return sequences


    def monte_carlo_sampler(self, choose=5):
        """Random sampling through Monte-Carlo.
        A normal distribution is chosen.
        Chooses 5 sequences by default.
        """
        new_sequences = []
        print("S| Choosing", choose)
        # mean, var, skew, kurt = norm.stats(moments='mvsk')
        # [TODO]
        return new_sequences


class sequences:
    def __init__(self):
        pass

    def check_dipeptide(self, sequence):
        """Returns first dipeptide match if present, else None
        """
        match = re.search(r"(.)\1", str(sequence))
        if match: return match[0], match.span()
        return None, None

    def dipeptide_matches(self, sequences):
        """Filters out and returns the non-dipeptide sequences"""
        new_sequences = sequences
        for sequence in sequences:
            if dipeptide_match(sequence):
                new_sequences.pop(sequence)

        print("Dipeptides filtered: " + str(new_sequences))
        return new_sequences

    def dipeptide_mutater(self, sequence, dipeptide, ddg):
        """Mutates to remove dipeptides."""
        groups = {
            'polar_uncharged': ['S', 'T', 'C', 'P', 'N', 'Q'],
            'positively_charged': ['K', 'R', 'H'],
            'negatively_charged': ['D', 'E'],
            'nonpolar_aliphatic': ['G', 'A', 'V', 'L', 'M', 'J', 'I'],
            'nonpolar_aromatic': ['F', 'Y', 'W']
        }
        match, span = dipeptide[0], dipeptide.span()

        # Decide mutation position by comparing ddG values.
        position = span[0]
        lesser_ddg = (ddg['ddGs'][position] > ddg['ddGs'][position+1])
        mutation_position = position+2 if lesser_ddg else position+1
        print("Position", mutation_position, "has lesser ddG value among the dipeptide", match)

        # Conservative replacement.
        contents = [sequence]
        contents.append(str(mutation_position)) # Just one mutation_position.
        print(contents)
        sequence, mutations = format_input(contents)

        # Discard mutations that produce another dipeptide.
        new_mutations = []
        for mutation in mutations:
            if mutation in mutation_lock:
                print("DP: Skipping locked position", mutation['position'])
                continue
            # Recognise the group of the mutation.
            for types in groups.keys():
                if mutation['wild_type'] in groups[types]:
                    for AA in groups[types]:
                        position = int(mutation['position'])
                        if (AA == sequence[position-2])|(AA == sequence[position]):
                            print("Discarding mutation of", mutation['wild_type'],
                                "with", AA, "at", position)
                        else:
                            print("DP: Mutating", mutation['wild_type'],
                                "with", AA, "at", position)
                            new_mutation = mutation['wild_type'] + mutation['position'] + AA
                            new_mutations.append(new_mutation)
                    break
        return new_mutations


def save_as(file, contents):
    content = "\n".join(contents)
    file = open(file, "w")
    file.write(content)


def to_mut_obj(sequence, given_mutations):
    """Convert to MutationObject"""
    remove_new_line = lambda s: str(s).replace('\n', '')

    muts = []
    for line in given_mutations:
        line = remove_new_line(line)
        mut = MutationObject(sequence, line)
        muts.append(mut)

    return muts


def format_input(contents):
    remove_new_line = lambda s: str(s).replace('\n', '')

    sequence = remove_new_line(contents[0])
    given_mutations = contents[1:]

    muts = to_mut_obj(sequence, given_mutations)
    mutations_obj = Mutater(sequence=sequence, mutations=muts, mutation_lock=[])
    return mutations_obj


def main():
    # For the command line parser.
    parser = argparse.ArgumentParser(prog='pep_mod', description='Peptide modifications generator')
    parser.add_argument('input_file', type=str, help='Input file [.txt]')
    parser.add_argument('-o', '--output', dest='output_file', type=str, help='Output filename')
    parser.add_argument('-d', '--dipeptide', action='store_true', help='Dipeptides match')
    parser.add_argument('-g', '--groups', action='store_true', help='Groups filter')
    parser.add_argument('-a', '--alaninescan', help='Alanine scan DDG results from BUDE Alanine scan')
    parser.add_argument('-l', '--lock', type=str, dest='mutation_lock', help='Mutation lock positions')
    parser.add_argument('-c', '--count', type=int, dest='mutation_count', help='Number of mutations to consider at a time', default=1)
    args = parser.parse_args()

    # If --output not specified, use input_file filename.
    output_file = args.output_file if args.output_file else args.input_file

    with open(args.input_file, "r") as file:
        input_contents = file.readlines()
    mutations_obj = format_input(input_contents)
    sequence = mutations_obj.sequence
    sequences = [sequence]

    if args.mutation_lock:
        with open(args.mutation_lock, "r") as file:
            lock_contents = file.readlines()
        mutation_lock = []
        for line in lock_contents:
            content = line.replace('\n', '') # Remove newlines.
            mutation_lock.append(content)
        mutations_obj.mutation_lock = mutation_lock.sort(key=lambda x: int(x))
        print("Locked mutation positions:", mutation_lock)

    if args.groups:
        muts = mutations_obj.by_groups()
        seqs = mutations_obj.to_sequences()
        mutations_obj.save_sequences(output_file.replace(".txt", "_GrpAllSeqs.txt"))


    if args.alaninescan:
        bude = BAlaS()
        df_ddg = bude.replot_read(args.alaninescan)
        ddg_preferences = bude.replot_filter(mutation_lock, 0, 1)
        positions = bude.replot_get_positions(args.mutation_count)

        muts = to_mut_obj(sequence, positions)
        mutations_obj = Mutater(sequence=sequence, mutations=muts, mutation_lock=[])

        muts = mutations_obj.by_groups()
        seqs = mutations_obj.to_sequences()
        mutations_obj.save_sequences(output_file.replace(".txt", "_BAlsAllSeqs.txt"))

    if args.dipeptide:
        seqs = mutations_obj.remove_dipeptides()
        mutations_obj.save_sequences(output_file.replace(".txt", "_SeqsDiPep.txt"))

    # get_unique = lambda seqs: list(dict.fromkeys(seqs))
    # sequences = get_unique(sequences)

    # print("Output sequences:")
    # mutations_obj.show_sequences()
    # print("Output sequences count:", cardinality.count(mutations_obj.sequences))

    seqs = mutations_obj.random_sampler(5)
    mutations_obj.save_sequences(output_file.replace(".txt", "_SeqsRndm.txt"))


if __name__ == "__main__":
    main()
