#!/bin/bash
# remove folders modified 2 days ago
find /tmp/* -type d -ctime +2 -exec rm -rf {} \;
