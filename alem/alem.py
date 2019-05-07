#!/usr/bin/env python
# encoding: utf-8

import os
import alembic
import argparse
import subprocess as subp

from os.path import (
    isfile,
    join as path_join,
    exists as path_exists
)


_cwd = os.getcwd()


class Alem(object):

    def __init__(self, upgrade, downgrade, alembic_args):
        self.upgrade = upgrade
        self.downgrade = downgrade
        self.args = alembic_args

        self.versions_path = path_join(read_alembic_dir(), "versions")

        if "--raiseerr" not in self.args:
            self.args = ["--raiseerr"] + self.args

    @property
    def is_revision(self):
        return "revision" in self.args

    def run(self):
        if self.is_revision:
            self.do_revision()
        else:
            self.do_default_alembic()

    def _read_scripts_name(self):
        files = os.listdir(self.versions_path)
        return {f for f in files if f.endswith(".py")}

    @staticmethod
    def _read_sql_file(fpath):
        sql_lines = []

        if not fpath:
            return sql_lines

        if not path_exists(fpath):
            return [s.strip() for s in fpath.split(";") if s.strip()]

        with open(fpath) as f:
            rows = []
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue

                if line.endswith(";"):
                    rows.append(line.rstrip(";"))
                    sql_lines.append(" ".join(rows))
                    rows = []
                else:
                    rows.append(line)

        return sql_lines

    @property
    def _to_do_revision(self):
        return bool(self.upgrade or self.downgrade)

    @staticmethod
    def _gen_sql_line(sql):
        return '    conn.execute(u"""{}""")\n'.format(sql)

    @staticmethod
    def _add_coding_line(fpath):
        with open(fpath) as f:
            lines = f.readlines()

        if not (lines[0].startswith("# encoding") or
                lines[1].startswith("# encoding") or
                lines[0].startswith("# -*- coding") or
                lines[1].startswith("# -*- coding")):
            line = "# -*- coding: utf-8 -*-\n"
            if lines[0].startswith("#!"):
                lines = [lines[0], line] + lines[1:]
            else:
                lines = [line] + lines

        with open(fpath, "w") as f:
            f.writelines(lines)

    def do_revision(self):
        if not self._to_do_revision:
            self.do_default_alembic()
            return

        scripts_old = self._read_scripts_name()

        self.do_default_alembic()

        scripts_new = self._read_scripts_name()
        scripts = scripts_new - scripts_old
        if not scripts:
            return

        script = scripts.pop()
        script = path_join(self.versions_path, script)

        self._add_coding_line(script)

        def do_grade(grade, sql_lines):
            if not sql_lines:
                return

            for idx, sql in enumerate(sql_lines):
                sql_lines[idx] = self._gen_sql_line(sql)

            with open(script) as f:
                lines = f.readlines()

            prefix = "def " + grade
            for idx, line in enumerate(lines):
                if not line.startswith(prefix):
                    continue

                idx += 1
                lines[idx] = "    conn = op.get_bind()\n"  # replace the row "pass"
                lines = lines[:idx+1] + sql_lines + lines[idx+1:]
                break

            with open(script, "w") as f:
                f.writelines(lines)

        do_grade("upgrade", self._read_sql_file(self.upgrade))
        do_grade("downgrade", self._read_sql_file(self.downgrade))

    def do_default_alembic(self):
        with subp.Popen(["alembic"]+self.args, stdout=subp.PIPE) as proc:
            print(proc.stdout.read().decode("utf8"))


def is_alembic_dir():
    return path_exists(path_join(_cwd, "alembic.ini"))


def read_alembic_dir():
    with open(path_join(_cwd, "alembic.ini")) as f:
        for line in f.readlines():
            if line.startswith("script_location"):
                return line.split("=")[1].strip()


def main():
    if not is_alembic_dir():
        print("current path '{}' is not an alembic project".format(_cwd))
        return

    parser = argparse.ArgumentParser()
    parser.add_argument("--upgrade", "-U")
    parser.add_argument("--downgrade", "-D")

    args, remain = parser.parse_known_args()
    Alem(args.upgrade, args.downgrade, remain).run()


if __name__ == '__main__':
    main()
