import pandas as pd

avengers = ['hawkeye', 'Captain America', 'Ironman', 'Black Widow', 'Black Panther']

releases = ['avengers', 'avengers - age of ultraon', 'avengers - infinity war', 'avengers - end game']

matrix = [[col for col in releases] for row in avengers]

for row in matrix:
    print(row)