from Bio import SeqIO
from Bio.Seq import Seq


# Trimming the sequence with given upstream and downstream adapters, with filtering phred_threshold and minimum read length
# The the sequence processes are kept as biopython Seq.record type
# e.g. Using sequence.seq to get the sequence from the record

class Trimmer:
    def __init__(self, upstream_adaptor, downstream_adaptor):
        self.upstream_adaptor = upstream_adaptor
        self.downstream_adaptor = downstream_adaptor
        self.min_len = 0
        self.phred_threshold = 30
        self.trimmed_seq = ''

    def set_min_len(self, min_len):
        self.min_len = min_len

    def set_phred_threshold(self, phred_threshold):
        self.phred_threshold = phred_threshold

    def get_trimmed_seq(self):
        return self.trimmed_seq

    def trim(self, sequence):
        seq_len = len(sequence.seq)
        upstream_adaptor_len = len(self.upstream_adaptor)
        downstream_adaptor_len = len(self.downstream_adaptor)
        up_index = sequence.seq.find(self.upstream_adaptor)  # upstream_adaptor start index
        down_index = sequence.seq.find(self.downstream_adaptor)  # downstream_adaptor start index

        if (up_index != -1 and self.upstream_adaptor != ""):
            if (down_index != -1):
                if (down_index - up_index > upstream_adaptor_len + self.min_len - 1):
                    self.trimmed_seq = sequence.seq[up_index + upstream_adaptor_len: down_index]
                else:
                    self.trimmed_seq = ''
            else:
                self.trimmed_seq = ''
        else:
            self.trimmed_seq = ''

        if self.trimmed_seq != '':
            # record has letter_annotations['phred_quality'] variable, which is a list of quality scores match every
            # single letter in the strand
            if min(sequence.letter_annotations['phred_quality'][up_index + upstream_adaptor_len: down_index]) < \
                    self.phred_threshold:
                self.trimmed_seq = ''

    # reverse complementary trim
    def reverse_trim(self, sequence):
        seq_len = len(sequence.seq)
        upstream_adaptor_len = len(self.upstream_adaptor)
        downstream_adaptor_len = len(self.downstream_adaptor)
        seq = sequence.seq.reverse_complement()
        up_index = seq.find(self.upstream_adaptor)  # upstream_adaptor start index
        down_index = seq.find(self.downstream_adaptor)  # downstream_adaptor start index

        if (up_index != -1 and self.upstream_adaptor != ""):
            if (down_index != -1):
                if (down_index - up_index > upstream_adaptor_len + self.min_len - 1):
                    self.trimmed_seq = seq[up_index + upstream_adaptor_len: down_index]
                else:
                    self.trimmed_seq = ''
            else:
                self.trimmed_seq = ''
        else:
            self.trimmed_seq = ''

        if self.trimmed_seq != '':
            # record has letter_annotations['phred_quality'] variable, which is a list of quality scores match every
            # single letter in the strand
            if min(sequence.reverse_complement().letter_annotations['phred_quality'][up_index + upstream_adaptor_len: down_index]) < \
                    self.phred_threshold:
                self.trimmed_seq = ''

    # Only for Anc81
    def trim_anc81(self, sequence):
        seq_len = len(str(sequence.seq))
        upstream_adaptor_len = len(self.upstream_adaptor)
        up_index = str(sequence.seq).find(self.upstream_adaptor)
        if (up_index != -1 and self.upstream_adaptor != ''):
            if (up_index + upstream_adaptor_len < seq_len - 81):
                self.trimmed_seq = str(sequence.seq)[up_index + upstream_adaptor_len : up_index + upstream_adaptor_len + 81]
            else:
                self.trimmed_seq = ''
        if self.trimmed_seq != '':
            if min(sequence.letter_annotations['phred_quality'][
                   up_index + upstream_adaptor_len : up_index + upstream_adaptor_len + 81]) < self.phred_threshold:
                self.trimmed_seq = ''

    # reverse complement trim for Anc81
    def reverse_trim_anc81(self, sequence):
        seq_len = len(str(sequence.seq))
        upstream_adaptor_len = len(self.upstream_adaptor)
        reversed_seq = sequence.seq.reverse_complement()
        up_index = str(reversed_seq).find(self.upstream_adaptor)
        if (up_index != -1 and self.upstream_adaptor != ''):
            if (up_index + upstream_adaptor_len < seq_len - 81):
                self.trimmed_seq = str(reversed_seq)[up_index + upstream_adaptor_len : up_index + upstream_adaptor_len + 81]
            else:
                self.trimmed_seq = ''
        if self.trimmed_seq != '':
            if min(sequence.reverse_complement().letter_annotations['phred_quality'][
                   up_index + upstream_adaptor_len : up_index + upstream_adaptor_len + 81]) < self.phred_threshold:
                self.trimmed_seq = ''
