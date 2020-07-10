import sys
import shutil
import os
import subprocess as sp
import glob

home_pathdir           = os.path.abspath(sys.argv[1])
experiments_pathdir    = os.path.abspath(sys.argv[2])
work_pathdir           = os.path.abspath(sys.argv[3])


def paths_file_to_dict(path_to_paths_file):
    paths_dict = dict()
    with open(path_to_paths_file, "r") as paths_handler:
        for line in paths_handler.readlines():
            key, path = line.rstrip().split("=")
            assert os.path.exists(path)
            paths_dict[key] = path
    return paths_dict

def parameters_file_to_dict(path_to_parameters_file):
    parameters_dict = dict()
    with open(path_to_parameters_file, "r") as parameters_handler:
        for line in parameters_handler.readlines():
            key, parameter = line.rstrip().split("=")
            parameters_dict[key] = parameter
    return parameters_dict

def generate_programmed_config():
    boilerplate_path = home_pathdir + "/Configurations/boilerplate.ini"
    program_file     = home_pathdir + "/Configurations/program_paths.txt"
    data_paths       = home_pathdir + "/Configurations/data_paths.txt"

    assert os.path.isfile(boilerplate_path)
    assert os.path.isfile(program_file)
    assert os.path.isfile(data_paths)

    program_dict   = paths_file_to_dict(program_file)
    data_path_dict = paths_file_to_dict(data_paths)

    with open(boilerplate_path, "r") as bplate:
        config = bplate.read()

    config = config.replace("{SAMTOOLS}",       program_dict['SAMTOOLS'])
    config = config.replace("{PBSIM}",          program_dict['PBSIM'])
    config = config.replace("{ERROR_PROFILES}", program_dict['ERROR_PROFILES'])
    config = config.replace("{STRAIN_SIM}",     program_dict['STRAIN_SIM'])

    config = config.replace("{TAXDUMP}",      data_path_dict['TAXDUMP'])
    config = config.replace("{METADATA}",     data_path_dict['METADATA'])
    config = config.replace("{ID_TO_GENOME}", data_path_dict['ID_TO_GENOME'])

    config = config.replace("{TMP_DIR}", experiments_pathdir + "/tmp")

    num_genomes = str(sum(1 for line in open(data_path_dict['METADATA'])) - 1)

    config = config.replace("{GENOMES_TOTAL}", num_genomes)
    config = config.replace("{GENOMES_REAL}",  num_genomes)

    with open(experiments_pathdir + "/programmed_config.ini", "w") as f:
        f.write(config)

def setup_experiment(experimental_parameter_file):
    parameters_dict = parameters_file_to_dict(experimental_parameter_file)

    with open(experiments_pathdir + "/programmed_config.ini", "r") as f:
        config = f.read()

    config = config.replace("{SIZE}",           parameters_dict["SIZE"])
    config = config.replace("{FRAG_SIZE_MEAN}", parameters_dict["FRAG_SIZE_MEAN"])
    config = config.replace("{FRAG_SIZE_SD}",   parameters_dict["FRAG_SIZE_SD"])

    experiment_pathdir = experiments_pathdir + "/" + parameters_dict["RUN_NAME"]
    assert not os.path.exists(experiment_pathdir)
    os.mkdir(experiment_pathdir)

    camisim_pathdir = experiment_pathdir + "/CAMISIM_output"
    os.mkdir(camisim_pathdir)
    config = config.replace("{OUTPUT_DIR}", camisim_pathdir)

    with open(experiment_pathdir + "/config.ini", "w") as f:
        f.write(config)

    shutil.copyfile(experimental_parameter_file, experiment_pathdir + "/parameters.txt")

if __name__ == "__main__":
    assert os.path.exists(experiments_pathdir)
    assert os.path.exists(home_pathdir)
    sys.stderr.write("Paths:\n"
                      "====================\n")
    sys.stderr.write( "Home directory path:        {}"
                    "\nExperiments directory path: {}"
                    "\nWork directory path:        {}"
                    "\n\n".format(home_pathdir, experiments_pathdir, work_pathdir))
    sys.stderr.flush()

    experimental_parameters_pathdir = experiments_pathdir + "/parameters"
    assert os.path.exists(experimental_parameters_pathdir)

    generate_programmed_config()

    sys.stderr.write("Experimental parameters files:\n"
                      "====================\n")
    for experimental_parameter_file in os.listdir(experimental_parameters_pathdir):
        experimental_parameter_file = os.path.join(experimental_parameters_pathdir, experimental_parameter_file)
        sys.stderr.write(experimental_parameter_file + "\n")
        sys.stderr.flush()
        setup_experiment(experimental_parameter_file)




