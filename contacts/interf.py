import learn.functions as foo
import sys
def get_int (prompt):

    try:
        value = input(prompt)

        if value == 'q':
            sys.exit('Canceled')

        value = int(value)
    except ValueError:
        print ('It is not a natual number')
        return get_int(prompt)

    if value < 0:
        print ('It is not a positive number')
        return get_int(prompt)
    else:
        return value

def get_any (prompt):

    try:
        value = input(prompt)
        if not value:
            raise ValueError

        elif value == 'q':
            sys.exit('Canceled')

    except ValueError:
        print ('Can not be empty')
        get_any(prompt)
    else:
        return value

def browse (where, conn, **kargs):

        query = [where, kargs['value']]
        if query[1] is None:
            query.pop(1)
        query = tuple(query)
        hits = foo.search(conn, query)

        if where == 'contact':

            if len(hits) > 0:

                msg = '''
Found more than one entry\n\n'''
                msg+= ('%5s %12s %12s %12s\n') % ('Digit', 'Last name',
                                                'First name', 'Phone number')
                l = []
                for i in range (len(hits)):
                    h = list(hits[i])
                    h.append(i)
                    l.append(h)

                for i in l:
                    msg+= ('%5d %12s %12s %12d\n') % (i[-1], i[1], i[2], i[3])
                print (msg)
                return l

            elif len(hits) == 1:
                return list(hits)

            else:
                print ('Nothing has been found')
                return None
        else:

            if len(hits) > 0:



                msg = '''
Found more than one entry\n\n'''
                msg+= ('%5s %12s\n') % ('Digit', 'Group name')

                l = []
                for i in range (len(hits)):
                    h = list(hits[i])
                    h.append(i)
                    l.append(h)

                for i in l:
                    msg+= ('%5d %12s\n') % (i[-1], i[1])
                print (msg)
                return l

            else:
                print ('Nothing has been found')
                return None

def pick_one(prompt, where, conn):

    try:
        value = get_any(prompt)
        hits = browse( where, conn, value = value)
        print (hits)
        if not hits:
            raise ValueError
    except ValueError:
        pick_one(prompt, where, conn)
    else:
        while True:
            value = get_int("Choose an entry by digit: ")
            if value > hits[-1][-1]:
                print ('Wrong digit')
            else:
                for i in hits:
                    if value == i[-1]:
                        print (i[0])
                        return i[0]


