import json
import boto3
import pandas as pd
from io import BytesIO
import re
from datetime import datetime
import database, db_columns

##
def connect_s3():
    conn = boto3.client(
    's3',
    region_name='us-east-1')
    if conn:
        return conn
    else:
        return False

def lambda_handler(event, context):
    filename = event['object_key']
    s3bucket = event['bucket_name']
    #connect to s3
    conn = connect_s3()
    if not conn:
        return {"statusCode": 500,"body": json.dumps({"error": "cant connect to s3 server",}),}
    #get the file object in bucket
    obj = conn.get_object(Bucket=s3bucket, Key=filename)['Body']
    #try to pandas read_csv in iso-8859-1 decode format 
    try:
        df=pd.read_csv(BytesIO(obj.read().decode('iso-8859-1').encode("utf-8")),sep=';',index_col=False)
    except:
        #if cant decode, early returns with error
        return {"statusCode": 500,"body": json.dumps({"error": "file format cant be decoded. Try an iso-8859-1 file",}),}
    #add ID_CESSAO empty column
    df.insert(loc=0, column='ID_CESSAO', value=None)
    #rename csv column names to db names
    df.rename(columns={
    'Originador':'ORIGINADOR',
    'Doc Originador':'DOC_ORIGINADOR',
    'Cedente':'CEDENTE',
    'Doc Cedente':'DOC_CEDENTE',
    'Id':'ID_EXTERNO',
    'Cliente':'CLIENTE',
    'CPF/CNPJ':'CPF_CNPJ',
    'Endereço':'ENDERECO',
    'Cidade':'CIDADE',
    'Valor do Empréstimo':'VALOR_DO_EMPRESTIMO',
    'Parcela R$':'VALOR_PARCELA',
    'Total Parcelas':'TOTAL_PARCELAS',
    'Parcela':'PARCELA',
    'Data de Emissão':'DATA_DE_EMISSAO',
    'Data de Vencimento':'DATA_DE_VENCIMENTO',
    'Preço de Aquisição':'PRECO_DE_AQUISICAO'
    }, inplace=True)
    #remove cpf-cnpj format
    df['CPF_CNPJ'] = df['CPF_CNPJ'].apply(lambda x: x.replace('.','').replace('/','').replace('-',''))
    df['DOC_ORIGINADOR'] = df['DOC_ORIGINADOR'].apply(lambda x: x.replace('.','').replace('/','').replace('-',''))
    #convert date to specified format yyyy-mm-dd
    df['DATA_DE_EMISSAO'] = df['DATA_DE_EMISSAO'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y').date())
    df['DATA_DE_VENCIMENTO'] = df['DATA_DE_VENCIMENTO'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y').date())
    #drop unecessary columns
    for column in df.head():
        if not column in db_columns.column_names:
            df.drop(column, inplace=True, axis=1)
    #send dataframe to send_to_database function
    if not database.send_to_database(df):
        #if not sended, early returns error
        return {"statusCode": 500,"body": json.dumps({"error": "failed to save csv in database",}),}
    #if all done, returns 200
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "csv {} from bucket {} inserted in db".format(filename,s3bucket),
        }),
    }
