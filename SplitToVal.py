import csv
import numpy as np

# Read data from the CSV file
train_data = []
with open('train.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        train_data.append(row)

# Group data by conv_id
from collections import defaultdict
data_by_conv_id = defaultdict(list)
for row in train_data:
    data_by_conv_id[row['conv_id']].append(row)

# Shuffle the groups
conv_id_groups = list(data_by_conv_id.values())
np.random.shuffle(conv_id_groups)

# Define the ratio for train/validation split (e.g., 90% train, 10% validation)
train_ratio = 0.9

# Split the groups
num_train_samples = int(len(train_data) * train_ratio)
current_size = 0
train_set = []
validation_set = []

for group in conv_id_groups:
    if current_size < num_train_samples:
        train_set.extend(group)
        current_size += len(group)
    else:
        validation_set.extend(group)

# Define fieldnames based on the keys in the data
fieldnames = train_data[0].keys()

# Write validation data to a CSV file
with open('ValidationSet.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for sample in validation_set:
        writer.writerow(sample)

# Write the updated training data to a CSV file
with open('UpdatedTrainSet.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for sample in train_set:
        writer.writerow(sample)

print("Validation data has been written to ValidationSet.csv")
print("Training data has been updated and written to UpdatedTrainSet.csv")