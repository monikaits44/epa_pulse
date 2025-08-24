#!/bin/bash
set -e


TO_BE_SINGNED_PREFIX="to be signed - *"

find . -type f -name "$TO_BE_SINGNED_PREFIX" -print0 | while read -d $'\0' INPUT_FILE; do
  OUTPUT_FILE=$(echo "$INPUT_FILE" | sed "s/$TO_BE_SINGNED_PREFIX//")   # remove prefix
  OUTPUT_FILE=${OUTPUT_FILE%.xml}.p7b   # use .p7b
  echo "--> $INPUT_FILE -> $OUTPUT_FILE"

  # macOS openssl does not support `cms`
  OPENSSL_PATH=$(brew --prefix)/opt/openssl@1.1/bin/openssl

  $OPENSSL_PATH cms -sign \
    -signer 80276883119861414289-C.CH.AUT.pem \
    -inkey 80276883119861414289-C.CH.AUT.key \
    -nodetach \
    -outform der \
    -in "$INPUT_FILE" \
    > $OUTPUT_FILE

  rm "$INPUT_FILE"
done
