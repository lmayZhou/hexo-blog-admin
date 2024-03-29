#! /bin/sh
# chkconfig: 2345 55 25
# Description: Startup script for uwsgi webserver on Debian. Place in /etc/init.d and
# run 'update-rc.d -f uwsgi defaults', or use the appropriate command on your
# distro. For CentOS/Redhat run: 'chkconfig --add uwsgi'

### BEGIN INIT INFO
# Provides:          uwsgi
# Required-Start:    $all
# Required-Stop:      $all
# Default-Start:      2 3 4 5
# Default-Stop:     0 1 6
# Short-Description: starts the uwsgi web server
# Description:       starts uwsgi using start-stop-daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="hexo-blog-admin"
NAME=uwsgi
DAEMON=/usr/local/bin/uwsgi
# 项目 uwsgi配置
CONFIGFILE=/home/services/hexo-blog-admin/hexo-blog-admin.ini
PIDFILE=/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

set -e
[ -x "$DAEMON" ] || exit 0

do_start() {
     $DAEMON $CONFIGFILE || echo -n "uwsgi already running"
}

do_stop() {
     killall -9 $NAME || echo -n "uwsgi not running"
     rm -f $PIDFILE
     echo "$DAEMON STOPED."
}

do_reload() {
     $DAEMON --reload $PIDFILE || echo -n "uwsgi can't reload"
}

do_status() {
     ps aux|grep $DAEMON
}

case "$1" in
 status)
     echo -en "Status $NAME: \n"
     do_status
 ;;
 start)
     echo -en "Starting $NAME: \n"
     do_start
 ;;
 stop)
     echo -en "Stopping $NAME: \n"
     do_stop
 ;;
 reload|graceful)
     echo -en "Reloading $NAME: \n"
     do_reload
 ;;
 *)
     echo "Usage: $SCRIPTNAME {status|start|stop|reload}" >&2
     exit 3
 ;;
esac
