cat cow.txt | openssl base64 | curl --data @- http://0.0.0.0:5000/receive