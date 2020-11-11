# install Python dependencies
# TODO: requirements.txt から取ってこれると良いかも
pip install --target ./package python-snappy fastavro

# zip Python package
cd package
zip -r9 ../function.zip .

# function
cd ..
zip -g ./function.zip ./lambda_function.py
zip -g ./function.zip ./record.avsc