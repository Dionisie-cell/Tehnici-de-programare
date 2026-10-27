import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return host.strip("/") + ("/") + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if url.startwith("https://"):
        return "True"
    else:
        return "False"


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    raspuns = requests.get(url)
    return(raspuns.status_code(url), raspuns.show_response(url))


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    raspuns = requests.get(url)
    return (f"{raspuns.status_code}, {raspuns.content_type}, {raspuns.length}, {raspuns.server}")

def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    try:
        raspuns = requests.get(SITES)
        raspunsstatus= raspuns.raise_for_status
        if(raspunsstatus == 200):
            return(SITES)
    except requests.exceptions.HTTPError:
            return 0


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
