from common_models.pwd_context import get_password_hash, pwd_context


def test_get_password_hash():
    password = "securepassword123"
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password.startswith("$2b$")
    assert len(hashed_password) > len(password)


def test_hash_uniqueness():
    password = "mypassword"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    assert hash1 != hash2


def test_password_hash_verification():
    password = "supersecret"
    hashed_password = get_password_hash(password)
    assert pwd_context.verify(password, hashed_password)
