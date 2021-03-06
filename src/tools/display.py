#!/usr/bin/env python

import dendropy
import sys
import os
import re


tree = dendropy.Tree.get(path=sys.argv[1],schema="newick",rooting="default-rooted")
outgroup = sys.argv[2]
outgroup_node = tree.find_node_with_taxon_label(outgroup)
new_root = tree.reroot_at_edge(outgroup_node.edge,suppress_unifurcations=True)
I = set()
Orig = set()
b=0
for nd in tree.postorder_internal_node_iter():
	b += 1
	if nd.label is not None and re.findall("N",nd.label):
		I.add(int(nd.label.replace("N","")))
		Orig.add(nd)
	

L = range(1, 2*len(tree.leaf_nodes()) )
O = list(set(L) - I)
c = 0
for nd in tree.preorder_node_iter():
	if  nd in Orig:
		nd.edge.length = int(nd.label.replace("N",""))
	else:	
		nd.edge.length = int(O[c])
		c += 1
children = new_root.child_nodes()
for c in children:
	if c.taxon.label is not None and c.taxon.label == outgroup:
		tmplabel = c.edge.length
		other = list(set(children)-{c})
		break
other[0].edge.label = None
other[0].edge.length = None
tree.write(path=sys.argv[1]+".out",schema= "newick",
        suppress_internal_taxon_labels=False,
        suppress_internal_node_labels=False,
        suppress_rooting=True,
        suppress_edge_lengths=False,
        unquoted_underscores=False,
        preserve_spaces=False,
        store_tree_weights=False,
        suppress_annotations=False,
        suppress_item_comments=False)
