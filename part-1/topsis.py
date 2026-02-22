import sys
import pandas as pd
import numpy as np

input_file = sys.argv[1]
weights = sys.argv[2]
impacts = sys.argv[3]
output_file = sys.argv[4]

#checking for errors
if len(sys.argv) != 5:
    print("Incorrect number of parameters")
    sys.exit(1)

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print("File not found")
    sys.exit(1)

if df.shape[1] < 3:
    print("Input file must contain three or more columns")

data = df.iloc[:,1:].apply(pd.to_numeric)

weights = list(map(float, weights.split(',')))
impacts = impacts.split(',')

if len(weights) != df.shape[1]:
    print("Weights count mismatch")

for i in impacts:
    if i not in ['+','-']:
        print("Impacts must be + or -")

    # Step 1: Normalize Matrix

    norm = np.sqrt((data**2).sum())
    normalized_data = data / norm

    
    # Step 2: Weighted Matrix
    
    weighted_data = normalized_data * weights

    
    # Step 3: Ideal Best & Worst
    
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

    
    # Step 4: Distance Calculation
    
    distance_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

   
    # Step 5: Performance Score
    
    scores = distance_worst / (distance_best + distance_worst)

   
    # Step 6: Ranking
    
    df['Topsis Score'] = scores
    df['Rank'] = df['Topsis Score'].rank(method='max', ascending=False).astype(int)

   
    # Save Output
    
    df.to_csv(output_file, index=False)
    print("TOPSIS successfully calculated. Results saved to", output_file)


