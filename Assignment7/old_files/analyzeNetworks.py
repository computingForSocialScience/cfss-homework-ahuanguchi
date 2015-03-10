import pandas as pd, networkx as nx, numpy as np

def readEdgeList(filename):
    df = pd.read_csv(filename)
    if len(df.columns) > 2:
        print('Warning: dataframe will be reduced to first two columns')
        df = df[df.columns[0:2]]
    return df

def degree(edgeList, in_or_out):
    if in_or_out == 'in':
        degree_vals = edgeList['artist2'].value_counts()
    elif in_or_out == 'out':
        degree_vals = edgeList['artist1'].value_counts()
    else:
        print("in_or_out can be either 'in' or 'out'")
        return
    return degree_vals

def combineEdgeLists(edgeList1, edgeList2):
    combined = edgeList1.append(edgeList2)
    combined.drop_duplicates(inplace=True)
    return combined

def pandasToNetworkX(edgeList):
    edge_data = edgeList.to_records(index=False)
    g = nx.DiGraph()
    for artist1, artist2 in edge_data:
        g.add_edge(artist1, artist2)
    return g

def randomCentralNode(inputDiGraph):
    dct = nx.eigenvector_centrality(inputDiGraph)
    dct_sum = float(sum(dct.values()))
    nc_dct = dict((k, v / dct_sum) for k, v in dct.items())
    rando = np.random.choice(nc_dct.keys(), p=nc_dct.values())
    return rando
