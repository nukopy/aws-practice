import fastavro


path = "./success-pets-2-2020-11-05-08-44-22-32b8395a-44a6-408e-9133-521f4c8772ea.avro"
with open(path, "rb") as f:
    dic = fastavro.reader(f)
