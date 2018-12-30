command(){
    tar --create --file - --verbose $ARCHIVE_NAME | gpg --recipient florent.pastor@gmail.com --encrypt --verbose -o $ARCHIVE_NAME.gpg &&
    rm -v $ARCHIVE_DIRECTORY/$ARCHIVE_NAME.gpg &&
    cp -v $ARCHIVE_NAME.gpg $ARCHIVE_DIRECTORY/$ARCHIVE_NAME.gpg
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

