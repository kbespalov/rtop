#!/bin/bash

### BEGIN INIT INFO
# Provides:          rtop
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: remote top
# Description:       none
### END INIT INFO

PYDAEMON=/usr/bin/python
DAEMON_USER=root
DAEMON_NAME=rtop
APP_DIR=/opt/rtop
APP="$APP_DIR/app.py"

PIDFILE=/var/run/$DAEMON_NAME.pid 

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --name $DAEMON_NAME --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --exec $PYDAEMON $APP  
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;
esac
exit 0