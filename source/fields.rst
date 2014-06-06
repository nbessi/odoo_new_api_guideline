 Fields
========

Now fields are class property.
It uses Python property mechanins under the hoods: ::
  # import to do
  name = Char()

Fields types
------------

Char
####

Integer
#######

Float
#####

Date/Datetime
#############
Helper to convert to real date available.
srt_to_datetime, str_to_date

Name conflicts
--------------
!! fields anf method name can conflict.

When you call an record as a dict it will force to look on the columns.

Fields name
-----------

If string is not passed name of attrubute will be used and Capitalized.


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

Computed fields
---------------
There is no more direct creation of fields.function.

Instead you add a compute key. the value is the name of the function as a string.
This allows to have fields definition atop of class.

The signature of the function is self.


Older attibute are kept

Also all result are stored in a cache so when accessing again cache should be used: ::

@api.one
@api.depends('name', parent_id)
_display_name(self):
  """Self represent the record set to workon
  """
  names = [self.parent_id.name, self.name]

The function can be void.
It should modifiy record property in order to be written to the cache: ::
  self.name = new_value

If you need to do bulk change for performance you can remove
the @api.one decorator and do bulk write.

Inverse
-------

The inverse key allows to trigger call of the function
When the fields is written/"created"


Multi fields
------------
To have one function that compute multiples values
@api.multi
@api.depends('field.relation', 'an_otherfields.relation' )
def _amount(self):
   for x in self:
     x.total = an_algo
     x.untaxed = an_algo

Cache is invalidated and all updated fields are updated at the end.


Related field
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

!! When updating an related field translation not all
translation for related field are yet translated if field
is stored

Chain related fields modification will trigger invalidation of the cache
for all element of the chain
