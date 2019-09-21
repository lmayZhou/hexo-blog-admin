#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# -- This's The Python Frontmatter
# -- Python Frontmatter: Parse and manage posts with YAML frontmatter
# ****************************
# Author: lmay.Zhou
# Email: lmay@lmaye.com
# Blog: www.lmaye.com
# Date: 2018/5/20 下午12:57 星期日
# ----------------------------------------------------------
import codecs
import re
import yaml
from core.models.post import Post, u
try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper

__all__ = ['parse', 'load', 'loads', 'dump', 'dumps']
# match three or more dashes
# split on this
FM_BOUNDARY = re.compile(r'^-{3}$', re.MULTILINE)

POST_TEMPLATE = """
---
{metadata}
---

{content}
"""


def parse(text, **defaults):
    """
    Parse text with YAML frontmatter, return metadata and content.
    Pass in optional metadata defaults as keyword args.

    If frontmatter is not found, returns an empty metadata dictionary
    and original text content.
    """
    # ensure unicode first
    text = u(text)
    # 解决解析识别问题
    text = text[text.index("\n") + 1:].replace("\r", "")

    # metadata starts with defaults
    metadata = defaults.copy()

    # split on the first two triple-dashes
    try:
        fm, content = FM_BOUNDARY.split(text, 2)
    except ValueError:
        # if we can't split, bail
        return metadata, text

    # parse yaml, now that we have frontmatter
    fm = yaml.safe_load(fm)
    if isinstance(fm, dict):
        metadata.update(fm)

    return metadata, content.strip()


def load(fd, **defaults):
    """
    Load and parse a file or filename, return a post.
    """
    if hasattr(fd, 'read'):
        text = fd.read()

    else:
        with codecs.open(fd, 'r', 'utf-8') as f:
            text = f.read()

    return loads(text, **defaults)


def loads(text, **defaults):
    """
    Parse text and return a post.
    """
    metadata, content = parse(text, **defaults)
    return Post(content, **metadata)


def dump(post, fd, **kwargs):
    """
    Serialize post to a string and dump to a file-like object.
    """
    content = dumps(post, **kwargs)
    if hasattr(fd, 'write'):
        fd.write(content)

    else:
        with codecs.open(fd, 'w', 'utf-8') as f:
            f.write(content)


def dumps(post, **kwargs):
    """
    Serialize post to a string and return text.
    """
    kwargs.setdefault('Dumper', SafeDumper)
    kwargs.setdefault('default_flow_style', False)

    metadata = yaml.dump(post.metadata, **kwargs).strip()
    metadata = u(metadata) # ensure unicode
    return POST_TEMPLATE.format(metadata=metadata, content=post.content).strip()
