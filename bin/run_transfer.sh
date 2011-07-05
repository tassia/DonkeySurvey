#!/bin/bash

NC="/bin/nc"

# Define host that will download files
# (hostname port user password)
UPLOADER=(192.168.0.111 4000 admin "12")

# Define host that will share files
# (hostname port user password)
SHARING=(localhost 4000 admin "12")

MLEXEC=/usr/bin/mlnet
MLDIR=/home/tassia/.mldonkey
SHARED=$MLDIR/shared
PIDFILE=$MLDIR/mlnet.pid
LOGFILE=$MLDIR/mlnet.log
START_STOP=/sbin/start-stop-daemon

# Initialize sharing host
# Args: Null
function initialize_sharing() {
#	# Restarting mldonkey
#	if [ -f $PID_FILE ]
#	then
#		echo "Stoping MLDonkey..."
#		$START_STOP --stop --oknodo --pidfile $PIDFILE --retry 30	
#	fi
#	echo "Starting MLDonkey..."
#	$START_STOP --start --pidfile $PIDFILE --background --exec $MLEXEC -- -log_file $LOGFILE -pid $MLDIR 
#
	# Creation and release of shared files
	echo "Creating shared files..."
	rm $SHARED/donkey* 2>&1
	for i in {1..3}
	do
        	DATE=$(date +%s)
        	dd if=/dev/zero of=$SHARED/donkey_$DATE count=5120 bs=1024 > /dev/null 2>&1
		echo $DATE >> $SHARED/donkey_$DATE
		sleep 1
	done
	query ${SHARING[@]} reshare 
	echo "Connecting to Ed2k Network..."
	sleep 30
	# get all links on shared host
	LINKS=$(query ${SHARING[@]} links | grep "ed2k:")
}

# Query for commands in mldonkey server
# Args: host port user pass command [args]
function query() {
	output=$(${NC} $1 $2 << EOF
	auth $3 $4
	${@:5}
	q
EOF)
	echo "$output" | egrep -v "elcome|Use|command-line:|^> $|^$"
}

# Get first connected server on sharing host
# Args: Null
function get_first_server() {
	VM=$(query ${SHARING[@]} vm)
	SERVER_IP=${VM%%:*}
	SERVER_IP=${SERVER_IP##* }
	SERVER_PORT=${VM#*:}
	SERVER_PORT=${SERVER_PORT%% *}
	echo $SERVER_IP $SERVER_PORT
}

# Remove all servers from the its list and connect to common-server
# Args: Null
function conect_to_common(){
	query $@ rem all
	query $@ n ${COMMON_SERVER}
	VMA=$(query $@ vma)
        ID=${VMA#*[Donkey }
	ID=${ID%%]*}
	query $@ " c $ID"
}

# Add links to download queue for uploader host
# Args: link1 link2 linkn
function download_links() {
	echo "Downloading ${#@} files..." 
	for link in $@; do
		echo $link
		query ${UPLOADER[@]} dllink $link
		VD=$(query ${UPLOADER[@]} vd)
		ID=${VD%%]*}
		ID=${ID##* }
                read KEY
                if [ "$KEY" == 'p' ]; then
                        query ${UPLOADER[@]} pause $ID
                        read KEY
                        query ${UPLOADER[@]} resume $ID
                        read KEY
                fi

	done
}

# Cancel all downloads for a host
# Args: host port user pass
function cancel_downloads() {
	query $@ cancel all
	query $@ confirm yes
}

# Initialize sharing host
initialize_sharing

# Get first connected server
COMMON_SERVER=$(get_first_server)
echo "Common server: $COMMON_SERVER"

# Connect both to common-server
conect_to_common ${SHARING[@]}
conect_to_common ${UPLOADER[@]}

# Cancel all downloads in progress at uploader host
cancel_downloads ${UPLOADER[@]}

# Start download links in uploader host in interactive mode
download_links $LINKS
