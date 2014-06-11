Compatibility specificities
============================
working on self will use Recordset.
But there is a special object that is the old model.

self.pool
self._model

will use old model

self
self.env

will call recodset.

@return
=======
@model
=======

Migrating code
--------------

fields shoul dbe on the top
first migrate columns and then function
