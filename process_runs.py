import sys
import os
import subprocess as sp
import glob
import shutil

camisim_sample_pathdir = sys.argv[1]
output_pathdir         = sys.argv[2]

def main():
    if os.path.exists(output_pathdir):
        shutil.rmtree(output_pathdir)
    os.mkdir(output_pathdir)

    bamfiles = glob.glob(camisim_sample_pathdir + "/bam/*bam")
    sp.call(["samtools", "merge", output_pathdir + "/read_origins.bam"] + bamfiles)
    command = "bedtools bamtobed -i {}".format(output_pathdir + "/read_origins.bam")
    command += " | awk '{printf \"%s\\t%s\\t%s\\n\", $4, $2, $3}'"
    command += " > {}".format(output_pathdir + "/read_coordinates.txt")
    sp.call(command, shell=True)

    coord_records = []
    with open(output_pathdir + "/read_coordinates.txt", "r") as coords:
        for line in coords.readlines():
            read_id, start_coord, end_coord = line.rstrip().split("\t")
            cluster = read_id.split("-")[0]
            coord_records.append((read_id, int(start_coord), int(end_coord)))

    cgraph = open(output_pathdir + "/correct_graph.network", "w")
    for i, coord_record in enumerate(coord_records):
        current_read, current_start_coord, current_end_coord = coord_record
        j = 1
        while i + j < len(coord_records) and coord_records[i + j][1] <= current_end_coord:
            overlapped_read, overlapped_start_coord, overlapped_end_coord = coord_records[i + j]
            j += 1
            if overlapped_end_coord < current_end_coord:
                continue
            if current_read.split("-")[0] == overlapped_read.split("-")[0]:
                cgraph.write("{}\t{}\t1.0\n".format(current_read, overlapped_read))
    cgraph.close()

if __name__ == "__main__":
    main()
