#!/usr/bin/env python3
#
# Copyright 2019 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import json
import logging
import mimetypes
import os
import stat
import sys

from ansible.module_utils.basic import AnsibleModule


mimetypes.init()


def path_in_tree(root, path):
    full_path = os.path.realpath(os.path.abspath(
        os.path.expanduser(path)))
    if not full_path.startswith(root):
        logging.debug("Skipping path outside root: %s" % (path,))
        return False
    return True


def walk(root, original_root=None):
    if original_root is None:
        original_root = root
    logging.debug("Walk: %s", root)
    data = []
    dirs = []
    files = []
    for e in os.listdir(root):
        if os.path.isdir(os.path.join(root, e)):
            if not os.path.islink(os.path.join(root, e)):
                dirs.append(e)
        else:
            files.append(e)
    for d in sorted(dirs):
        logging.debug("Directory: %s", d)
        path = os.path.join(root, d)
        if not path_in_tree(original_root, path):
            continue
        data.append(dict(name=d,
                         mimetype='application/directory',
                         encoding=None,
                         children=walk(os.path.join(root, d), original_root)))
    for f in sorted(files):
        logging.debug("File: %s", f)
        path = os.path.join(root, f)
        if not path_in_tree(original_root, path):
            continue
        mime_guess, encoding = mimetypes.guess_type(path)
        if not mime_guess:
            mime_guess = 'text/plain'
        st = os.stat(path)
        last_modified = st[stat.ST_MTIME]
        size = st[stat.ST_SIZE]
        data.append(dict(name=f,
                         mimetype=mime_guess,
                         encoding=encoding,
                         last_modified=last_modified,
                         size=size))
    return data


def run(root_path, output):
    data = walk(root_path, root_path)
    with open(output, 'w') as f:
        f.write(json.dumps({'tree': data}))


def ansible_main():
    module = AnsibleModule(
        argument_spec=dict(
            root=dict(type='path'),
            output=dict(type='path'),
        )
    )

    p = module.params
    run(p.get('root'), p.get('output'))

    module.exit_json(changed=True)


def cli_main():
    parser = argparse.ArgumentParser(
        description="Generate a Zuul file manifest"
    )
    parser.add_argument('--verbose', action='store_true',
                        help='show debug information')
    parser.add_argument('root',
                        help='Root of upload directory')
    parser.add_argument('output',
                        help='Output file path')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    run(args.root, args.output)


if __name__ == '__main__':
    if sys.stdin.isatty():
        cli_main()
    else:
        ansible_main()
