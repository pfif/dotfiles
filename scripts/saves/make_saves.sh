save(){
    rsync -aPv --delete $RSYNC_DRY_RUN $SOURCE_DIRECTORY  ~/saves/$SAVE_NAME/
    b2 sync $B2_DRY_RUN --delete --threads 1 ~/saves/$SAVE_NAME/ b2://mistertree-saves/$SAVE_NAME/
}

usage(){
    echo "usage: $0 source_directory save_name [--no-dry-run]"
}

if [ $# == 2 ] || [ $# == 3 ]
then
    if [ "$3" != "--no-dry-run" ]
    then
        RSYNC_DRY_RUN="-n"
        B2_DRY_RUN="--dryRun"
    fi
    SOURCE_DIRECTORY=$1
    SAVE_NAME=$2
    save
else
    usage
fi

