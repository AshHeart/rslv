#!/bin/sh

#When in doubt, Run this file first


echo "Number of spam emails are: " 
ls -l ./enron1/ham/*.txt | wc -l
echo "number of non-spam emaisl are: " 
ls -l ./enron1/spam/*.txt | wc -l
