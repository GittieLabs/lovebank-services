''' pytests for models.py '''

class TestDB:
    # Test User Model
    def test_User(new_user):
    '''
    GIVEN a User model
    WHEN a new User is created
    THEN check fields are defined correctly
    '''
        assert new_user.email == 'ann@test.com'
        assert new_user.username == 'Ann'
