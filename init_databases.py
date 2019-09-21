#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# --
# --
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/4/21 0:37 星期六
# ----------------------------------------------------------
from datetime import datetime
from core.models.user import User
from core.app import db
from core.models.role import Role
from core.utils.security import Security

if __name__ == '__main__':
    now = datetime.utcnow() + datetime.timedelta(hours=8)
    role = Role(role_code="R0000", role_name="管理员", last_date=now)
    db.session.add(role)
    db.session.commit()

    sc = Security("lmayZhou")
    user = User(nickname="lmay", password=sc.encrypt("root@123").replace("\n", ""), email="lmay@lmaye.com",
                qq="379839355", last_date=now)
    db.session.add(user)
    db.session.commit()
