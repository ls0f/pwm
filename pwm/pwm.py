# coding:utf-8

from hashlib import sha1
from base64 import b64encode
import sys
import hmac
import re
import sqlite3
import os
import getpass
from optparse import OptionParser
import sys
is_py2 = sys.version_info[0] == 2


__author = 'ls0f'
__version = '0.3'
__package = 'pwm'


class PWM(object):

    def __init__(self, key, db_path=None):
        self.key = key
        self.passwd_length = 15
        self.db_path = db_path
        self.table = 'pwm'

    def gen_passwd(self, raw):

        if sys.version_info > (3, 0):
            h = hmac.new(self.key.encode(), raw.encode(), sha1)
            base64 = b64encode(h.digest()).decode()
        else:
            h = hmac.new(self.key, raw, sha1)
            base64 = h.digest().encode("base64")
        _passwd = base64[0: self.passwd_length]
        return self._format_passwd(_passwd)

    def _format_passwd(self, passwd):
        # 格式化密码，必须包含大小写和数字
        self.num_str = "0123456789"
        self.low_letters = "abcdefghijklmnopqrstuvwxyz"
        self.upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        passwd = passwd.replace("+", '0')
        passwd = passwd.replace("/", '1')
        list_passwd = list(passwd)

        if re.search(r"[0-9]", passwd) is None:
            list_passwd[-3] = self.num_str[ord(passwd[-3]) % len(self.num_str)]

        if re.search(r"[a-z]", passwd) is None:
            list_passwd[-2] = self.low_letters[ord(passwd[-2]) % len(
                self.low_letters)]

        if re.search(r"[A-Z]", passwd) is None:
            list_passwd[-1] = self.upper_letters[ord(passwd[-1]) % len(
                self.upper_letters)]

        return ''.join(list_passwd)

    def _get_conn(self):
        if self.db_path is None:
            print ("You didn't set you PWD_DB_PATH ENV")
            sys.exit(1)
        try:
            conn = sqlite3.connect(self.db_path)
        except sqlite3.OperationalError:
            print ("PWD_DB_PATH: {} is invalid! (Is it a directory or a file?)".format(self.db_path))
            sys.exit(1)
        return conn

    def __enter__(self):
        self.conn = self._get_conn()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def _create_table(self):
        sql = """
        create table if not exists {}(
          `id` INTEGER PRIMARY KEY,
          `domain` varchar(32) ,
          `account` varchar(32),
          `batch` varchar(4) default NULL
          );
        """.format(self.table)

        with self:
            cur = self.conn.cursor()
            cur.execute(sql)
            sql = "PRAGMA table_info(pwm);"
            cur.execute(sql)
            for cid, name, _, _, _, _ in cur.fetchall():
                if name == "batch":
                    return
            else:
                sql = "ALTER TABLE %s ADD COLUMN batch varchar(4);" % (
                    self.table, )
                cur.execute(sql)

    def _insert_account(self, domain, account, batch=None):
        sql = "insert into {} (domain, account, batch) values "\
                "('{}', '{}', '{}');".format(
                    self.table, domain, account, batch)
        with self:
            cur = self.conn.cursor()
            cur.execute(sql,)

    def _query_account(self, keyword):
        if keyword:
            query = " where domain like '%{}%' or account like '%{}%' ".format(
                keyword, keyword)
        else:
            query = ""

        sql = "select id,domain,account,batch from {} {}".format(
            self.table, query)
        # print sql

        with self:
            cur = self.conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            return result

    def _delete(self, id):

        sql = "delete from {} where id={}".format(self.table, id)
        with self:
            cur = self.conn.cursor()
            cur.execute(sql)
            row_count = cur.rowcount
            return row_count

    def insert(self, domain, account, batch):
        self._create_table()
        self._insert_account(domain, account, batch or '')
        print("save success")

    @staticmethod
    def gen_sign_raw(domain, account, batch):
        raw = "{}@{}".format(account.encode("utf-8"), domain.encode("utf-8"))
        if batch:
            raw = "{}@{}".format(raw, str(batch))
        return raw

    def gen_account_passwd(self, domain, account, batch):

        raw = self.gen_sign_raw(domain, account, batch)
        return self.gen_passwd(raw)

    def delete(self, id):
        self._create_table()
        row_count = self._delete(id)
        print("remove success, {} record(s) removed".format(row_count, ))

    def search(self, keyword):

        self._create_table()
        if keyword == '*':
            keyword = ''

        result = self._query_account(keyword)
        return result


def main():

    db_path = os.getenv("PWM_DB_PATH", None)
    if db_path is None:
        print("##########WARNING:############")
        print("You didn't set you PWD_DB_PATH ENV")
        print("echo \"export PWM_DB_PATH=your_path\" >> ~/.bashrc")
        print("source ~/.bashrc")
        print("###############################")
    parse = OptionParser(version="{} {}".format(__package, __version))

    parse.add_option('-k', '--key', help="your secret key", nargs=0)
    parse.add_option('-d', '--domain', help="the domain of you account")
    parse.add_option('-a', '--account', help="the account used to login")
    parse.add_option(
        '-s', '--search',
        help="list your account and domain by search keyword")
    parse.add_option(
        '-w', '--save',
        help="save your account and domain", nargs=0)
    parse.add_option(
        '-r', '--remove',
        help="remove your account and domain by id", nargs=1, type=int)
    parse.add_option(
        '-b', '--batch',
        help="add batch to generate different passwd with same domain and account",  # noqa
        nargs=1, type=int)
    parse.add_option(
        '-c', '--copy',
        help="copy password to clipboard", nargs=0)
    (options, args) = parse.parse_args()

    if options.copy is not None:
        try:
            import xerox
        except ImportError:
            print ("you should install xerox module")
            sys.exit(1)

    if options.key is not None:
        key = getpass.getpass(prompt="your key:")
    else:
        key = ''

    pwm = PWM(key=key, db_path=db_path)

    # 搜索
    if options.search:
        result = pwm.search(options.search.strip())
        fmt = "{:5s}|{:40s}|{:35s}|{:20s}|{:5s}"
        print(fmt.format("ID", "DOMAIN", "ACCOUNT", "PASWORD", "BATCH"))
        print(fmt.format("-"*5, "-"*40, "-"*35, "-"*20, "-"*5))
        for item in result:
            passwd = pwm.gen_account_passwd(item[1], item[2], item[3])
            if options.copy is not None:
                xerox.copy(passwd)
            if is_py2:
                print(fmt.format(str(item[0]), item[1].encode("utf-8"), item[2].encode("utf-8"), passwd, item[3]))
            else:
                print(fmt.format(str(item[0]), item[1], item[2], passwd, item[3] or ''))


        print("\n{} records found.\n".format(len(result)))
        return

    # 删除
    if options.remove:
        pwm.delete(options.remove)
        return

    # 生成密码
    if bool(options.domain) is False or bool(options.account) is False:
        parse.print_help()
        return

    passwd = pwm.gen_account_passwd(
            options.domain, options.account, options.batch)
    if options.copy is not None:
        xerox.copy(passwd)
    print("generate password:{}".format(passwd))

    # 保存
    if options.save is not None:
        pwm.insert(options.domain, options.account, options.batch)


if __name__ == "__main__":
    main()
