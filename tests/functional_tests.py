from selenium import webdriver
import pytest


@pytest.fixture(scope="class")
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def home_page(browser):
    return browser.get("http://127.0.0.1:8000")


class TestHomePage:
    def test_home_page_title(self, browser: webdriver.Firefox, home_page):
        assert "Hasker" in browser.title
        assert "Hasker" in browser.find_element_by_tag_name("h1").text
        assert browser.find_elements_by_id("search")
        assert "No question" in browser.find_element_by_id("list_question").text

    def test_registration(self, browser, home_page):
        btn_sign_up = browser.find_element_by_id("sign_up_btn")
        btn_sign_up.click()

        assert not browser.find_element_by_name("send_signup_form").is_enabled()
        browser.find_element_by_name("login").send_keys("new_login")
        browser.find_element_by_name("email").send_keys("new_user@mail.com")
        browser.find_element_by_name("password").send_keys("new_user@mail.com")
        browser.find_element_by_name("password-repeater").send_keys("new_user@mail.com")
        browser.find_element_by_name("send_signup_form").click()

        assert (
            "success sign up"
            in browser.find_element_by_class_name("alert-success").text()
        )
