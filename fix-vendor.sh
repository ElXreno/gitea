#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 version"
    echo "Example: $0 1.12.1"
    exit 1
fi

REPO_URL="https://github.com/go-gitea/gitea"
REPO_NAME="`basename $REPO_URL`"
VERSION="$1"
TAG="v$VERSION"

SOURCE="$REPO_URL/releases/download/$TAG/gitea-src-$VERSION.tar.gz"
SOURCE_FILE="`basename $SOURCE`"
NAME="$REPO_NAME-src-$VERSION"

rm -rf $NAME
mkdir $NAME

pushd $NAME
wget $SOURCE -O $SOURCE_FILE
tar xvf $SOURCE_FILE
rm $SOURCE_FILE
GO111MODULE=on go mod vendor
rm -f ../$NAME.tar.gz
tar --exclude ./.git -cf - . | pigz -9 - > ../$NAME.tar.gz
popd

rm -rf $NAME
