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
import sqlite3

import cx_Oracle
import pymysql as mysql

from core import LOG
from core.constant.response_enum import ResponseEnum
from core.exception.custom_errors import HandleError


def sql_connect(db_source):
    """
        Sql Connect

        :param str db_source: Databases source
        :return: Sql connect
        :rtype: object
    """
    try:
        if db_source and db_source["db_type"] == "mysql":
            # pymysql 游标模式字典类型[cursorclass=mysql.cursors.DictCursor]
            connect = mysql.connect(host=db_source["host"], port=db_source["port"], user=db_source["user"],
                                    password=db_source["password"], db=db_source["database"],
                                    charset=db_source["charset"])
        elif db_source and db_source["db_type"] == "oracle":
            connect = cx_Oracle.connect(db_source["user"], db_source["password"], db_source["host"] + "/"
                                        + db_source["database"])
        elif db_source and db_source["db_type"] == "sqlite":
            connect = sqlite3.connect(db_source["database"])
        else:
            LOG.error("[{}] 数据库-连接失败：配置有误".format(db_source["database"]))
            raise HandleError(ResponseEnum.TYPE_ERROR.value, "数据库-配置有误[{}]".format(
                ResponseEnum.TYPE_ERROR.value["msg"]))
        LOG.info("[{}] 数据库连接成功 ...".format(db_source["database"]))
        return connect
    except HandleError as e:
        # Databases type error
        raise e
    except Exception as e:
        LOG.error("[{}] 数据库-连接失败：{}".format(db_source["database"], e))
        raise HandleError(ResponseEnum.FAILURE.value, e)


def sql_execute(sql, handle=None, connect=None, args=None):
    # type: (str, str, object, object) -> object
    """
        Mysql Execute

        :param str sql: Execute sql statement.
        :param handle: It's insert, delete, update or select.
        :type handle: str or None
        :param object connect: Databases Connect
        :param object args: Sequence of sequences or mappings.  It is used as parameter.
        :return: Execute result
        :rtype: object
    """
    try:
        if connect is None:
            return None
        cur = connect.cursor()
        LOG.info("Execute sql: {}".format(sql))
        if "select" == handle:
            cur.execute(sql)
            # result = cur.fetchall()
            # 拼装成字典
            result = rows_to_dict_list(cur)
            return result
        else:
            if args:
                if "onlyOne" == handle:
                    result = cur.execute(sql, args)
                else:
                    result = cur.executemany(sql, args)
            else:
                result = cur.execute(sql)
            connect.commit()
            # 关闭游标
            cur.close()
            LOG.info("Execute success: {}".format(result))
            return result
    except Exception as e:
        LOG.error("操作失败{}：{}".format(e.__class__, e))
        if "select" != handle:
            connect.rollback()
        raise HandleError(ResponseEnum.FAILURE.value, "数据库-操作失败", e.__class__, e)


def sql_close(db_type, connect):
    """
        Sql Close

        :param db_type: Databases type
        :param object connect: Mysql connect to close.
    """
    if connect:
        connect.close()
        LOG.info("{} [数据库连接关闭] {} connect to close.".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                            db_type))


def rows_to_dict_list(cursor):
    """
        记录转换成Dict

        :param cursor: cursor
        :return: Dict
    """
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor]
