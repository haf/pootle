#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pootle.settings'

from optparse import make_option

from django.core.management.base import BaseCommand

from pootle.core.models import Revision


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--restore',
            action='store_true',
            default=False,
            dest='restore',
            help='Restore the current revision number from the DB.',
        ),
    )

    help = "Print the number of the current revision."

    def handle(self, **options):
        if options['restore']:
            from pootle_store.models import Unit
            Revision.set(Unit.max_revision())

        self.stdout.write('%s' % Revision.get())
