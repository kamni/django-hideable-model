# django-disabled-model

This Django app provides a model manager and admin interfaces that can be used
work with models that should be hidden or disabled instead of deleted. When
using a disabled model, the normal Django query 'get' and 'filter' methods will
not return any disabled objects, so you can run normal queries without worrying
about whether you have forgotten to exclude the objects with the disabled flag
set. You can include the disabled objects at any time in a query by passing the
flag 'include_disabled=True' for 'get' and 'filter.

This Django app also includes a ModelAdmin class that can be subclassed to
work with disabled objects. By default, disabled objects will only show up in
the admin for superusers, but normal staff Django users will not see them.
Deleting the objects as a superuser acts as expected, but deleting as a staff
user will simply disable the object so that it can be recovered at any time by
a superuser admin.

## Installation

TODO: write

## Setup

This app does not have any Django models that need to be created in the
database, so it does not need to be added to INSTALLED_APPS in your settings.py
file.

## Usage

TODO: write