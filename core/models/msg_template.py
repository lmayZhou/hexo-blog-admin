# !/usr/bin/env python3
# -*- coding:utf-8 -*-

from core.app import db


class MsgTemplate(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    content = db.Column(db.String(255), nullable=False)
    version = db.Column(db.Integer, default=1)
    ext = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__,
                                ", ".join("{}:{}".format(key, getattr(self, key)) for key in self.__dict__.keys()))
