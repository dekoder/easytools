 while true; do { echo -e "HTTP/1.1 200 OK\r\n\r\n`date`"; bash -c test;} | nc -l 8000; done 
