from selenium import webdriver
import pytest
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture(scope="class")
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def home_page(browser, live_server):
    return browser.get(live_server.url)


@pytest.fixture
def profile_page(browser, live_server, user):
    browser.get(live_server.url)
    func_login(browser, user)
    return browser.get(live_server.url + "/account/settings/")


def func_login(browser, user):
    try:
        browser.find_element_by_id('logout').click()
    except NoSuchElementException:
        pass

    browser.find_element_by_id("login_btn").click()

    browser.find_element_by_id("login_username").send_keys(user.username)
    browser.find_element_by_id("login_password").send_keys('very_Strong_password!@# Z')

    browser.find_element_by_name("send_login_form").click()


class TestHomePage:
    def test_home_page_title(self, browser: webdriver.Firefox, home_page):
        assert "Hasker" in browser.title
        assert "Hasker" in browser.find_element_by_tag_name("h1").text
        assert browser.find_elements_by_id("search")
        assert "No question" in browser.find_element_by_id("list_question").text

    def test_registration(self, browser, home_page):
        btn_sign_up = browser.find_element_by_id("sign_up_btn")
        btn_sign_up.click()

        browser.find_element_by_name("username").send_keys("new_login")
        browser.find_element_by_name("email").send_keys("new_user@mail.com")
        browser.find_element_by_name("password1").send_keys("new_user@mail.com")
        browser.find_element_by_name("password2").send_keys("new_user@mail.com")
        browser.find_element_by_name("send_signup_form").click()
        assert (
                "success sign up"
                in browser.find_element_by_class_name("alert-success").text
        )
        ### After sign up user already login and see button logout
        assert browser.find_element_by_id('logout')
        browser.find_element_by_id('logout').click()

    def test_login(self, browser, home_page, user):
        browser.find_element_by_id("login_btn").click()

        browser.find_element_by_id("login_username").send_keys(user.username)
        browser.find_element_by_id("login_password").send_keys('very_Strong_password!@# Z')

        browser.find_element_by_name("send_login_form").click()
        assert browser.find_element_by_id('logout')
        browser.find_element_by_id('logout').click()

    def test_logout(self, browser, home_page, user):
        func_login(browser, user)
        assert browser.find_element_by_id('logout')

        browser.find_element_by_id('logout').click()

        assert browser.find_element_by_id('login_btn')


class TestProfilePage:
    def test_profile_page_title(self, browser, profile_page):
        assert "Settings" in browser.title
        assert "Settings" in browser.find_element_by_class_name("name-page").text

    def test_change_email(self, browser, profile_page):
        browser.find_element_by_name('email').send_keys('newemail@test.com')
        browser.find_element_by_id('send_settings_form_btn').click()
        assert "newemail@test.com" in browser.find_element_by_name('email').text
