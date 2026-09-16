#!/bin/bash

# this makes the scripts exit immediately if any command exits with a non-zero status meaning that the scripts encounter an error. If we dont set this, the scripts will continue executing even after an error occurs
set -o errexit

# this treat unset variables as errors and exits the script immediately.This is going to help us to catch any bugs related to undefines variables
set -o nounset

# This ensures that the script exits with a non-zero status. If any command in a pipeline fails by default, our pipelines exit status is that of the last command in the pipeline
set -o pipefail

#
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
