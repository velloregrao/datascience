import pandas as pd


avengers = ['hawkeye', 'Captain America', 'Ironman', 'Black Widow', 'Black Panther']

releases = ['avengers', 'avengers - age of ultraon', 'avengers - infinity war', 'avengers - end game']


lengths = (len(member) for member in avengers)

print(list(lengths))
