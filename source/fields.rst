Fields
======

Now fields are class property.
It uses Python property under the hoods: ::

    from openerp import models, fields


    class AModel(models.Model):

    _name = 'a_name'

    name = fields.Char(
        string="Name",                   #  Optional label of the field
        compute="_compute_name_custom",  #  Transform the fields in computed fields
        store=True,                      #  If computed it will store the result
        select=True,                     # Force index on field
        readonly=True,                   # Field will be readonly in views
        inverse="_write_name"            #  On update trigger
        required=True,                   #  Mandatory field
        translate=True,                  #  Translation enable
        help='blabla',                   #  Help tooltip text
        company_dependent=True,          #  Transform columns to ir.property
    )

   # the string key is not mandatory
   # by default it wil use the property name Capitalized

  name = fields.Char()  #  Valid definition


.. _fields_inherit:

Fields inheritance
------------------

One of the new feature of the API is to be able to change only an attribute of the fields: ::

   name = fields.Char(string)

Fields types
------------

Boolean
#######

Boolean type field: ::

    abool = fields.Boolean()

Char
####

Store string with variable len.: ::

    achar = fields.Char()


Specific options:

 * size: data will be trimmed to sepcified size
 * translate: fields can be translated


Integer
#######

Store integer value. No null value support. If value not set it returns 0: ::

    anint = fields.Integer()

Float
#####

Store float value. No null value support. If value not set it returns 0.0
If digits option is set it will use numeric type: ::


    aflaot = fields.Float()
    aflaot = fields.Float(digits=(32, 32))
    aflaot = fields.Float(digits=lambda cr: (32, 32))

Specific options:

  * digits: force use of numeric type on database. parameter can be a tuple (int len, float len) or a callable that return a tuple and take a cursor as parameter

Date
####

Store date.
The field provide some helper:

  * context_today  returns current day date string based on tz
  * today return current system date string
  * from_string returns datetime.date() from string
  * to_string retruns date string from datetime.date

: ::

    from openerp import fields

    adate = fields.Date()
    fields.Date.today()
    >>> '2014-06-15'
    fields.Date.context_today(self)
    >>> '2014-06-15'
    fields.Date.context_today(self, timestamp=datetime.datetime.now())
    >>> '2014-06-15'
    fields.Date.from_string(fields.Date.today())
    >>> datetime.datetime(2014, 6, 15, 19, 32, 17)
    fields.Datetime.to_string(datetime.datetime.today())
    >>> '2014-06-15'

DateTime
########

Store datetime.
The field provide some helper:

  * context_timestamp  returns current day date string based on tz
  * now return current system date string
  * from_string returns datetime.date() from string
  * to_string retruns date string from datetime.date

: ::

    fields.Datetime.context_timestamp(self, timestamp=datetime.datetime.now())
    >>> datetime.datetime(2014, 6, 15, 21, 26, 1, 248354, tzinfo=<DstTzInfo 'Europe/Brussels' CEST+2:00:00 DST>)
    fields.Datetime.now()
    >>> '2014-06-15 19:26:13'
    fields.Datetime.from_string(fields.Datetime.now())
    >>> datetime.datetime(2014, 6, 15, 19, 32, 17)
    fields.Datetime.to_string(datetime.datetime.now())
    >>> '2014-06-15 19:26:13'


Binary
######

Store file in bytea format: ::

    abin = fields.Binary()

Selection
#########

Store text in database but propose a selection widget.
It induces no selection constraint in database.
Selection must be set as a list of tuples or a callable that returns a list of tuples: ::

    aselection = fields.Selection([('a', 'A')])
    aselection = fields.Selection(selection=[('a', 'A')])
    aselection = fields.Selection(selection='a_function_name')

Specific options:

  * selection: a list of tuple or a callable name that take recordset as input

Reference
#########

Store an arbitrary reference to a model and a row: ::

    aref = fields.Reference([('model_name', 'String')])
    aref = fields.Reference(selection=[('model_name', 'String')])
    aref = fields.Reference(selection='a_function_name')

Specific options:

  * selection: a list of tuple or a callable name that take recordset as input


Many2one
########

Store a relation against a co-model: ::

    arel_id = fields.Many2one('res.users')
    arel_id = fields.Many2one(comodel_name='res.users')

Specific options:

  * comodel_name: name of the opposite model

One2many
########

Store a relation against many rows of co-model: ::

    arel_ids = fields.One2many('res.users', 'rel_id')
    arel_ids = fields.One2many(comodel_name='res.users', inverse_name='rel_id')

Specific options:

  * comodel_name: name of the opposite model
  * inverse_name: relational column of the opposite model


Many2many
#########

Store a relation against many 2 many rows of co-model: ::

    arel_ids = fields.Many2many('res.users')
    arel_ids = fields.Many2many(comodel_name='res.users',
                                relation='table_name',
                                column1='col_name',
                                column2='other_col_name')


Specific options:

  * comodel_name: name of the opposite model
  * relation: relational table name
  * columns1: relational table left column name
  * columns2: relational table right column name


Name Conflicts
--------------
!! fields and method name can conflict.

When you call an record as a dict it will force to look on the columns.


Fields Defaults
---------------

Default is now a keyword of a field:

You can attribute it a value or a function

::

   name = fields.Char(default='A name')
   # or
   name = fields.Char(default=a_fun)

   #...
   def a_fun(self):
      return self.do_something()

Using a fun will force you to define function brfore fields definition.




Computed Fields
---------------
There is no more direct creation of fields.function.

Instead you add a `compute` key. the value is the name of the function as a string.
This allows to have fields definition atop of class: ::

    class AModel(models.Model):
        _name = 'a_name'

        computed_total = fields.Float(compute='compute_total')

        def compute_total(self):
            ...
            self.computed_total = x


The function can be void.
It should modifiy record property in order to be written to the cache: ::
  self.name = new_value

Be aware that this assignation will trigger a write into the database.
If you need to do bulk change or must be carful about performance.
You should do classic call to write


Inverse
-------

The inverse key allows to trigger call of the function
When the fields is written/"created"


Multi Fields
------------
To have one function that compute multiples values: ::

    @api.multi
    @api.depends('field.relation', 'an_otherfields.relation' )
    def _amount(self):
       for x in self:
         x.total = an_algo
         x.untaxed = an_algo


Related Field
-------------

There is not anymore related fields.related type.

Instead you just set the name argument related to your model: ::

  participant_nick = field.Char(string='Nick name',
                                related='partner_id.name')

The type field named arg is not needed anymore.

Setting the store key word will store the value
and from now the value of the related fields will be autmatically
updated. sweet. ::

  participant_nick = field.Char(string='Nick name',
                                store=True,
                                related='partner_id.name')

!! When updating any related field not all
translations of related field are yet translated if field
is stored!!

Chain related fields modification will trigger invalidation of the cache
for all elements of the chain


Property Field
--------------

There is some use cases where value of the fields must change depending of
the current company.

To activate such behavior you can now use the `company_depending` option.

A notable evolution in new API is that "property fields" are now searchable

WIP copyable option
-------------------

There is a dev running that will prevent to redefine copy by simply
setting an copyable option on fields. It has not yet landed in new API: ::

  copyable=False  # !! WIP to prevent redefine copy
