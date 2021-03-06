#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestAccounts():

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login_with_user(user="default")
        Assert.false(home_page.footer.is_login_visible)
        Assert.true(home_page.is_featured_section_visible)

        settings_page = home_page.header.click_settings()

        Assert.equal(settings_page.email_text, mozwebqa.credentials["default"]["email"])

        home_page = settings_page.click_logout()
        home_page.wait_for_ajax_on_page_finish()
        Assert.true(home_page.footer.is_login_visible)

    @pytest.mark.nondestructive
    def test_user_can_click_back_from_settings_page(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=795185#c11
        """
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        home_page.login_with_user(user="default")
        Assert.false(home_page.footer.is_login_visible)

        settings_page = home_page.header.click_settings()
        Assert.equal(settings_page.email_text, mozwebqa.credentials["default"]["email"])

        settings_page.click_apps()
        Assert.equal("Apps", settings_page.selected_settings_option)

        settings_page.header.click_back()
        Assert.true(home_page.is_featured_section_visible)
