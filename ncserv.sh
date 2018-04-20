 while true; do { echo "HTTP/1.1 404 Not Found\r\nContent-Length: 4\r\nConnection: Closed\r\n\r\n1234"; bash -c test;} | nc -l 8023; done 
