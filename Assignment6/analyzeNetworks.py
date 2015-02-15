import pandas as pd

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
