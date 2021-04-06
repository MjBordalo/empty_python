from db_access import SqlActions


"""
To use this you need to create user, database and tables.
"""

db = SqlActions("localhost", "test_user", "qweasd", "smart_water",cnx_active=True, debug=True)

what = db.other_simple_query("INSERT INTO sw_sector (id, name) VALUES (2, 'fixolas');", "couves", table_changed="sw_secto")
print("WHAT?? {}".format(what))
what = db.other_simple_query("DELETE FROM sw_sector WHERE id = 2;", "delete", table_changed="sw_sector")
print("WHAT!! {}".format(what))

