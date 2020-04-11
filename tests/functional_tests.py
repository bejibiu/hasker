from selenium import webdriver
import pytest


@pytest.fixture
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def home_page():
    return "http://127.0.0.1:8000"


class TestHomePage:
    def test_home_page_title(self, browser, home_page):
        browser.get(home_page)
        assert "Hasker" in browser.title
        assert "Hasker" in browser.find_element_by_tag_name("h1").text
        assert "questions" in browser.find_element_by_tag_name("h2").text
        assert "no question" in browser.find_elements_by_id("list_question").text
        assert browser.find_elements_by_name("search")
