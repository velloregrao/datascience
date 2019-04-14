import pandas as pd

word = 'data'
it = iter(word)
print(*it)

avengers = ['hawkeye', 'Captain America', 'Ironman', 'Black Widow', 'Black Panther']

releases = ['avengers', 'avengers - age of ultraon', 'avengers - infinity war', 'avengers - end game']

marvel = iter(avengers)

marvelmovies = zip(avengers, releases)

print(next(marvel))
print(next(marvel))
print(next(marvel))
print(next(marvel))
print(next(marvel))

marvel = list(enumerate(avengers))

print(marvel)

for item in marvel:
    print(item)

print(*marvelmovies)

states = {}

for chunk in pd.read_csv('states.csv', chunksize=5):
    print(chunk)
