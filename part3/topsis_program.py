import pandas as pd
import numpy as np
import sys

def run_topsis(input_file, weights, impacts, output_file):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

    if df.shape[1] < 3:
        print("Input file must contain three or more columns")

    data = df.iloc[:,1:].apply(pd.to_numeric)

    weights = list(map(int, weights.split(',')))
    if len(weights) != data.shape[1]:
        print("Weights count mismatch")
        sys.exit(1)

    impacts = impacts.split(',')
    if len(impacts) != data.shape[1]:
        print("Impacts count mismatch")
        sys.exit(1)
        
    for i in impacts:
        if i not in ['+','-']:
            print("Impacts must be + or -")
            sys.exit(1)
            
    # Normalize
    norm = np.sqrt((data**2).sum())
    normalized_data = data / norm

    # Weighted matrix
    weighted_data = normalized_data * weights

    # Ideal best & worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Distance
    distance_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Score
    scores = distance_worst / (distance_best + distance_worst)

    df['Topsis Score'] = scores
    df['Rank'] = df['Topsis Score'].rank(method='max', ascending=False)

    df.to_csv(output_file, index=False)