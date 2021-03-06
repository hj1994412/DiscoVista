#!/usr/bin/env python

import os
import sys
import dendropy


def get_present_taxa(tree, labels):
	ptaxa = list()
	for label in labels:
		x = tree.find_node_with_taxon_label(label)
		if x is None:
			print "The species '" + label + "' was not found in the species tree. Please check your annotation file"
			sys.exit(1)
		else:
			ptaxa.append(x.taxon)	
	return ptaxa
def is_mono(tree, clades):
        tree_tmp = tree.clone(depth=1)
	alltmp = tree_tmp.encode_bipartitions(is_bipartitions_mutable = True)
        allBiparts = [ t.compile_split_bitmask() for t in alltmp ]
	taxon_namespace = tree.taxon_namespace
	taxa = get_present_taxa(tree, clades)
	otherside = set(taxon_namespace)-set(taxa)
        bipartition = taxon_namespace.taxa_bipartition(taxa=taxa,is_bipartitions_updated=True)
	othersidebipart = taxon_namespace.taxa_bipartition(taxa=otherside,is_bipartitions_updated=True)
        bipartition = bipartition.compile_split_bitmask()
	othesidebipart = othersidebipart.compile_split_bitmask()
        allBiparts = set(allBiparts)
        return (bipartition in allBiparts or othesidebipart in allBiparts)

if not os.path.exists(sys.argv[1]):
	print("species tree you've entered is not found! please check your species tree")
	sys.exit(1)
tree = dendropy.Tree.get_from_path(sys.argv[1], 'newick', preserve_underscores=True,rooting="default-unrooted")
if not os.path.exists(sys.argv[2]):
	print("annotation file is not found! please check your annotation file")
	sys.exit(1)
anot = (open(sys.argv[2],'r')).readlines()

clades = dict()

for line in anot:
	line = line.replace('\n','')
	line = line.strip('\n')
	line = line.strip()
	listLine = line.split('\t')
	x = tree.find_node_with_taxon_label(listLine[0])
	if x is None:
		print "The species '" + listLine[0] + "' was not found in the species tree. Please check your annotation file"
		sys.exit(1)
	if listLine[1] in clades:
		
		clades[listLine[1]].append(listLine[0])
	else:
		clades[listLine[1]] = list()
		clades[listLine[1]].append(listLine[0])

for clade in clades:
	m = is_mono(tree, set(clades[clade]))
	
	print m, clades[clade], clade
	if m:
		continue
	else:
		print "The annotation file you've passed is not monophyletic for the clade " + str(clade).strip("\n") + ". Please check your annotation file."
		sys.exit(1)

print "All clades specified in the annotation file are monophyletic"

