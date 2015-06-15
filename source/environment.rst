Record/Recordset and Model
==========================

The new version 8.0 of OpenERP/Odoo introduce a new ORM API.

It intends to add a more coherent and concise syntax and provide a bi-directional compatibility.

The new API keeps its previous root design as Model and Record but now adds
new concepts like Environment and Recordset.

Some aspects of the previous API will not change with this release, e.g. the domain syntax.


Model
-----

A model is a representation of a business Object.

It is basically a class that define various class know-how and fields that are stored in database.
All functions defined in a Model where previously callable directly by the Model.

This paradigm has changed as generally you should not access Model directly but a RecordSet see :ref:`recordset`

To instantiate a model you must inherit an openerp.model.Model: ::

    from openerp import models, fields, api, _


    class MyModel(models.Model):

        _name = 'a.model'  # Model identifer used for table name

        firstname = fields.Char(string="Firstname")


Inheritance
###########

The inheritance mechanism has not changed. You can use: ::

    class MyModelExtended(Model):
         _inherit = 'a.model'                       # direct heritage
         _inherit = ['a.model, 'a.other.model']     # direct heritage
         _inherits = {'a.model': 'field_name'}      # polymorphic heritage

For more details about inheritance please have a look at

  `Inherit <https://www.odoo.com/forum/Help-1/question/The-different-openerp-model-inheritance-mechanisms-whats-the-difference-between-them-and-when-should-they-be-used--46#answer-190>`_

for fields inheritance please read :ref:`fields_inherit`

.. _recordset:

Recordset
---------

All instances of Model are at the same time instances of a RecordSet.
A Recordset represents a sorted set of records of the same Model as the RecordSet.

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

In this example the functions are defined at model level but when executing the code
the ``self`` variable is in fact an instance of RecordSet containing many Records.

So the self passed in the ``do_something`` is a RecordSet holding a list of Records.

If you decorate a function with ``@api.one`` it will automagically loop
on the Records of current RecordSet and self will this time be the current Record.

As described in :ref:`records` you have now access to a pseudo Active-Record pattern

.. note::
   If you use it on a RecordSet it will break if recordset does not contains only one item.!!


Supported Operations
--------------------

RecordSet also support set operations
you can add, union and intersect, ... recordset: ::

    record in recset1       # include
    record not in recset1   # not include
    recset1 + recset2       # extend
    recset1 | recset2       # union
    recset1 & recset2       # intersect
    recset1 - recset2       # difference
    recset.copy()           # to copy recordset (not a deep copy)

Only the ``+``  operator preserves order

RecordSet can also be sorted: ::

  sorted(recordset, key=lambda x: x.column)

Useful helpers
--------------

The new API provides useful helper on recordset to use them in a more functional apprach

You can filter an exisiting recordset quite easily: ::

    recset.filtered(lambda record: record.company_id == user.company_id)
    # or using string
    recset.filtered("product_id.can_be_sold")

You can sort a recordset: ::
    
    # sort records by name
    recset.sorted(key=lambda r: r.name)

You can also use the operator module: ::
    
    from operator import attrgetter
    recset.sorted(key=attrgetter('partner_id', 'name'))
    
There is an helper to map recordsets: ::

    recset.mapped(lambda record: record.price_unit - record.cost_price)
    
    # returns a list of name
    recset.mapped('name')

    # returns a recordset of partners
    recset.mapped('invoice_id.partner_id')

The ids Attribute
-----------------

The ids attribute is a special attribute of RecordSet.
It will be return even if there is more than one Record in RecordSet

.. _records:

Record
------

A Record mirrors a "populated instance of Model Record" fetched from database.
It proposes abstraction over database using caches and query generation: ::

  >>> record = self
  >>> record.name
  toto
  >>> record.partner_id.name
  partner name


Displayed Name of Record
########################

With new API a notion of display name is introduced.
It uses the function ``name_get`` under the hood.


So if you want to override the display name you should override the ``display_name`` field.
`Example <https://github.com/odoo/odoo/blob/8.0/openerp/addons/base/res/res_partner.py#L232>`_


If you want to override both display name and computed relation name you should override ``name_get``.
`Example <https://github.com/odoo/odoo/blob/8.0/addons/event/event.py#L194>`_


.. _ac_pattern:

Active Record Pattern
#####################

One of the new features introduced by the new API is a basic support of the active record pattern.
You can now write to database by setting properties: ::

  record = self
  record.name = 'new name'

This will update value on the caches and call the write function to trigger a write action on the Database.


Active Record Pattern Be Careful
################################

Writing value using Active Record pattern must be done carefully.
As each assignement will trigger a write action on the database: ::


    @api.one
    def dangerous_write(self):
      self.x = 1
      self.y = 2
      self.z = 4

On this sample each assignement will trigger a write.
As the function is decorated with ``@api.one`` for each record in RecordSet write will be called 3 times.
So if you have 10 records in recordset the number of writes will be 10*3 = 30.

This may cause some trouble on an heavy task. In that case you should do: ::

    def better_write(self):
       for rec in self:
          rec.write({'x': 1, 'y': 2, 'z': 4})

    # or

    def better_write2(self):
       # same value on all records
       self.write({'x': 1, 'y': 2, 'z': 4})


Chain of Browse_null
####################


Empty relation now returns an empty RecordSet.

In the new API if you chain a relation with many empty relations,
each relation will be chained and an empty RecordSet should be return at the end.


Environment
===========

In the new API the notion of Environment is introduced.
Its main objective is to provide an encapsulation around
cursor, user_id, model, and context, Recordset and caches

.. image:: Diagram1.png


With this adjonction you are not anymore forced to pass the infamous function signature: ::


    # before
    def afun(self, cr, uid, ids, context=None):
        pass

    # now
    def afun(self):
        pass


To access the environment you may use: ::

    def afun(self):
         self.env
         # or
         model.env

Environnement should be immutable and may not be modified in place as
it also stores the caches of the RecordSet etc.


Modifing Environment
--------------------

If you need to modifiy your current context you
may use the with_context() function. ::

  self.env['res.partner'].with_context(tz=x).create(vals)

Be careful not to modify current RecordSet using this functionality: ::

   self = self.env['res.partner'].with_context(tz=x).browse(self.ids)


It will modifiy the current Records in RecordSet after a rebrowse and will generate an incoherence between caches and RecordSet.


Changing User
#############

Environment provides an helper to switch user: ::

    self.sudo(user.id)
    self.sudo()   # This will use the SUPERUSER_ID by default
    # or
    self.env['res.partner'].sudo().create(vals)

Accessing Current User
######################

::

    self.env.user
    

Fetching record using XML id
############################

::

    self.env.ref('base.main_company')

Cleaning Environment Caches
---------------------------

As explained previously an Environment maintains multiple caches
that are used by the Moded/Fields classes.

Sometimes you will have to do insert/write using the cursor directly.
In this cases you want to invalidate the caches: ::

  self.env.invalidate_all()


Common Actions
==============

Searching
---------
Searching has not changed a lot. Sadly the domain changes
announced did not meet release 8.0.

You will find main changes below.


search
######

Now seach function returns directly a RecordSet: ::

    >>> self.search([('is_company', '=', True)])
    res.partner(7, 6, 18, 12, 14, 17, 19, 8,...)
    >>> self.search([('is_company', '=', True)])[0].name
    'Camptocamp'

You can do a search using env: ::

    >>> self.env['res.users'].search([('login', '=', 'admin')])
    res.users(1,)


search_read
###########

A ``search_read`` function is now available. It will do a search
and return a list of dict.

Here we retrieve all partners name: ::

    >>> self.search_read([], ['name'])
    [{'id': 3, 'name': u'Administrator'},
     {'id': 7, 'name': u'Agrolait'},
     {'id': 43, 'name': u'Michel Fletcher'},
     ...]

search_count
############
The ``search_count`` function returns the count of results matching search domain: ::

    >>> self.search_count([('is_company', '=', True)])
    26L

Browsing
--------
Browsing is the standard way to obtain Records from the
database. Now browsing will return a RecordSet: ::

    >>> self.browse([1, 2, 3])
    res.partner(1, 2, 3)

More info about record :ref:`records`


Writing
-------

Using Active Record pattern
###########################

You can now write using Active Record pattern: ::

    @api.one
    def any_write(self):
      self.x = 1
      self.name = 'a'

More info about the subtility of the Active Record write pattern here :ref:`records`

The classical way of writing is still available.

From Record
###########

From Record:  ::

    @api.one
    ...
    self.write({'key': value })
    # or
    record.write({'key': value})


From RecordSet
##############

From RecordSet: ::

    @api.multi
    ...
    self.write({'key': value })
    # It will write on all record.
    self.line_ids.write({'key': value })

It will write on all Records of the relation line_ids

Many2many One2many Behavior
###########################

One2many and Many2many fields have some special behavior to be taken in account.
At that time (this may change at release) using create on a multiple relation fields
will not introspect to look for the relation. ::

  self.line_ids.create({'name': 'Tho'})   # this will fail as order is not set
  self.line_ids.create({'name': 'Tho', 'order_id': self.id})  # this will work
  self.line_ids.write({'name': 'Tho'})    # this will write all related lines

When adding new relation records in an :ref:`@api.onchange` method, you can use
the :py:meth:`openerp.models.BaseModel.new` constructor. This will create a record that is not committed to the
database yet, having an id of type :py:class:`openerp.models.NewId`. ::

    self.child_ids += self.new({'key': value})

Such records will be committed when the form is saved.

Copy
----

.. note::
   Subject to change, still buggy !!!

From Record
###########

From Record: ::

    >>> @api.one
    >>> ...
    >>>     self.copy()
    broken


From RecordSet
##############

From RecordSet: ::

    >>> @api.multi
    >>> ...
    >>>     self.copy()
    broken


Create
------

Create has not changed, except the fact it now returns a recordset: ::

  self.create({'name': 'New name'})


Dry run
--------

You can do action only in caches by using the ``do_in_draft`` helper of Environment context manager.


Using Cursor
============

Record Recordset and environment share the same cursor.

So you can access cursor using: ::

  def my_fun(self):
      cursor = self._cr
      # or
      self.env.cr

Then you can use cursor like in previous API


Using Thread
============
When using thread you have to create you own cursor
and initiate a new environment for each thread.
committing is done by committing the cursor: ::

   with Environment.manage():  # class function
       env = Environment(cr, uid, context)

New ids
=======

When creating a record a model with computed fields, the records of the recordset will be in memory only.
At that time the `id` of the record will be a dummy ids of type :py:class:`openerp.models.NewId`

So if you need to use the record `id` in your code (e.g. for a sql query) you should check if it is available: ::

   if isinstance(current_record.id, models.NewId):
       # do your stuff
