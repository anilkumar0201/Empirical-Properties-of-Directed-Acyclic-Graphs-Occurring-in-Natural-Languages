# Using NetworkX package and conllu package
# Using NetworkX package and conllu package
# This is baseline conditions module; more conditions can be added as functions
import os
from io import open
import networkx as nx
from operator import itemgetter
import random
from Measures_rand import *
from Measures import *
import treegen as gen
import depgraph as dep

class Random_base(object):
    def __init__(self, tree):                   # tree has an abstract node=0 and real nodes =1,2,... 
        self.tree=tree
        self.ls_rand=[]
    
    def num_cross_rand(self,randtree,abs_root):
        comput=Compute_measures_rand(randtree,abs_root)
        ncross_random=0
        for edgex in randtree.edges:
            if not edgex[0]==abs_root: 
                if comput.is_projective(edgex):
                    ncross_random += 0
                else:
                    ncross_random += 1
        return ncross_random

    def is_equal_num_crossings(self,randtree,abs_root,num_cross_real):
        flag=False
        num_cross_random=self.num_cross_rand(randtree,abs_root)
        if num_cross_random==num_cross_real:
            flag=True
        return flag
    
    def is_similar_DD_distribution(self,randtree,abs_root):
        find=Compute_measures_rand(randtree,abs_root)
        rand_tree=nx.DiGraph()
        for edgex in randtree.edges:
            if not edgex[0]==abs_root:
                rand_tree.add_edge(edgex[0],edgex[1])
        
        random_dd_sample=[]
        for edgey in rand_tree.edges:
            random_dd_sample.append(find.dependency_distance(edgey))
        random_dd_sample.sort()
        
        get=Compute_measures(self.tree)
        real_tree = nx.DiGraph()
        for edgez in self.tree.edges:
            if not edgez[0]==0:
                real_tree.add_edge(edgez[0],edgez[1])

        real_dd_sample=[]
        for edgev in real_tree.edges:
            real_dd_sample.append(get.dependency_distance(edgev))
        real_dd_sample.sort()

        return random_dd_sample==real_dd_sample

    def rand_tree(self,n,num_cross_real):
        code=gen.random_pruefer_code(n)
        all_rand_trees = list(gen.directed_trees(gen.tree_from_pruefer_code(code)))
        random.shuffle(all_rand_trees)

        for treex in all_rand_trees:
            real_root=next(nx.topological_sort(treex))
            abstract_root=1000
            treex.add_edge(abstract_root,real_root)

            for edgex in treex.edges:
                treex.nodes[edgex[1]]['head']=edgex[0]

            if self.is_equal_num_crossings(treex,abstract_root,num_cross_real):
                self.ls_rand.append(treex)
                break

    def gen_random(self,num_cross_real):
        n = len(self.tree.edges)
        rand_out=[]
        x=0

        if n<16:

            # CHANGED ONLY THIS LINE
            while (len(self.ls_rand)<10) and x<40000:

                x=x+1
                self.rand_tree(n,num_cross_real)
                rand_out=self.ls_rand

        return rand_out