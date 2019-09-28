
import boto3
import pandas as pd

client = boto3.client('s3') #low-level functional API
resource = boto3.resource('s3') #high-level object-oriented API
my_bucket = resource.Bucket('healthsignals') #subsitute this for your s3 bucket name.

files = list(my_bucket.objects.filter(Prefix='data/Access Point Availability/'))

for file in files:
    print(file)
    obj = file.get()
    key = obj['ContentLength']
    print(key)
    if key != 0:
        df = pd.read_csv(obj['Body'])
        print(df.head(2))
