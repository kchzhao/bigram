import random
import matplotlib.pyplot as plt
from collections import defaultdict


def read_data(filename):
  """
    Read data from a file and return it as a list of names.
    """
  with open(filename, 'r') as file:
    data = file.read().split()
  return data


def build_bigram_model(names):
  """
    Build a bigram language model from the input names.
    Returns a nested dictionary with probabilities.
    """
  model = defaultdict(dict)

  for name in names:
    name = name.lower()  # Convert names to lowercase
    name = "<START> " + name + " <END>"  # Add start and end tokens

    for i in range(len(name) - 1):
      current_char = name[i]
      next_char = name[i + 1]

      if next_char not in model[current_char]:
        model[current_char][next_char] = 1
      else:
        model[current_char][next_char] += 1

  # Convert frequencies to probabilities
  for char in model:
    total_count = sum(model[char].values())
    for next_char in model[char]:
      model[char][next_char] /= total_count

  return model


def generate_name(model):
  """
    Generate a random name using the given bigram language model.
    """
  name = ""
  current_char = "<START>"

  while True:
    if current_char not in model:
      break

    next_char = random.choice(list(model[current_char].keys()))
    probabilities = list(model[current_char].values())
    next_char = random.choices(next_char, probabilities)[0]

    if next_char == "<END>":
      break

    name += next_char
    current_char = next_char

  return name.strip()  # Strip leading and trailing spaces


def plot_bigram_probabilities(model):
  """
    Plot a bar chart of the probabilities of the bigrams.
    """
  chars = []
  probabilities = []

  for char in model:
    for next_char in model[char]:
      chars.append(char + next_char)
      probabilities.append(model[char][next_char])

  plt.figure(figsize=(10, 6))
  plt.bar(chars, probabilities)
  plt.title("Bigram Probabilities")
  plt.xlabel("Bigram")
  plt.ylabel("Probability")
  plt.xticks(rotation=90)
  plt.show()


# Main code
filename = "names.txt"
names = read_data(filename)
model = build_bigram_model(names)

print("Name Generator - Bigram Language Model")
print("--------------------------------------")

while True:
  user_input = input(
    "Press Enter to generate a new name, 'P' to plot bigram probabilities, or 'Q' to quit: "
  )

  if user_input.lower() == "q":
    break
  elif user_input.lower() == "p":
    plot_bigram_probabilities(model)
  else:
    name = generate_name(model)
    print("Generated Name:", name)
    print()
