from AAV.Application_qsub import Application
from AAV.Application_qsub import init_args
import subprocess
import glob

file_list = glob.glob("data/data/get.broadinstitute.org/pkgs/SN0154643/*.fastq")

for f in file_list:
    out_file_path = "Nova_output/"
    init_args(f, out_file_path)
    # a = Application(f, out_file_name)
    arg_list = ['qsub', '-cwd', '-V', '-o', 'Nova_output/output_log/' + f[48:-6] + '.out.txt', '-e', 'Nova_output/output_log/' + f[48:-6] +
                '.err.txt', '-b', 'y', 'python', 'Application_qsub.py']
    # subprocess.run("qsub -cwd -V -o " + "output_log/" + f[48:-6] + ".out.txt"
    #                + "-e " + "output_log/" + f[48:-6] + ".err.txt")

    subprocess.run(arg_list)
