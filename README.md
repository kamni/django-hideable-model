# django-model-ninja

[Note: this project is still in development and has not even reached alpha.
Please expect complete overhauls between versions]

This Django library provides a model manager and admin interfaces that can be
used to work with models that should be hidden or disabled instead of deleted.
This particular functionality may be useful for applications where you have
users that want to delete objects, but may need to undo the deletion or recover
them at a later time, but as a developer you want to minimize bugs related to
remembering to hide those pseudo-deleted objects from users.

When using a hidden model, the normal Django query 'get' and 'filter' methods
will not return any disabled objects, so you can run normal queries without
worrying about whether you have forgotten to exclude the objects with the
disabled flag set. You can include the disabled objects at any time in a query
by passing the flag 'include_disabled=True' for 'get' and 'filter.

This Django app will eventually include two ModelAdmin classes that can be
subclassed to work with disabled objects. In the first ModelAdmin, disabled
objects will only show up in the admin for superusers, but normal staff Django
users will not see them. Deleting the objects as a superuser acts as expected,
but deleting as a staff user will simply disable the object so that it can be
recovered at any time by a superuser admin. In the second ModelAdmin, both
staff and superusers can see and delete hidden objects normally.

[Currently the admin interface will not show disabled models and does not
handle all validation gracefully]

## Installation

The easiest way to get the latest stable version is to simply do:

    pip install django-model-ninja

For developers wanting to work with the most recent code:

    pip install -e git+https://github.com/kamni/django-hideable-model.git#egg=master

## Setup

These libraries do not have any Django models that need to be created in the
database for normal usage, so it does not need to be added to INSTALLED_APPS in
your settings.py file if you only want to use this in your project.

If you want to run the tests for this app, please include it in INSTALLED_APPS
so the test models get created.

## Usage

These libraries contain a model class that can be imported that automatically
includes the correct obje