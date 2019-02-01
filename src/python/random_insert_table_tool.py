#! /usr/bin/python
# encoding=utf-8

import ibm_db
import time
import random
import string


class RandomInsertTable(object):
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        # get db connection
        self.connection = self.__connect()


    def __connect(self):
        dbinfo = 'DATABASE='+self.database+';HOSTNAME='+self.host+';PORT='+str(self.port)+';PROTOCOL=TCPIP;UID='+self.username+';PWD='+self.password
        try:
            connection = ibm_db.connect(dbinfo, "", "")
            return connection
        except:
            print 'get db connection failed!'


    def __get_table_cols_info(self, schema, table):
        '''
        获取表结构信息，解析列的信息并返回
        :param schema: 模式名
        :param table: 表名
        :return: 表结构信息
        '''
        sql = "select KEYSEQ,COLNAME,TYPENAME,LENGTH,SCALE from syscat.columns where tableschema='" + schema.upper() + "' and tabname='" + table.upper() + "' order by colno with ur;"
        stmt = ibm_db.exec_immediate(self.connection, sql)
        result = ibm_db.fetch_both(stmt)
        if not result:
            print 'get table '+schema+'.'+table+' structure info failed!'
            return
        cols = {}
        while result:
            col = result['COLNAME']
            cols[col] = {}
            cols[col]['TYPENAME'] = result['TYPENAME']
            cols[col]['LENGTH'] = result['LENGTH']
            cols[col]['KEYSEQ'] = result['KEYSEQ']
            cols[col]['SCALE'] = result['SCALE']
            result = ibm_db.fetch_both(stmt)
        return cols



    def __get_keyseq_inf(self, cols):
        '''
        获取主键信息，以便于构造主键
        :param cols: 表的列信息
        :return: 主键的总长度，
                 主键字段在主键中的取值起始位置, 如[0, 4, 24, 27] 表示有3个主键, 截取主键字符中的0-3,4-23,24-27位
        '''
        keyLenTotal = 0 # 主键字段总长度
        keyColLen = {} # 联合主键每个主键的长度, 按主键顺序
        keyColBegin = [0, ] # 联合主键中每个主键在整体主键中的开始和结束位置, 便于截取
        for key in cols:
            if cols[key]['KEYSEQ']:
                keyLenTotal += cols[key]['LENGTH']
                keyColLen[cols[key]['KEYSEQ']] = cols[key]['LENGTH']
        for keyLen in sorted(keyColLen):
            keyColBegin.append(keyColBegin[-1] + keyColLen[keyLen])
        return [keyLenTotal, keyColBegin]


    def insert_random(self, schema, table, sample=None):
        '''
        随机插入1条记录
        :param schema: 模式名
        :param table: 表名
        :param sample: 可选参数, 阳历值, 如果提供, 则主键除外, 其他值取样例里的值
        :return: None
        '''
        cols = self.__get_table_cols_info(schema, table)
        [keyLenTotal, keyColBegin] = self.__get_keyseq_inf(cols)
        insertsqlvalues = []
        columns = []
        for key in cols:
            value = None
            if sample:
                value = sample[key]
                if value == None:
                    continue #该字段不处理
            columns.append(key)
            #to promise key is unique
            current_timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
            pk = current_timestamp + self.__gen_random_nnbr(keyLenTotal - len(current_timestamp)) #主键为时间戳+随机数字
            if cols[key]['KEYSEQ']:
                value = pk[int(keyColBegin[int(cols[key]['KEYSEQ']) - 1]): int(keyColBegin[int(cols[key]['KEYSEQ'])])]
            typename = cols[key]['TYPENAME']
            if typename == 'DECIMAL':
                value = self.__gen_random_nnbr(1)+'.'+self.__gen_random_nnbr(cols[key]['SCALE']) if not value else value
            elif typename == 'INTEGER' or typename == 'SMALLINT':
                value = self.__gen_random_nnbr(int(cols[key]['LENGTH']) - 1 if not int(cols[key]['LENGTH']) > 1 else 1) if not value else str(value)
            elif typename == 'DATE':
                value = "'" + time.strftime('%Y-%m-%d', time.localtime()) + "'" if not value else ("'" + unicode(value)+"'")
            elif typename == 'TIME':
                value = "'" + time.strftime('%H:%M:%S', time.localtime()) + "'" if not value else ("'" + unicode(value) + "'")
            elif typename == 'TIMESTAMP':
                value = "'" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "'" if not value else ("'" + unicode(value) + "'")
            else:  # VARCHAR or CHAR
                value = "'" + self.__gen_random_nstr((int(cols[key]['LENGTH']))) + "'" if not value else "'" + unicode(value) + "'"
            insertsqlvalues.append(value)

        insertsql = 'INSERT INTO '+schema.upper()+"."+table.upper()+' ( '+','.join(columns)+' ) VALUES ( ' + ','.join(insertsqlvalues) + ' )'
        print insertsql
        insertstmt = ibm_db.exec_immediate(self.connection, insertsql)
        print 'exec status: ', 'failed' if not insertstmt else 'success'



    def insert_random_n(self, schema, table, n, sample=None):
        '''
        随机插入n条记录
        :param schema: 模式名
        :param table: 表名
        :param n: 数量
        :param sample:
        :return: 可选参数, 阳历值, 如果提供, 则主键除外, 其他值取样例里的值
        '''
        for i in range(n):
            self.insert_random(schema, table, sample)


    def insert_like_first_record(self, schema, table):
        '''
        类似第一条记录, 构造主键插入1条记录
        :param schema: 模式名
        :param table: 表名
        :return: None
        '''
        sample = self.__get_first_record(schema, table)
        self.insert_random(schema, table, sample)


    def insert_like_first_record_n(self, schema, table):
        '''
        类似第一条记录, 构造主键插入n条记录
        :param schema: 模式名
        :param table: 表名
        :return: None
        '''
        sample = self.__get_first_record(schema, table)
        self.insert_random_n(schema, table, sample)


    def __get_first_record(self, schema, table):
        '''
        获取数据表的第一行记录
        :param schema: 模式名
        :param table: 表名
        :return: 第一行记录, 可能为 None
        '''
        sql = 'SELECT * FROM '+schema.upper()+'.'+table.upper()+" fetch first 1 rows only with ur"
        stmt = ibm_db.exec_immediate(self.connection, sql)
        result = ibm_db.fetch_both(stmt)
        return result


    def __gen_random_nstr(self, n):
        '''
        返回随机n长度数字字符组成的字符串
        :param n: 长度
        :return: 数字字母字符串
        '''
        return ''.join(random.choice(string.digits + string.letters) for _ in range(n))


    def __gen_random_nnbr(self, n):
        '''
        返回随机长度为n的数字组成的字符串
        :param n: 长度
        :return: 数字字符串
        '''
        return ''.join(random.choice(string.digits) for _ in range(n))



if __name__ == '__main__':
    rit = RandomInsertTable("127.0.0.1", 50000, "dbname", "username", "password")
    rit.insert_random("schema", "table")
    rit.insert_random_n("schema", "table", 2)
    rit.insert_like_first_record("schema", "table")
    rit.insert_like_first_record_n("schema", "table", 3)