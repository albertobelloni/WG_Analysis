#!/bin/sh

if [ $# -lt 1 ]
then
	echo >&2 "use: condor_log_upload logfile ..."
	echo >&2 ""
	echo >&2 "This script uploads one or more Condor userlog files"
	echo >&2 "representing a single workload to the Condor Log Analyzer"
	echo >&2 "and prints out the url you can visit to see the results."
	exit 1
fi

for logfile in $*;
do
	if [ ! -f $logfile ]
	then
		echo >&2 "condor_log_upload: $logfile does not exist"
		exit 1
	fi
done

checksum=$(cat $* | md5sum | awk '{print $1}')
url=http://condorlog.cse.nd.edu/logs/${checksum:0:2}/${checksum:2:2}/$checksum

cat $* | curl http://condorlog.cse.nd.edu/upload.php --form privacy=public --form logfile=@- -s >/dev/null

echo $url
