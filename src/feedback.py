import os
import csv

def save_feedback(text, label):
    file_exists = os.path.isfile("data.csv")

    with open("data.csv", "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["text", "label"])

        writer.writerow([text, label])