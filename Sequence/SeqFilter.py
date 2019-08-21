from Bio import SeqIO

class SeqFilter:
    def __init__(self, seq_gen):
        self.seq_gen = seq_gen

    def filter(self, phred_threshold):
        for seq in self.seq_gen:
            if min(seq.letter_annotations['phred_quality']) < phred_threshold:
                return 0

