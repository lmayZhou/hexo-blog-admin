#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Post
# -- 
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/5/20 下午12:44 星期日
# ----------------------------------------------------------
import six


def u(text, encoding='utf-8'):
    """Return unicode text, no matter what"""

    if isinstance(text, six.binary_type):
        return text.decode(encoding)
    # it's already unicode
    return text


class Post(object):
    """
    A post contains content and metadata from YAML Front Matter.
    For convenience, metadata values are available as proxied item lookups.

    Don't use this class directly. Use module-level functions load, dump, etc.
    """

    def __init__(self, content, **metadata):
        self.content = u(content)
        self.metadata = metadata

    def __getitem__(self, name):
        """Get metadata key"""
        return self.metadata[name]

    def __setitem__(self, name, value):
        """Set a metadata key"""
        self.metadata[name] = value

    def __delitem__(self, name):
        """Delete a metadata key"""
        del self.metadata[name]

    def __bytes__(self):
        return self.content.encode('utf-8')

    def __str__(self):
        if six.PY2:
            return self.__bytes__()
        return self.content

    def __unicode__(self):
        return self.content

    def get(self, key, default=None):
        """Get a key, fallback to default"""
        return self.metadata.get(key, default)

    def keys(self):
        """Return metadata keys"""
        return self.metadata.keys()

    def values(self):
        """Return metadata values"""
        return self.metadata.values()

    def to_dict(self):
        """Post as a dict, for serializing"""
        d = self.metadata.copy()
        d['content'] = self.content
        return d
