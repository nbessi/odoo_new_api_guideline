Record/Recordset and Model
==========================

The new version 8.0 of OpenERP/Odoo introduce a new ORM API.
It intends to add more coherent and concise syntax and provide a bi-directional compatiblity.

The new API keeps his previous root design as Model and record but now adds
new concept like Environnement and Recordset.

Some aspect of the API will not change with this release like the domain syntax


Model
-----
A model is a representation of a business Object.

It is bascially a class that have has class property various fields that are stored in Database.
All functions define in a Model can previously be called directly.

This paradigm has changes as generaly you should not access Model directly but a RecordSet see :ref:`recordset`

To instanciate a model you must inherit an openerp.model.Model: ::

    from openerp import Model, fields, api, _


    class MyModel(Model):

        _name = 'a.model' #  Model identifer used for table name

        firstname = fields.Char(string="Firstname")


Inheritance
###########

The inheritance mechanisms have not change you can use: ::

    class MyModelExtended(Model):
         _inherit = 'a.model' # direct heritage
         _inherit = ['a.model, 'a.other.model']' # direct heritage
         _inherits = {'a.model': 'field_name'} # polymorphique heritage

For more detail about inheritance please have a look at

  `Inherit <https://www.odoo.com/forum/Help-1/question/The-different-openerp-model-inheritance-mechanisms-whats-the-difference-between-them-and-when-should-they-be-used--46#answer-190>`_

For fields inheritance please :ref:`fields_inherit`

.. _recordset:

Recordset
---------
All instances of Model are at the same time an instance of a RecordSet.
A Recorset represents a sorted set of record of the same Model of the RecordSet.

You can call function on recordset: ::

    class AModel(Model):
    # ...
        def a_fun(self):
            self.do_something() # here self is a recordset a mix between class and set
            record_set = self
            record_set.do_something()

        def do_something(self):
            for record in self:
               print record

In this example the function are define at model level but when executing the code
the `self` varibale is in fact a instance of RecordSet containing many records.

So the self passe in the `do_something` is a RecordSet holding a list of records.

If you decorate a function with `@api.one` it will automagically loop
on the recording and self will this time be a Record.

As described in :ref:`records` you have now access to an pseudo active record pattern

If you use it on a record set it will break if recordset does not contains only one item.


Supported opperations
---------------------
Record set support set opperation
you can add, union and intersect recordset: ::

    record in recset1 #  include
    record not in recset1 #  not include
    recset1 + recset2 #  sum
    recset1 | recset2 #  union
    recset1 & recset2 #  intersect
    recset1 - recset2 #  difference
    recset.copy() # to copy recordset (not a deep copy)

Only the `+`  operator preserves order

RecordSet can also be sorted: ::

  sorted(recordset, key=lambda x: x.column)


The ids attribute
-----------------

.. _records:

Record
------

A Record mirrors a "populated instance of Model Record" fetch from database.
I propose abstaction over database using caches and query generation: ::

  record = self
  record.name
  >>> toto
  record.partner_id.name
  >>> partner name

Active Record Pattern
#####################

One of the new features introduced by the new API is a basic support of active record pattern.
You can now write to database by setting propertx: ::

  record = self
  record.name = 'new name'

This will update value on the cache and call the write function to  trigger a write action on the Database.

Active Record Pattern Be Careful
################################

Writing value using Active Record pattern must be done carefully.
As each assignement will trigger a write action on database: ::
    @api.one
    def dangerous_write(self):
      self.x = 1
      self.y = 2
      self.z = 4

On this sample each assignement will trigger a write.
As the function is decorated with `@api.one` for each record in RecordSet write will be called 3 time
So if you have 10 records in recordset the number of write will be 10*3 = 30.

This may not cause any problems if you are in a simple on change context but on an heavy task you should: ::

    def better_write(self):
       for rec in self:
          rec.write({'x': 1, 'y': 2, 'z': 4})

    # or

    def better_write2(self):
       #same value on all records
       self.write({'x': 1, 'y': 2, 'z': 4})

M2m one2m behavior.
####################
One2many and Many2many fields have some special behavior to be taken in account.
At that time (This may change at release) using create on a multiple relation fields
will not introspect to look for relation. ::

  self.line_ids.create({'name': 'Tho'}) #  this will fail as order is not set
  self.line_ids.create({'name': 'Tho', 'order_id': self.id}) #  this will work
  self.line_ids.write({'name': 'Tho'}) #  this will write all related lines



Chain of browse null
####################
!!Subject to changes!!

Empty relation now return Null Value.

In the new API if you chain a relation with many empty relation.
Each relation will be chained and a Null should be return at the end.

Environment
===========
In the new API the notion of Environment is introduced.
His main objective is to provide an encapsulation around
cursor, user_id, model, and context, Recordset and caches

See drawing:


With this adjonction you are not anymore forced to pass the infamous function signature: ::
    # before
    def afun(self, cr, uid, ids, context=None):
        pass

    # now
    def afun(self):
        pass


To acess to environnement you may use: ::

    def afun(self):
         self.env
         # or
         model.env

Environnement sould be immutable and may not be modified in place as
it  also store the caches or recordset etc.


Modifing environnement
----------------------
If you need to use modifiy your current context you
may use the with_context() function. ::

  self.env['res.partner'].with_context(tz=x).create(vals)

Be careful not to modify current RecordSet using this functionnality: ::

   self = self.env['res.partner'].with_context(tz=x).browse(self.ids)

if will modifiy the current records in RecordSet after a rebrowse.
This will generate an incoherence between caches and RecordSet.

Chaning User
############

Environement provides an helper to switch user: ::

    self.sudo(user.id)
    self.sudo() # This will use the SUPERUSER_ID by default
    # or
    self.env['res.partner'].sudo()

Cleaning environnement caches
-----------------------------
As explained previously An environnement maintain multiple caches
That are triggered by the Moded/Fields classes.

Sometime you will have to do insert/write using your the cursor.
In this cases you want to invalidate the caches: ::

  self.env.invalidate_all()

Commons action
==============

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
If you use the do_in_draft helper of context manager of Environnement
No changes will be committed in database only cache will be altered.


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
