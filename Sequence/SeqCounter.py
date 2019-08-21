from Bio import SeqIO
from Bio.Seq import Seq
from collections import Counter, defaultdict
from AAV.Sequence import Control
import time


# Needs speed improvement
class SeqCounter:
    # Passing a sequence generator to the constructor
    def __init__(self, seq_gen):
        self.sequence_gen = seq_gen
        self.count_dict = defaultdict()
        self.control_count_dict = defaultdict()

    # count_uniqe & count_uniqe2 has no performance difference
    def count_unique(self):
        c = Counter()
        for x in self.sequence_gen:
            c[str(x)] += 1
        del c[''] # delete empty one
        return c

    # with counting control as well
    def count_unique2(self):
        # count_dict = defaultdict()
        ctrl = Control.Control('control_20180322')
        for x in self.sequence_gen:
            if str(x) in self.count_dict:
                self.count_dict[str(x)] += 1
            else:
                self.count_dict[str(x)] = 1
            ctrl.count_controls(str(x))
            self.control_count_dict = ctrl.control_count_dict

    # The fastest one so far. Converting a generator to a list. Then sort the list, so we can use one loop to put
    # duplicates count into a dictionary
    def count_unique3(self):
        count_dict = defaultdict()
        seq_list = []

        seq_gen = (str(s) for s in self.sequence_gen)

        time2 = time.time()
        seq_list = list(seq_gen)
        time3 = time.time() - time2
        print("converting to list used {}".format(time3))

        time0 = time.time()
        seq_list.sort()
        time1 = time.time() - time0
        print("sorting used {}".format(time1))
        # counting part starts
        temp_seq = seq_list[0]
        seq_list_len = len(seq_list)
        count = 1
        for i in range(1, seq_list_len):
            if (seq_list[i] == temp_seq):
                count += 1
            else:
                temp_seq = seq_list[i]
                count_dict[seq_list[i-1]] = count
                count = 1

        return count_dict

    def count_unique4(self):
        count_dict = defaultdict()
        seq_gen = (str(s) for s in self.sequence_gen)
        seq_set = set(seq_gen)
        return seq_set



def main():
    print("seq counter")
    # seq = SeqCounter(counter_gen())
    # c_gen = seq.count_uniqe()
    #
    # print(c_gen)

if __name__ == '__main__':
    main()

