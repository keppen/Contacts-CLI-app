#!/usr/bin/env python3

import sqlite3 as sql
from sqlite3 import Error
import re

def create_connection (database):
    conn = None
    try:
        conn = sql.connect(database)
    except sql.Error as e:
        print (e)
        return None
    if conn:
        return conn

def create_table (conn, create_table_sql):
    '''
    Create a table form the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a Creation Table statement
    '''
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print (e)

def create_contact(conn, contact):
    '''
    create contact entry in contact table
    :param conn: Connection object
    :param contact: a Creation Contact Entry statement
    '''
    entry_sql = '''
    INSERT INTO contacts (last_name, first_name,
    tel_num, email)
    VALUES (?, ?, ?, ?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(entry_sql, contact)
        conn.commit()
    except sql.Error as err:
        e = str(err)
        e = e.split()
        if e[-1] ==  'contacts.email':
            print ('That email adress already exists')
        else:
            print ('That phone number already exists')
        return None
    else:
        return cur.lastrowid

def create_group (conn, group):
    '''
    create group entry in groups table
    :param conn: connection object
    :param group: a creation group statement
    '''
    entry_sql = '''
    INSERT INTO groups (grp)
    VALUES (?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(entry_sql, group)
        conn.commit()
    except sql.Error as e:
        print ('That group name already exists')
        return None
    else:
        return cur.lastrowid

def create_groups_contacts (conn, gr_con):
    '''
    create publisher entry in publisher table
    :param conn: connection object
    :param author: a creation publisher statement
    '''
    entry_sql = '''
    INSERT INTO groups_contacts (id_group, id_contact)
    VALUES (?, ?)
    '''
    cur = conn.cursor()
    cur.execute(entry_sql, gr_con)
    return cur.lastrowid

def search (conn, query):
    cur = conn.cursor()

    if query[0].lower() == 'contact':
        query_sql = '''
        SELECT * FROM contacts
        '''
        cur.execute(query_sql)
        rows = cur.fetchall()

        if len(query) > 1:
            query = list(query)
            query.pop(0)
            match = []
            try:
                query[0] = int(query[0])
            except ValueError:
                pass
            finally:

                if type(query[0]) is int:
                    for row in rows:
                        if re.search(str(query[0]), str( row[3] )):
                            match.append(row)
                    return (match)

                elif type(query[0]) is str:
                    word = str(query[0])
                    word = word.lower()
                    print (word)
                    for row in rows:
                        if re.search(word, row[1].lower()):
                            match.append(row)
                    return (match)
                else:
                    return None
        else:
            l = []
            for row in rows:
                l.append(row)
        return (l)

    if query[0].lower() == 'group':
        query_sql = '''
        SELECT * FROM groups
        '''
        cur.execute(query_sql)
        rows = cur.fetchall()


        if len(query) > 1:
            query = list(query)
            query.pop(0)
            match = []
            for row in rows:
                if re.search(query[0].lower(), row[1].lower()):
                    match.append(row)
            return (match)
        else:
            l = []
            for row in rows:
                l.append(row)
            else:
                return (l)
        query_sql = '''
        SELECT * FROM Users
        '''
        cur.execute(query_sql)
        usrs = cur.fetchall()

        tables = [titles, authors, publs, usrs]
        match = []

        for table in tables:
            t = []

            for word in query:
                for row in table:
                    if re.search(word, row[1]):
                        t.append(row[1])
            match.append(t)

        return (match)

def update (conn, query):
    '''
    update table enteries of choice
    :param conn: connection object
    :param option: tuple containg update query: table, column,
    updated value and entry
    '''
    if query[0] == 'contact':
        update_sql = 'UPDATE contacts SET '
        if query[1] == '1':
            update_sql += 'last_name = ? WHERE id = ?'
        elif query[1] == '2':
            update_sql += 'first_name = ? WHERE id = ?'
        elif query[1] == '3':
            update_sql += 'tel_num = ? WHERE id = ?'
        elif query[1] == '4':
            update_sql += 'email = ? WHERE id = ?'

    elif query[0] == 'group':
        update_sql = 'UPDATE groups SET '
        update_sql += 'grp = ? WHERE id = ?'

    try:
        update_val = (query[3], query[2])
        cur = conn.cursor()
        cur.execute(update_sql, update_val)
        conn.commit()
    except sql.Error as err:
        e = str(err)

        e = e.split()
        if e[-1] == 'contacts.email':
            print ('That email adress already exists')
        elif e[-1] == 'contacts.num_tel':
            print ('That phone number already exists')
        else:
            print ('That group already exists')
        return None
    else:
        return True


def delete (conn, query):

    if query[0] == 'contact':
        delete_sql = 'DELETE FROM contacts  WHERE id = ?'
    elif query[0] == 'group':
        delete_sql = 'DELETE FROM groups  WHERE id = ?'

    delete_val = query[1]
    cur = conn.cursor()
    cur.execute(delete_sql, (delete_val,))
    conn.commit()

def view (conn, query):


    if query[0] == 'contact':
        view_sql = '''
        SELECT * FROM contacts WHERE id = ?
        '''

        view_val = (query[1],)
        cur = conn.cursor()
        cur.execute(view_sql, view_val)
        entry = cur.fetchone()


        return entry

    else:

        view_group_sql = '''
        SELECT * FROM groups WHERE id = ?
        '''
        view_groups_contacts_sql = '''
        SELECT * FROM groups_contacts WHERE id_group = ?
        '''
        view_contacts_sql =  '''
        SELECT * FROM contacts WHERE id = ?
        '''
        view_val = (query[1],)
        cur = conn.cursor()

        cur.execute(view_group_sql, view_val)
        group_name = cur.fetchone()

        cur.execute(view_groups_contacts_sql, view_val)
        cont = cur.fetchall()

        contacts_list = []
        for i in range (len (cont)):
            cur.execute(view_contacts_sql, (cont[i][0],))
            c = cur.fetchone()
            c =list(c)
            c.append(i)
            contacts_list.append(c)
        contacts_list.append(group_name)

        return contacts_list



