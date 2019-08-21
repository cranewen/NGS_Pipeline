from Bio import SeqIO
import time

# fastq file reader
class Reader:
    def __init__(self, file_path):
        self.file_path = file_path
    # read fastq file from SeqIO, store the information as generator
    def parse_fastq(self):
        for record in SeqIO.parse(self.file_path, "fastq"):
            yield record
    '''
    def parse_fastq_seq(self):
        record = [record for record in SeqIO.parse(self.file_path, "fastq")]
        record_seq = [record[0].seq for record[0].seq in record]
        return record_seq
    '''

def main():
    r = Reader("../data/20181010/Anc81C1Hamilton_S4_L001_R1_001.fastq")
    # seqs = r.parse_fastq()
    # t0 = time.time()
    # f = open("../data/test_seq_anc81.txt", "w")
    # for s in seqs:
    #     f.write(str(s.seq) + "\n")
    #     # print(s.description)
    #     # print(s.name)
    # f.close()
    # t1 = time.time() - t0


if __name__ == '__main__':
    main()