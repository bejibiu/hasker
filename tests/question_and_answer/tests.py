
def test_home_page(client):
    res = client.get('/')
    elements_by_id_on_home_page = [
        'logo',
        'search',
        'user_block',
        'signin',
        'regestry'
    ]

    res = (res.content).decode()

    for element in elements_by_id_on_home_page:
        assert element in res
