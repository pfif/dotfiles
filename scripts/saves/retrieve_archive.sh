command(){
    gpg -d $ARCHIVE_DIRECTORY/$ARCHIVE_NAME.gpg | tar --extract --file - -v
}

usage(){
    echo "usage: $0 archive_name archive_directory"
}

if [ $# == 2 ]
then
    ARCHIVE_NAME=$1
    ARCHIVE_DIRECTORY=$2
    command
else
    usage
fi
