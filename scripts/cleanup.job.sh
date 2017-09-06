#!/bin/bash
# remove folders modified 4 days ago
find /tmp/* -type d -ctime +4 -exec rm -rf {} \;
