import re
import time
from base64 import b64decode

from django.core import mail
from selenium import webdriver
import pytest
from selenium.common.exceptions import NoSuchElementException

from question_and_answer.models import Question


@pytest.fixture(scope="session")
def browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def home_page(browser, live_server):
    return browser.get(live_server.url)


@pytest.fixture
def auth_session(browser, live_server, user):
    page = browser.get(live_server.url)
    func_login(browser, user)
    return page


@pytest.fixture
def profile_page(browser, live_server, user):
    browser.get(live_server.url)
    func_login(browser, user)
    return browser.get(live_server.url + "/account/settings/")


@pytest.fixture
def question_page(browser, live_server, question):
    return browser.get(live_server.url + question.get_absolute_url())


@pytest.fixture
def avatar_img(tmpdir):
    avatar_path = tmpdir.mkdir("avatar").join("avatar.gif")
    with open(avatar_path, 'wb')as f:
        f.write(b64decode(
            b"R0lGODlhEAAQANU/APXRACIeJyUhLEM8T/zyAPvtAPrpAPnmAPjiAPjfADw1RvPKAPPIAFBHXv30ACsmMvXUAO+5AB0aI/33APjdAPHDAEU+UTgyQllPaQsJDR8cJTUvPvLHAP75AEhAVPC+ADYwP/fbAE5FW/78ADMuPPHBAFtQaf76AH5wlBcVG5mJtG1hgExDWY19pf/9APbXAE9GXUA5S/TNAPbYAP34APjgAC8qN1VMZPPLAP79AElBVktCVzErOVFIX////////yH5BAEAAD8ALAAAAAAQABAAAAanwJ/w1ysOj8jeiEboIZ89V8fhfB6jJ6r1OupUrSqVL3eaFBsNmIjlGfxaLV9nQigcaqG1Tra4oFA+DnUGCBQYEAAWCxwkKys+BQYHhRg9ADI4CiA2JiY+kwkhN4gWMRwcJQ8eHj6hMxA7AzgMHBs8Dz8gID4viAMLDCAbJSUfAj8CAj6XOBckxB8PyUIpKT4xFxXFyRHdGkIZGT5C0gEaGhLpQ+FbT0EAOw=="))
    return avatar_path


def func_login(browser, user):
    logout(browser)

    browser.find_element_by_id("login_btn").click()

    browser.find_element_by_id("login_username").send_keys(user.username)
    browser.find_element_by_id("login_password").send_keys('very_Strong_password!@# Z')

    browser.find_element_by_name("send_login_form").click()


def logout(browser):
    try:
        browser.find_element_by_id('logout').click()
    except NoSuchElementException:
        pass


class TestHomePage:
    def test_home_page_title(self, browser: webdriver.Firefox, home_page):
        assert "Hasker" in browser.title
        assert "Hasker" in browser.find_element_by_tag_name("h1").text
        assert browser.find_elements_by_id("search")
        assert "No question" in browser.find_element_by_id("list_question").text

    def test_registration(self, browser, home_page, avatar_img):
        btn_sign_up = browser.find_element_by_id("sign_up_btn")
        btn_sign_up.click()

        browser.find_element_by_name("username").send_keys("new_login")
        browser.find_element_by_name("email").send_keys("new_user@mail.com")
        browser.find_element_by_name("password1").send_keys("new_user@mail.com")
        browser.find_element_by_name("password2").send_keys("new_user@mail.com")
        browser.find_element_by_name("avatar").send_keys(avatar_img.strpath)
        browser.find_element_by_name("send_signup_form").click()
        assert (
                "success sign up"
                in browser.find_element_by_class_name("alert-success").text
        )
        ### After sign up user already login and see button logout
        assert "new_login" == browser.find_element_by_id('profile').text
        assert browser.find_element_by_id('logout')
        assert browser.find_element_by_class_name('avatar')

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

    def test_page_has_popular_question(self, browser, question_30, home_page):
        assert browser.find_element_by_class_name("popular-questions")
        assert len(browser.find_elements_by_class_name('popular-question')) == 20


class TestProfilePage:
    def test_profile_page_title(self, browser, profile_page):
        assert "Settings" in browser.title
        assert "Settings" in browser.find_element_by_class_name("name-page").text

    def test_change_email(self, browser, profile_page):
        browser.find_element_by_name('email').clear()
        browser.find_element_by_name('email').send_keys('newemail@test.com')
        browser.find_element_by_id('send_settings_form_btn').click()
        assert (
                "Success update"
                in browser.find_element_by_class_name("alert-success").text
        )


class TestHomePageQuestion:
    def test_not_available_button_ask_if_user_not_auth(self, browser, home_page, user):
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_id('ask_btn')
        func_login(browser, user)
        assert browser.find_element_by_id('ask_btn')

    def test_save_ask_question(self, browser, auth_session):
        browser.find_element_by_id('ask_btn').click()

        browser.find_element_by_name("title").send_keys("New Question")
        browser.find_element_by_name("text").send_keys("This is text question?")
        browser.find_element_by_name("send_ask_btn").click()

        assert (
                "Ask saved successfully"
                in browser.find_element_by_class_name("alert-success").text
        )
        browser.find_element_by_class_name('question').click()
        assert "/question/" in browser.current_url


