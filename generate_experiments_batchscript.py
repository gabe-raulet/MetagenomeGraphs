import sys
import shutil
import os
import subprocess as sp
import glob

experiments_pathdir = sys.argv[1]
camisim_path        = sys.argv[2]
qos                 = sys.argv[3]
time                = sys.argv[4]
computer_system     = sys.argv[5]
number_of_cores     = sys.argv[6]


if __name__ == "__main__":
    number_of_experiments = sum(1 for line in open(experiments_pathdir + "/sim_paths.txt"))
    sys.stdout.write("#!/bin/bash\n"
                     "#SBATCH --qos={}\n"
                     "#SBATCH --nodes={}\n"
                     "#SBATCH --time={}\n"
                     "#SBATCH --constraint={}\n"
                     "#SBATCH --ntasks={}\n\n".format(qos, number_of_experiments, time, computer_system, number_of_experiments))

    sys.stdout.write("conda activate camisim\n\n")

    sys.stdout.write("CAMISIM_PATH={}\n".format(camisim_path))
    #  sys.stdout.write("EXPERIMENTS_PATH={}\n\n".format(experiments_pathdir))

    with open(experiments_pathdir + "/sim_paths.txt", "r") as f:
        paths = [path.rstrip() for path in f.readlines()]

    command = ["srun", "-N", "1", "-n", "1", "-c", number_of_cores, "--cpu_bind=cores",
               "python", camisim_path + "/metagenomesimulation.py"]

    command_str = " ".join(command)

    for path in paths:
        sys.stdout.write(command_str + " " + path + "/config.ini &\n")

    sys.stdout.write("wait")
    sys.stdout.flush()


