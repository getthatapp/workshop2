import hashlib
import random
import string

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generateSalt():
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        salt += random.choice(ALPHABET)
    return salt


def hashPassword(password, salt=None):
    """
    Hashes the password with salt as an optional parameter.

    If salt is not provided, generates random salt.
    If salt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.

    :param str password: password to hash
    :param str salt: salt to hash, default None

    :rtype: str
    :return: hashed password
    """

    # generate salt if not provided
    if salt is None:
        salt = generateSalt()

    # fill to 16 chars if too short
    if len(salt) < 16:
        salt += ("a" * (16 - len(salt)))

    # cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    # use sha256 algorithm to generate haintegersh
    tSha = hashlib.sha256()

    # we have to encode salt & password to utf-8, this is required by the
    # hashlib library.
    tSha.update(salt.encode('utf-8') + password.encode('utf-8'))

    # return salt & hash joined
    return salt + tSha.hexdigest()


def checkPassword(passToCheck, hashed):
    """
    Checks the password.
    The function does the following:
        - gets the salt + hash joined,
        - extracts salt and hash,
        - hashes `pass_to_check` with extracted salt,
        - compares `hashed` with hashed `pass_to_check`.
        - returns True if password is correct, or False. :)

    :param str passToCheck: not hashed password
    :param str hashed: hashed password

    :rtype: bool
    :return: True if password is correct, False elsewhere
    """

    # extract salt
    salt = hashed[:16]

    # extract hash to compare with
    hashToCheck = hashed[16:]

    # hash password with extracted salt
    newHash = hashPassword(passToCheck, salt)

    # compare hashes. If equal, return True
    if newHash[16:] == hashToCheck:
        return True
    else:
        return False