class TestQuestionAndAnswer:

    def test_not_form_for_not_auth_client(self, browser, user, client, question_page):
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_id('answer-form')
        func_login(browser, user)
        assert browser.find_element_by_id("answer-form")

    def test_send_answer(self, browser, auth_session, user, question_page):
        browser.find_element_by_name('text').send_keys('this is answer')
        browser.find_element_by_id('send_answer_btn').click()
        assert (
                "Answer saved successfully"
                in browser.find_element_by_class_name("alert-success").text
        )
        browser.find_element_by_class_name('answer')
        email = mail.outbox[0]
        assert user.email in email.to
        assert email.subject == 'YOU GOT AN ANSWER'
        assert 'Use this link to you\'r answer' in email.body
        url_search = re.search(r'http://.+/.+$', email.body)
        assert url_search
        url = url_search.group(0)
        browser.get(url)
        browser.find_element_by_class_name('answer')

    def test_add_votes_to_question(self, browser, auth_session, question_page):
        browser.find_element_by_id('up_question').click()
        assert browser.find_element_by_id('votes-question').text == "1"
        browser.find_element_by_id('up_question').click()
        assert browser.find_element_by_id('votes-question').text == "0"
        browser.find_element_by_id('down_question').click()
        assert browser.find_element_by_id('votes-question').text == "-1"
        browser.find_element_by_id('down_question').click()
        assert browser.find_element_by_id('votes-question').text == "0"

    def test_add_votes_to_answer(self, browser, auth_session, answers, question_page):
        browser.find_element_by_id(f'answer-{answers[0].pk}-up').click()
        assert browser.find_element_by_id(f'votes-answer-{answers[0].pk}').text == "1"
        browser.find_element_by_id(f'answer-{answers[0].pk}-up').click()
        assert browser.find_element_by_id(f'votes-answer-{answers[0].pk}').text == "0"
        browser.find_element_by_id(f'answer-{answers[0].pk}-down').click()
        assert browser.find_element_by_id(f'votes-answer-{answers[0].pk}').text == "-1"
        browser.find_element_by_id(f'answer-{answers[0].pk}-down').click()
        assert browser.find_element_by_id(f'votes-answer-{answers[0].pk}').text == "0"
        browser.find_element_by_id(f'answer-{answers[0].pk}-up').click()
        browser.find_element_by_id(f'answer-{answers[1].pk}-up').click()
        assert browser.find_element_by_id(f'votes-answer-{answers[0].pk}').text == "0"
        assert browser.find_element_by_id(f'votes-answer-{answers[1].pk}').text == "1"

    def test_set_answer_as_right(self, browser, auth_session, answers, question_page):
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_class_name('right-answer')
        browser.find_element_by_id(f'toggle-right-answer-{answers[0].pk}').click()
        assert browser.find_element_by_class_name('right-answer')

    def test_set_all_answer_as_right(self, browser, auth_session, answers, question_page):
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_class_name('right-answer')
        browser.find_element_by_id(f'toggle-right-answer-{answers[0].pk}').click()
        assert browser.find_element_by_id(f'grade-{answers[0].pk}')
        assert browser.find_element_by_class_name('right-answer')
        browser.find_element_by_id(f'toggle-right-answer-{answers[0].pk}').click()
        assert browser.find_element_by_id(f'no-grade-{answers[0].pk}')

    def test_paginate(self, browser, auth_session, answers_two_page, question_page):
        assert browser.find_element_by_link_text('2')
        browser.find_element_by_link_text('2').click()
        assert '?page=2' in browser.current_url


class TestSearchPage:
    def test_empty_search_result(self, browser, home_page):
        browser.find_element_by_id('search-input').send_keys('_NoResult')
        browser.find_element_by_id('search-btn').click()
        assert 'search?q=' in browser.current_url
        assert "No question" in browser.find_element_by_id("list_question").text

    def test_search_question(self, browser, question_30, home_page):

        browser.find_element_by_id('search-input').send_keys(f'{question_30[-1].text}')
        browser.find_element_by_id('search-btn').click()
        assert 'search?q=' in browser.current_url
        assert f"{question_30[-1].title}" in browser.find_element_by_id("list_question").text
        assert f"{question_30[-2].title}" not in browser.find_element_by_id("list_question").text

    def test_paginate_search_result(self, browser, question_30, home_page):
        browser.find_element_by_id('search-input').send_keys("This unique")
        browser.find_element_by_id('search-btn').click()
        assert 'search?q=' in browser.current_url
        browser.find_element_by_id('page-2-id').click()
        assert '?page=2' in browser.current_url
        assert browser.find_element_by_link_text("This unique 20 question")

    def test_sorted(self, browser, question_30, home_page, user):
        browser.find_element_by_id('search-input').send_keys("This unique")
        browser.find_element_by_id('search-btn').click()
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_link_text("This unique 20 question")
        Question.objects.get(title="This unique 20 question").votes_up.add(user)
        browser.refresh()
        assert browser.find_element_by_link_text("This unique 20 question")

    def test_get_by_tags(self, browser, question, tag, home_page):
        browser.find_element_by_id('search-input').send_keys(f"tag:{tag.label}")
        browser.find_element_by_id('search-btn').click()
        assert browser.find_element_by_link_text("Title")

    def test_click_on_tag_go_to_search(self, browser, question, tag, home_page):
        browser.find_element_by_link_text(f"{tag.label}").click()
        assert 'search' in browser.current_url
