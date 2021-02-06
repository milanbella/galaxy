from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from typing import NewType
from typing import Any
from typing import Dict
from typing import List

import psycopg2 # type: ignore
import os
import re
import collections

class AnyClass:
    def __getattr__(self, item: str) -> Any:
        pass

DbConnection = NewType('DbConnection', AnyClass)

cFILE = 'module_utils/idempiere.py'

class Idempiere:
    cCLASS = 'Idempiere' 
    cMIGRATION_DIR = 'migration'

    def __init__(self, idempiereInstallationPath: str, dbAdempiereUserPassword: str, dbHost: str, dbPort = 5432):
        self.idempiereInstallationPath = idempiereInstallationPath
        self.dbAdempiereUserPassword = dbAdempiereUserPassword
        self.dbHost = dbHost
        self.dbPort = dbPort

        if not os.path.isdir(self.idempiereInstallationPath):
            raise Exception('idempiereInstallationPath \'{}\' either does not exists or is not the directory'.format(idempiereInstallationPath))

    def getConnection(self) -> DbConnection:
        try:
            conn = psycopg2.connect(dbname='idempiere', user='adempiere', password = self.dbAdempiereUserPassword, host = self.dbHost, port = self.dbPort)
            return conn
        except:
            raise Exception('Could not connect do idempiere database')

    def getExecutedSqls(self) -> List[str]:
        try:
            con = self.getConnection()
            cur = con.cursor()
            cur.execute('select name from ad_migrationscript order by 1')
            result = cur.fetchall()
            result = list(map(lambda x: x[0], result))
            return result
        finally:
            con.close()
            cur.close()

    def getSourcodeSqls(self) -> List[Dict[str, str]]:
        migrationDirPath = '{}/{}'.format(self.idempiereInstallationPath, self.cMIGRATION_DIR)
        sqls = []
        for (dirpath, dirnames, filenames) in os.walk(migrationDirPath):
            for f in filenames:
                folder = os.path.split(dirpath)[0]
                folder = os.path.split(folder)[1]
                match = re.search(r'/(i\d+.\w+)/postgresql/.*\.sql', os.path.join(dirpath, f))
                if match != None:
                        sqls.append({
                            'filePath': os.path.join(dirpath, f),
                            'fileName': f,
                            'folder': folder,
                        })
        return sqls

    def getNotExecutedSqls(self, sourcodeSqls) -> List[Dict[str, str]]:
        sourcecodeSqls = self.getSourcodeSqls()
        executedSqls = self.getExecutedSqls()

        notExecutedSqls = []
        for sql in sourcecodeSqls:
            if sql['fileName'] not in set(executedSqls):
                notExecutedSqls.append(sql)

        return notExecutedSqls

    def getLocalSqlSqls(self) -> List[Dict[str, str]]:
        migrationDirPath = '{}/{}/{}'.format(self.idempiereInstallationPath, self.cMIGRATION_DIR, 'local_sql')
        sqls = []
        for (dirpath, dirnames, filenames) in os.walk(migrationDirPath):
            for f in filenames:
                match = re.search(r'/local_sql/.*\.sql', os.path.join(dirpath, f))
                if match != None:
                    sqls.append({
                        'filePath': os.path.join(dirpath, f),
                        'fileName': f,
                    })
        return sqls

    def getProcessesPostMigrationSqls(self) -> List[Dict[str, str]]:
        migrationDirPath = '{}/{}/{}/postgresql'.format(self.idempiereInstallationPath, self.cMIGRATION_DIR, 'processes_post_migration')
        sqls = []
        for (dirpath, dirnames, filenames) in os.walk(migrationDirPath):
            for f in filenames:
                match = re.search(r'/processes_post_migration/postgresql/.*\.sql', os.path.join(dirpath, f))
                if match != None:
                    sqls.append({
                        'filePath': os.path.join(dirpath, f),
                        'fileName': f,
                    })
        return sqls

    def getToBeExecutedSqls(self) -> List[str]:
        sourcodeSqls = self.getSourcodeSqls();
        notExecutedSqls = self.getNotExecutedSqls(sourcodeSqls);
        notExecutedSqls.sort(key = lambda d: (d['folder'], d['fileName']));
        notExecutedSqlsList = [x['filePath'] for x in notExecutedSqls]

        localSqlSqls = self.getLocalSqlSqls()
        localSqlSqls.sort(key = lambda d: d['fileName']);
        localSqlSqlsList = [x['filePath'] for x in localSqlSqls]

        processesPostMigrationSqls = self.getProcessesPostMigrationSqls()
        processesPostMigrationSqls.sort(key = lambda d: d['fileName']);
        processesPostMigrationSqlsList = [x['filePath'] for x in processesPostMigrationSqls]

        toBeExecutedSqlsList = notExecutedSqlsList + localSqlSqlsList + processesPostMigrationSqlsList
        return toBeExecutedSqlsList
