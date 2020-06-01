#!/usr/bin/env python3

import contacts
import click
from  contacts import functions as foo
import os.path
from contacts import interf
import sys


@click.group()
def cli():
    pass


@cli.command()
@click.option('--what', help = 'Chose an item to create',
        type = click.Choice(['contact', 'group'], case_sensitive= False))
def create(what):
    '''Adding an entry into selected table'''
    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))
    if not conn:
        return None
    if what == 'contact'.lower():

        l_n = interf.get_any('Enter last name (mendatory): ')
        if l_n == 'q':
            sys.exit('Canceled')
        f_n = str(raw_input('Enter first name : '))
        if f_n == 'q':
            sys.exit('Canceled')
        t_n = interf.get_int('Enter telefon number (mendatory): ')
        if t_n == 'q':
            sys.exit('Canceled')
        e_a = str(raw_input('Enter e-mail adress: '))
        if e_a == 'q':
            sys.eixt('Canceled')

        query = (l_n, f_n, t_n, e_a)

        i = foo.create_contact(conn, query)
    else:
        g_n = interf.get_any('Enter group name (mendatory): ')
        if g_n == 'q':
            sys.exit ('Canceled')
        query = (g_n,)
        i = foo.create_group(conn, query)
    if i:
        sys.exit('Done!')

@cli.command()
@click.option('--what', help = 'Choose an entry to update.',
        type = click.Choice(['contact', 'group'], case_sensitive = False))
@click.option('--entry', help = '''
        (In regard only to contacts)\n
        Choose specific value to undpate\n
        1 - Last name\n
        2 - First name\n
        3 - Telephone number\n
        4 - Email adress
        ''',
        type = click.Choice(['1', '2', '3', '4']))
def update(what, **entry):
    '''Updtaing existing entry'''

    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))

    if not conn:
        sys.exit('Could not connect to the database')

    if what.lower() == 'contact':

        old_val = interf.pick_one('Choose entry by telephone \
number or last name: ', what, conn)
        if entry['entry'] == '1':
            new_val = interf.get_any('Enter new last name: ')
            if new_val == 'q':
                sys.exit('Canceled')
        if entry['entry'] == '2':
            new_val = str(raw_input('Enter new first name: '))
            if new_val == 'q':
                sys.exit('Canceled')
        if entry['entry'] == '3':
            new_val = interf.get_int('Enter new telefon number: ')
            if new_val == 'q':
                sys.exit('Canceled')
        if entry['entry'] == '4':
            new_val = interf.get_any('Enter new email adress: ')
            if new_val == 'q':
                sys.exit('Canceled')


        query = (what,entry['entry'], old_val, new_val)


        i = foo.update(conn, query)


    else:
        old_val = interf.pick_one('Choose entry by group name: ', what, conn)

        new_val = interf.get_any('Enter new group name: ')
        if new_val == 'q':
            sys.exit ('Canceled')
        query = (what,'grp', old_val, new_val)
        i = foo.update(conn, query)
    if i:
        sys.exit('Done!')
@cli.command()
@click.option('--what', help = 'Choose an entry to delete from.',
        type = click.Choice(['contact', 'group'], case_sensitive = False))
def delete(what):
    '''Deteting existing entry'''

    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))

    if not conn:
        sys.exit('Could not connect to the database')

    if what == 'contact':
        val = interf.pick_one('Choose entry to delete by last name or\
telephone number: ', what, conn)
    else:
        val = interf.pick_one('Choose entry to delete by last name or\
 telephone number: ', what, conn)
    query = (what, val)
    i = foo.delete(conn, query)
    if i:
        sys.exit('Done')

@cli.command()
@click.option('--what', help = 'Choose an category to list out.',
        type = click.Choice(['contact', 'group'], case_sensitive = False))
def all(what):
    '''View content of chosen category'''

    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))


    if not conn:
        sys.exit('Could not connect to the database')

    interf.browse(what, conn, value = None)

    sys.exit('Done')

@cli.command()
@click.option('--what', help = 'Choose view contents of an entry.',
        type = click.Choice(['contact', 'group'], case_sensitive = False))
def view(what):
    '''View content of chosen entry'''

    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))

    if not conn:
        sys.exit('Could not connect to the database')

    val = interf.pick_one('Seach for a entry to view: ', what, conn)
    i = foo.view(conn, (what, val))
    try:
        msg = ('Group name - %s\n\nContent\n') % (i[-1][-1],)
        msg += ('%12s %12s %12s %24s\n\n') % ('Last name', 'First name',
                                          'Phone number', 'Email adress')

        for j in range(len(i) -1):
            msg += ('%12s %12s %12d %24s\n') % (i[j][1], i[j][2],
                                                i[j][3], i[j][4])
        print (msg)
    except TypeError:
        msg = ('%12s %12s %12s %24s\n\n') % ('Last name', 'First name',
                                         'Phone number', 'Email adress')
        msg += ('%12s %12s %12d %24s') % (i[1], i[2], i[3], i[4])

        print (msg)
    finally:
        sys.exit()

@cli.command()
def add ():
    '''View content of chosen entry'''

    path = os.path.abspath(contacts.__file__)
    path = os.path.split(path)[0]
    conn =foo.create_connection(os.path.join (path, 'database/libr.db' ))


    if not conn:
        sys.exit('Could not connect to the database')

    
