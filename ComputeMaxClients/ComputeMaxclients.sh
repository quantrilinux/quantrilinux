#!/bin/bash
# Script compute MaxClient for Apache
# Author: Arch
# Date: 06/12/2013

# Get total MEM
TOTAL_MEM=$(head -1 /proc/meminfo | awk '{print $2}')

# Get total Memory is being used
TOTAL_MEM_USED=$(free | grep 'buffers/cache' | awk '{print $3}')

# Get average memory of 1 process httpd
count=0
httpd_mem=0

for process_mem in `ps -ylC httpd --sort:rss | awk '{print $8}' | grep -v RSS`
do
	let "count+=1"
	let "httpd_mem+=$process_mem"
done

# Average memory per process
HTTPD_AVG_MEM=$(( $httpd_mem / $count ))

# Get total memory used for httpd:
HTTPD_TOTAL_MEM=$(( $TOTAL_MEM - $TOTAL_MEM_USED + $httpd_mem ))

MAX_CLIENT=$(( $HTTPD_TOTAL_MEM / $HTTPD_AVG_MEM ))

# Final result
echo -e "Total RAM in this server:\t\t $TOTAL_MEM KB"
echo -e "Total RAM is being used:\t\t $TOTAL_MEM_USED KB"
echo -e "Total RAM will be used for httpd:\t $HTTPD_TOTAL_MEM KB"
echo -e "Average RAM per process httpd:\t\t $HTTPD_AVG_MEM KB"
echo -e "Recommend MaxClients value:\t\t $MAX_CLIENT"
