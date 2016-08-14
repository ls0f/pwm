#!/bin/bash

set -e;

# check pwm exists;
pwm;

# save;

pwm -d github.com -a lovedboy -w;

# search;

pwm -s github | grep github.com;
pwm -s github | grep LNXStZoEGuHi9rb;
pwm -s github | grep "1 records";

# delete;

pwm -r 1 | grep '1 record(s) removed';
pwm -s github | grep "0 records";
