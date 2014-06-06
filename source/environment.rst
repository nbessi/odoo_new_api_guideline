Record/Recordset and Model
==========================

Model
-----
Model doe not really change

Recordset
---------
Represents a list of record.
But Recordset are also an instance of Model.
Using the magic of meta you can call Model function.

If you use @api.one decorator on a function calling
a Model function on a Recordset it will automagically loop
an call the function on Recordset records

The write function can now be call from Model, RecordSet, or Record
as it is decorated with @api.one

When calling a property on a RecordSet it will affect only the first record.
Only Recordset id property will return the list of ids.

Record
------

Record of a row of the model.
I has accessor and allows you to access relations: ::
  record = self
  record.name
  >>> toto
  record.partner_id.name
  >>> partner name

Record does now  respect of active record pattern: ::

  record = self
  record.name = 'new name'

This will update value on the cache and call the write function and trigger a write action an the Database.
At the end of proccess call it will be committed on database.

Environment
===========
now the environement replace the pooler
It has est special item getter to return Model
It add the cursor, uid, and context property.

To acess it use: ::
 self.env
 # or
 model.env

Environnement is immutable and can not be modified in place.
So how to modify the current environnement

Environment also store the cache or record set etc.
So there is many cache one per environement.

See drawing:

Modifing environnement
----------------------
If you need to use the with_context(tz=x, cr=y, context={})
Adding kwargs extend the current dictionnary, positional arg replace dictionnary. ::

  self.env['res.partner'].with_context(tz=x).create(vals)

if will modifiy the current record. In fact it will be rebrowse the record
and return a new browsed record. As self is a locally scoped variable it will
not affect global Record set except if you reassing self.

Do not reassing self ther is a great chance to fucked up the caches and environnement

Chaning User
############

recs.sudo(user)
recs.sudo()


Cleaning environnement cache
----------------------------
You can invalidate your cache by using the environement.

To do this simply do: ::
  self.env.invalidate_all()

Searching
---------

search
######
Now seach function return directly a RecordSet


search_read
###########
Now seach function return directly a list of dict


search_count
############
Retruns count of ids


Browsing
--------
Just get ids / id

writing
-------

From record
###########

@api.one
...
self.KYwrite({'key': value })
or
record.write({'key': value})
or
record.name = value # it will call write behind the hood

From RecordSet
##############

@api.mutli
...
self.write({'key': value })
it will write on all record.

!! if you do self.name only first record will be written

self.line_ids.write({'key': value })

will write on all record set of the relation line_ids

From Model
##########
TODO

Copy
----

TODO

copy data


Dry run
--------
if you use the do_in_draft contenxt manager of Environnement
It will not be committed but only be done in cache.


Using Cursor
============

Record Recordset and environment share the same cursor.

So you can access cursor using: ::

  def my_fun(self):
      cursor = self._cr
      # or
      self.env.cr
Then you cau use cursor like in previous API

Using thread
============
When using thread you have to create you own cursor
and initiate a new environnement for each thread.
committing is done by committing the cursor.

   with Environment.manage(): #class function
      env = Environnement(cr, uid, context)

 Cache
=======

New cache is now automatically invalidated.
When you do manual SQL you have to invalidate cache manually: ::
  invalidate_cache
