import networkx as nx
from subprocess import Popen, PIPE, STDOUT
import re

def to_adj_matrix(G):
    """Return the 01-adjacency matrix of the given graph.

    - input: a networkx graph G, assumed to be undirected, loopless, and simple

    - output: a string of integers separated by blanks. The first
      integer is the graph's order n (i.e., the number of
      vertices). Then follow n * n 0s and 1s for the graph's adjacency
      matrix, row by row. This is the input format for tutte_bhkk.
      """
    l= [str(G.order())]
    l.extend( [str(int(G.has_edge(u,v))) for u in G for v in G] )
    return ' '.join(l)

def call_tutte_bhkk(G):
    p= Popen(['./tutte_bhkk'], stdin=PIPE, stdout=PIPE)
    # (out,err)= p.communicate(input=to_adj_matrix(G)) a bytes-like object is required, not 'str'
    (out,err)= p.communicate(input=bytes(to_adj_matrix(G), 'utf-8'))
    ret = str (out)
    #remove the ' and the b
    ret = ret[2:-1]
    return ret

def sp_power(s,i):
    if i==0: return ""
    if i==1: return s
    return s+"**"+str(i)

def to_sp(lines):
    (i,j) = (0,0)
    P = []
    for line in lines.split('\\n'):
        if line == '': continue
        for coeff in line.split(' '):
            
            if int(coeff) >= 1:
                if i==0 and j==0:
                    P.append(coeff +"*"+ "1")
                elif i==0:
                    P.append(coeff +"*"+ sp_power('y',j))
                elif j==0:
                    P.append(coeff +"*"+ sp_power('x',i))
                else:
                    P.append(coeff +"*"+ sp_power('x',i) +"*"+ sp_power('y',j))

            j += 1
        i += 1
        j = 0
    return " + ".join(P)

def tutte_poly(G, output='sp'):
    """Return the Tutte polynomial of the given graph.

    arguments:
    G: a networkx graph. Simple, loopless, umweighted, undirected.
    output: one of  'raw', or 'sp'.

    By default output == 'sp': returns the corresponding sp string 
    with ** as ^ so it can be interpreted by sympy.
    If output == 'raw', returns the raw outpout of tutte_bhkk.
    """
    lines = call_tutte_bhkk(G)

    if output == 'raw':
        return lines
    if output == 'sp':
        return to_sp(lines)

