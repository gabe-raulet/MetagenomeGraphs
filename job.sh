#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=3
#SBATCH --time=30
#SBATCH --constraint=haswell
#SBATCH --ntasks=3

module load python
conda activate camisim

CAMISIM_PATH=/global/homes/g/gabeh98/CAMISIM
srun -N 1 -n 1 -c 64 --cpu_bind=cores python /global/homes/g/gabeh98/CAMISIM/metagenomesimulation.py /global/homes/g/gabeh98/MetagenomeGraphs/Experiments/sim1/config.ini &
srun -N 1 -n 1 -c 64 --cpu_bind=cores python /global/homes/g/gabeh98/CAMISIM/metagenomesimulation.py /global/homes/g/gabeh98/MetagenomeGraphs/Experiments/sim2/config.ini &
srun -N 1 -n 1 -c 64 --cpu_bind=cores python /global/homes/g/gabeh98/CAMISIM/metagenomesimulation.py /global/homes/g/gabeh98/MetagenomeGraphs/Experiments/sim3/config.ini &
wait
