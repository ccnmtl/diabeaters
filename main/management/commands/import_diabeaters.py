from diabeaters.main.exportimport import import_zip
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from optparse import make_option
from textwrap import dedent
from zipfile import ZipFile

DEFAULT_PATH = "pagetree.zip"

@transaction.commit_manually
def import_zipfile(zipfile):
    hierarchy = import_zip(zipfile)
    transaction.commit()
    return hierarchy

class Command(BaseCommand):

    args = "[import_zipfile]"

    help = dedent("""
           Import default site content for Diabeaters.

           You should provide the path to a zipfile containing the exported site content.
           If run with no arguments, it will assume the content is in a default location.
           """).strip()

    def handle(self, *args, **options):
        args = args or (DEFAULT_PATH,)
        path = args[0]
        zipfile = ZipFile(path)
        hierarchy = import_zipfile(zipfile)
        print "Successfully imported content, now you can start the server and visit the site"
