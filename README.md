# serial to syslog bridge using a Raspberry PI pico

This is a proof of concept for using a raspberry pi pico to send serial console logs to a remote syslog server.

## adapting to your environment
The WIFI secrets are stored in the file `secrets.py`, adapt to your environment.
The syslog server's IP address is hard coded in `main.py?, also the port number 6666, so also adjust this to your environment.

## rsyslog example configuration

This is my rsyslog config (in `/etc/rsyslog.d/netconsole.conf`):
```
$ModLoad imudp.so         # provides UDP syslog reception
$RuleSet remote

$template ncRemoteLogIP,"/var/log/net/%fromhost-ip%.log"

if ($fromhost-ip startswith '192.168.') then {
        $RepeatedMsgReduction   off
        ?ncRemoteLogIP
        stop
}

$InputUDPServerBindRuleset remote
$UDPServerRun 6666

$RuleSet RSYSLOG_DefaultRuleset
```

## License
The content of this repository is licensed under the WTFPLv2. See `COPYING`.

