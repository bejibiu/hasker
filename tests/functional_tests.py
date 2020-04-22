from base64 import b64decode

from django.utils.baseconv import base64
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


class TestProfilePage:
    def test_profile_page_title(self, browser, profile_page):
        assert "Settings" in browser.title
        assert "Settings" in browser.find_element_by_class_name("name-page").text

    def test_change_email(self, browser, profile_page):
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
    """
+    Страница вопроса со списĸом ответов. На странице вопроса можно добавить ответ.
    Ответы сортируются по рейтингу и дате добавления при равном рейтинге. Ответы разбиваются по 30 штуĸ на странице.

+    Форма добавления ответа находится на странице вопроса. Отображается тольĸо для авторизованных пользователей.
        После добавления ответа, автор вопроса должен получить email с уведомление от новом ответе.
            В этом письме должна быть ссылĸа для перехода на страницу вопроса.
        Автор вопроса может пометить один из ответов ĸаĸ правильный.
        Пользователи могут голосовать за вопросы
         и ответы с помощью лайĸов «+» или «–».
         Один пользователь может голосовать за 1 вопрос и ответ тольĸо 1 раз,
         однаĸом может отменить свой выбор или переголосовать неограниченное число раз.
    """

    def test_not_form_for_not_auth_client(self, browser, user, client, question_page):
        with pytest.raises(NoSuchElementException):
            browser.find_element_by_id('answer-form')
        func_login(browser, user)
        assert browser.find_element_by_id("answer-form")

    def test_send_answer(self, browser, auth_session, question_page):
        browser.find_element_by_name('text').send_keys('this is answer')
        browser.find_element_by_id('send_answer_btn').click()
        assert (
                "Answer saved successfully"
                in browser.find_element_by_class_name("alert-success").text
        )
        browser.find_element_by_class_name('answer')
