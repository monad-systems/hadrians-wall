#!/bin/bash
aws s3 sync hadrian-www/static/logs s3://hadrian-log --region us-east-2
