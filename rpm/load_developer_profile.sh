#!/bin/sh
# Don't load arbitary file from shell-profile directory only when developer profile is enabled.
# We check for devel-su because that is only installed when developer-mode is installed.
if [ -e /usr/bin/devel-su ] || [ -e /etc/sailfishos-emulator ]; then
    . /etc/profile.d/developer-profile.sh
fi
