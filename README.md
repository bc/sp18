# sp18
EEG --> Signal Processor --> Tendon Controller --> Cadaver Finger Force --> VR Visual Feedback
Started project in Spring 2018 in Los Angeles.

# How to bind IP address
1. Within Control panel, Network> Internet, Network Connections
2. Pick the ethernet connecetion identified by realtec usb
3. Select the status window for it.
4. under properties, choose IPv4 properties.
5. set the IP address to whatever, subnet mask set to default, gateway to default

on the MSI side we set it to 

on linux

add to /etc/dhcpcd.conf
```bash
interface eth1
static ip_address=192.169.2.10/24
```

for remote ssh into rpi
```
brew cask install osxfuse
brew install sshfs
sshfs username@hostname:/remote/directory/path /local/mount/point -ovolname=NAME
```

on rpi, to keep ssh open
```

```

# Contributors
Lead
-@bc

EEG
-@marjanin

Biomimetic-Design
-@mayumiishikawa
-@brandonmiura

Tendon-Drive Networking
-@tstroobosscher

Scientific-Analytics
-@medvidov2786

TendonDrive
-@sofiahurtado
-@fmdunlap
-@nterrile

VR-Modeling
-@ArfanR
-@kujustin
-@ceubanks
