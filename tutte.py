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
    (out,err)= p.communicate(to_adj_matrix(G))
    return out

def latex_power(s,i):
    if i==0: return ""
    if i==1: return s
    return s+"^"+str(i)

def to_latex(lines):
    (i,j) = (0,0)
    P = []
    for line in lines.split("\n"):
        for coeff in line.split():
            if int(coeff) == 1:
                P.append(latex_power('x',i) + latex_power('y',j) )
            if int(coeff) > 2:
                P.append(coeff + latex_power('x',i) + latex_power('y',j) )
            j += 1
        i += 1
        j = 0
    return " + ".join(P)

def tutte_poly(G, output='lol'):
    """Return the Tutte polynomial of the given graph.

    arguments:
    G: a networkx graph. Simple, loopless, umweighted, undirected.
    output: one of 'lol', 'raw', or 'tex'.

    By default, or if output == 'lol', returns a list of lists L of
    coefficients, where L[i][j] is the coefficient of x^i y^j.  If
    output == 'tex', returns the corresponding tex string. If output
    == 'raw', returns the raw outpout of tutte_bhkk.
    """
    lines = call_tutte_bhkk(G)

    if output == 'raw':
        return lines
    if output == 'lol':
        L = [map(int,l.split()) for l in lines.split('\n')] # string to 2d list
        return filter(len, L)                               # without empty lists
    else:
        return to_latex(lines)

def __test():
    return tutte_poly(nx.petersen_graph()) == [[0, 36, 84, 75, 35, 9, 1],
                                               [36, 168, 171, 65, 10],
                                               [120, 240, 105, 15],
                                               [180, 170, 30],
                                               [170, 70],
                                               [114, 12],
                                               [56],
                                               [21],
                                               [6],
                                               [1]
                                               ]

def usage():
    print "Usage: python tutte.py [OPTIONS]"
    print "Example: python tutte.py --short=\"1--0 1--2 0--2\" --output=tex"
    print "         python tutte.py --petersen\n"
    print " -h, --help      print this message"
    print " -v              pass -v to tutte_bhkk (ignored)"
    print " --short=STRING  parse input graph from STRING"
    print "                 STRING looks like \"1--0 1--2 2--0 3--0\""
    print " --output=FORMAT print output in FORMAT"
    print "                 valid FORMATs are tex, raw"
    print " --petersen      compute Tutte polynomial of the Petersen graph\n"
    print "If neither --short nor --petersen are given, expects edge list on"
    print "standard input. (Two integers per line, separated by space, define edge.)"
    return
    
def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hop:vt", ["help", "output=","short=","petersen"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    output= "raw"
    petersen= False
    short= None
    test= False
    for o, a in opts:
        if o == "-v":
            verbose = True
        if o == "-t":
            test = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            if a not in ["raw", "tex"]:
                assert False, "output format must be raw or tex"
            else: output = a
        elif o in ("-s", "--short"):
            short = a
        elif o in ("-p", "--petersen"):
            petersen= True
        else:
            assert False, "unhandled option"

    if test:
        if __test():
            print "tutte.py: Test passed"
            sys.exit()
        else:
            print "tutte.py: Test failed"
            sys.exit(1)
            
    if petersen:
        G = nx.petersen_graph()
    elif short:
        lines = map(lambda e: re.sub('--',' ',e), short.split())
        G = nx.parse_edgelist(lines)
    else:
        lines= sys.stdin.readlines()
        G = nx.parse_edgelist(lines)

    print tutte_poly(G, output)


if __name__ == "__main__":
    import sys
    import getopt
    main(sys.argv)
