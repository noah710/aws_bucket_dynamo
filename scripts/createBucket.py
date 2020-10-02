import boto3
import os
import csv

# create bucket
try:
    os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
    s3 = boto3.resource('s3')
    s3.create_bucket(
        Bucket='isthisvalid234523',
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )
except:
    print("Bucket already exists!")

# upload data to bucket
bucket = s3.Bucket('isthisvalid234523')
bucket.Acl().put(ACL='public-read')
for root, dirs, files in os.walk("/data"):
    for filename in files:
        name = filename.split('.')[0]
        body = open('/data/' + filename, 'rb')
        o = s3.Object('isthisvalid234523', name).put(Body=body )
        s3.Object('isthisvalid234523', name).Acl().put(ACL='public-read')
    entries = len(files)
# create dyndb
try:
    dyndb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dyndb.create_table(
        TableName='DataTable',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
                'ReadCapacityUnits': entries,
                'WriteCapacityUnits': entries
            }
    )
except:
    print("Dyndb already exists!")
    table = dyndb.Table("DataTable")

table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')
print(table.item_count)

# open csv and add entries to dynamo
with open('/data.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    for item in csvf:
        print(item)
        body = open('/data/'+item[3]+'.jpg', 'rb')
        s3.Object('isthisvalid234523', item[3]).put(Body=body )
        md = s3.Object('isthisvalid234523', item[3]).Acl().put(ACL='public-read')
        url = "https://s3-us-west-2.amazonaws.com/isthisvalid234523/"+item[3]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],'description' : item[4], 'date' : item[2], 'url':url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print("item may already be there or another failure")
response = table.get_item(Key={'PartitionKey': '4','RowKey': '4'})

item = response['Item']

print(item)