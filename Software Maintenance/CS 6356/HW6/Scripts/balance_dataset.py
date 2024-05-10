import pandas as pd

# Load the dataset
df = pd.read_csv("/Users/pritul/Downloads/final_dataset_se.csv")

# Count the number of buggy and non-buggy instances
num_buggy = df["bug"].sum()
num_non_buggy = len(df) - num_buggy

# Calculate the target number of buggy instances for each ratio
ratios = [0.2, 0.3, 0.4, 0.5]
target_num_buggy = [int(num_non_buggy * ratio) for ratio in ratios]

# Duplicate the buggy instances to reach the target number
for i, ratio in enumerate(ratios):
    target_df = df[df["bug"] == 1].copy()  # Copy the buggy instances
    # Calculate the number of duplicates
    num_duplicates = target_num_buggy[i] - num_buggy
    if num_duplicates > 0:
        # Duplicate the instances
        target_df = pd.concat([target_df] * num_duplicates)
        df = pd.concat([df, target_df])  # Add the duplicates to the dataset
        num_buggy = len(target_df)  # Update the count of buggy instances

# Shuffle the dataset
df = df.sample(frac=1)

# Save the balanced dataset to a new file
df.to_csv("balanced_dataset.csv", index=False)
