from http.cookiejar import MozillaCookieJar
from http.cookiejar import Cookie

# File jisme cookies save hongi
cookie_jar = MozillaCookieJar("cookies.txt")

# Ek dummy cookie create kar rahe hain
cookie = Cookie(
    version=0,
    name='sessionid',
    value='abcd1234',
    port=None,
    port_specified=False,
    domain='.example.com',
    domain_specified=True,
    domain_initial_dot=True,
    path='/',
    path_specified=True,
    secure=False,
    expires=None,
    discard=True,
    comment=None,
    comment_url=None,
    rest={'HttpOnly': None},
    rfc2109=False
)

# Cookie add karke save karo
cookie_jar.set_cookie(cookie)
cookie_jar.save(ignore_discard=True, ignore_expires=True)


  
