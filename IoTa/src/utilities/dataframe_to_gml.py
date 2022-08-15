import sys, time
import pandas as pd

def convert_to_gml(gml_file_name, segregated_iota, unique_addresses):
    
    segregated_iota_df = pd.read_csv(segregated_iota, sep=',')
    unique_addresses_df = pd.read_csv(unique_addresses, sep=',')
    
    f = open(gml_file_name, "w")
    #helpers
    s = " "
    ss = s+s
    sss = s+s+s
    ssss = s+s+s+s
    nl = "\n"

    #Root node
    f.write("graph"+nl)
    f.write("[")
    f.write("directed 1"+nl)

    #Write an edge
    def write_edge(row):
        f.write( ss + "edge" + nl)
        f.write( ss + "[" + nl)
        f.write( ssss + "source" + s + '"' + str(row[11]) + '"' + nl)
        f.write( ssss + "target" + s + '"' + str(row[12]) + '"' + nl)
        f.write( ssss + "value" + s + str(row[10]) + nl) # segregated_iota_df['count']
        f.write( ss + "]"+ nl)

    #Write a node
    def write_node(node):
        f.write( ss + "node" + nl)
        f.write( ss + "[" + nl)
        f.write( ssss + "id" + s + '"' + str(node[1]) + '"' + nl) # Node id
        f.write( ssss + "label" + s + '"' + str(node[0]) + '"' + nl) # Node name
        f.write( ss + "]"+ nl)

    #Generate nodes
    unique_addresses_df.apply(write_node, axis=1)

    print(nl+"Printing nodes over")
    
    #flush index
    ind = 0
    added_edges = []


    #Generate edges
    def edges(row):
        if(row[11] != row[12]): # row[11] is input addrs and row[12] is output addrs
            if((row[11], row[12]) not in added_edges):
                added_edges.append((row[11], row[12]))
                write_edge(row)
        return

    segregated_iota_df.apply(edges, axis = 1)


    print(nl+"Printing nodes and edges over")

    #closing node
    f.write("]"+nl)
    f.close()