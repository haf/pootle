# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

import pytest


@pytest.mark.django_db
def test_views_bad(bad_views):
    path, response, test = bad_views
    assert response.status_code == test["code"]
    for k, v in test.items():
        if k == "code":
            continue
        if k == "location":
            if test['location'] is None:
                location = None
            else:
                location = "http://testserver/%s" % test["location"].lstrip("/")
            assert response.get("location") == location
        else:
            assert response.get(k) == v
