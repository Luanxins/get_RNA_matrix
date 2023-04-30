#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 10:28:00 2020

@author: LuanXins and BingAI
"""

import os
import sys
import argparse

def getFPKM(gtf_file):
    """
    get FPKM from stringtie gtf file
    """
    fpkm_dict = {}
    with open(gtf_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if fields[2] == "transcript":
                transcript_id = fields[8].split(";")[0].split()[1].strip('"')
                gene_id = fields[8].split(";")[1].split()[1].strip('"')
                fpkm = float(fields[8].split(";")[3].split()[1].strip('"'))
                fpkm_dict[(gene_id, transcript_id)] = fpkm
    return fpkm_dict

def main():
    parser = argparse.ArgumentParser(description="Get FPKM matrix from stringtie gtf files")
    parser.add_argument("-i", "--input", required=True, help="A tab-delimited file with sample ID and gtf file path in each line")
    parser.add_argument("-g", "--gene_fpkm", required=True, help="Output gene FPKM matrix file")
    parser.add_argument("-t", "--transcript_fpkm", required=True, help="Output transcript FPKM matrix file")
    args = parser.parse_args()

    sample_list = []
    gene_fpkm_dict = {}
    transcript_fpkm_dict = {}

    with open(args.input) as f:
        for line in f:
            sample_id, gtf_file = line.strip().split("\t")
            sample_list.append(sample_id)
            fpkm_dict = getFPKM(gtf_file)
            for (gene_id, transcript_id), fpkm in fpkm_dict.items():
                gene_fpkm_dict.setdefault(gene_id, {})[sample_id] = fpkm
                transcript_fpkm_dict.setdefault((gene_id, transcript_id), {})[sample_id] = fpkm

    with open(args.gene_fpkm, "w") as f:
        f.write("Gene_ID\t" + "\t".join(sample_list) + "\n")
        for gene_id in sorted(gene_fpkm_dict.keys()):
            f.write(gene_id)
            for sample_id in sample_list:
                f.write("\t" + str(gene_fpkm_dict[gene_id].get(sample_id, 0)))
            f.write("\n")

    with open(args.transcript_fpkm, "w") as f:
        f.write("Gene_ID\tTranscript_ID\t" + "\t".join(sample_list) + "\n")
        for (gene_id, transcript_id) in sorted(transcript_fpkm_dict.keys()):
            f.write(gene_id + "\t" + transcript_id)
            for sample_id in sample_list:
                f.write("\t" + str(transcript_fpkm_dict[(gene_id, transcript_id)].get(sample_id, 0)))
            f.write("\n")

if __name__ == "__main__":
    main()
