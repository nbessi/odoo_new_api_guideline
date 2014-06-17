Introspection
=============
A common pattern in OpenERP was to do Model fields introspection using ``_columns`` property.
From 8.0 ``_columns`` is deprecated by ``_fields`` that contains list of consolidated fields
instantiated using old or new API.
