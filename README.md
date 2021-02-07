# Indicator Applet for Easy `gocryptfs` Mount

## Dependencies
  - [gocryptfs](https://github.com/rfjakob/gocryptfs) and the following Ubuntu packages must be installed.
  - `sudo apt-get install -y gir1.2-appindicator python3-gi gocryptfs ssh-askpass`

## Prepare list of mount points
The mount points you want must be listed in `gocryptfs-mount-applet.py`,
in the python variable `known_mounts`. A future version of this app might allow
specifying this in a config file.

## Run
  - Run `python3 gocryptfs-mount-applet.py`. You should see the an icon in your
  indicator applet (system tray).
  - Use [startup applications](https://help.ubuntu.com/stable/ubuntu-help/startup-applications.html.en) to add this applet to your computer startup.

This applet only supports easy mounting of pre-registered cipher directories with paired mount points. For any more elaborate functionality, you can use [SiriKali](https://mhogomchungu.github.io/sirikali/), or just `gocryptfs` on the command line.
