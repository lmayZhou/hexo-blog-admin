#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's JDBC Util
# -- MySQL/Oracle
# ****************************
# Author: lmay.Zhou
# Blog: www.lmaye.com
# Date: 2018年2月1日 11:40:49
# ----------------------------------------------------------
import datetime
import cx_Oracle
import pymysql as mysql
from core import LOG


def sql_connect(db_source, signal_out=None):
    """
            Sql Connect

        :param str db_source: Databases source
        :param signal_out: signal_out
        :return: Sql connect
        :rtype: object
    """
    try:
        if db_source and db_source["db_type"] == "mysql":
            connect = mysql.connect(host=db_source["host"], user=db_source["user"], password=db_source["password"],
                                    db=db_source["database"], charset=db_source["charset"])
        elif db_source and db_source["db_type"] == "oracle":
            connect = cx_Oracle.connect(db_source["user"], db_source["password"],
                                        db_source["host"] + "/" + db_source["database"])
        else:
            signal_out.emit("{} 数据库配置有误, 请检查配置！".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            return None
        if signal_out:
            signal_out.emit("{} [{}] 数据库连接成功 ...".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                         db_source["database"]))
        LOG.info("[{}] 数据库连接成功 ...".format(db_source["database"]))
        return connect
    except Exception as e:
        LOG.error("[{}] 数据库连接失败：{}".format(db_source["database"], e))
        if signal_out:
            signal_out.emit("{} [{}] 数据库连接失败：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                       db_source["database"], e))
        return None


def sql_execute(sql, handle=None, connect=None, args=None, signal_out=None):
    # type: (str, str, object, list, object) -> object
    """
        Mysql Execute

        :param str sql: Execute sql statement.
        :param handle: It's insert, delete, update or select.
        :type handle: str or None
        :param object connect: Databases Connect
        :param list args: Sequence of sequences or mappings.  It is used as parameter.
        :param signal_out: signal_out
        :return: Execute result
        :rtype: object
    """
    try:
        if connect is None:
            return None
        if signal_out:
            signal_out.emit("{} 执行SQL: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sql))
        cursor = connect.cursor()
        LOG.info("Execute sql: {}".format(sql))
        if "select" == handle:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        else:
            if not args:
                return 0
            result = cursor.executemany(sql, args)
            connect.commit()
            return result
    except Exception as e:
        LOG.error("操作失败：{}".format(e))
        if signal_out:
            signal_out.emit("{} 操作失败：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e))
        connect.rollback()


def sql_close(db_type, connect, signal_out=None):
    """
        Sql Close

        :param db_type: Databases type
        :param object connect: Mysql connect to close.
        :param object signal_out: signal_out
    """
    if connect:
        connect.close()
        LOG.info("{} [数据库连接关闭] {} connect to close.".format(datetime.datetime.now()
                                                               .strftime('%Y-%m-%d %H:%M:%S'), db_type))
        if signal_out:
            signal_out.emit("{} [数据库连接关闭] {} connect to close.".format(datetime.datetime.now()
                                                                      .strftime('%Y-%m-%d %H:%M:%S'), db_type))
