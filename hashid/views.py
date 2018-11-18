from django.shortcuts import render
from django.http import HttpResponseRedirect

import re
import wikipedia
import urllib

from .forms import HashForm

# List of the known hash algorithms of this script
hash_algorithms = {
    'MD2': re.compile(r'^(\$md2\$)?[a-f0-9]{32}$', re.IGNORECASE),
        # 27454d000b8f9aaa97da6de8b394d986
    'Bcrypt (SHA-256)': re.compile(r'^\$bcrypt-sha256\$(2[axy]|2)\,[0-9]+\$[a-z0-9\/.]{22}\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        # $bcrypt-sha256$2a,12$LrmaIX5x4TRtAwEfwJZa1.$2ehnw6LvuIUTM0iz4iz9hTxv21B6KFO
    'Fairly Secure Hashed Password': re.compile(r'^{FSHP[0123]\|[0-9]+\|[0-9]+}[a-z0-9\/+=]+$', re.IGNORECASE),
        # {FSHP1|16|480000}i1GqlXIuxThHCOFcC6FUKmtHXnGkdqCXJZHLbEPpRpeWLwV+czhOcOoQSthWRudL
    'RIPEMD-320': re.compile(r'^[a-f0-9]{80}$', re.IGNORECASE),
        # eb0cf45114c56a8421fbcb33430fa22e0cd607560a88bbe14ce70bdf59bf55b11a3906987c487992
    'Cisco Type 7': re.compile(r'^[a-f0-9]{4,}$', re.IGNORECASE),
        # 140713181F13253920
    'Cisco-ASA (MD5)': re.compile(r'^[a-z0-9\/.]{16}([:$].{1,})?$', re.IGNORECASE),
        # NuLKvvWGg.x9HEKO
    'PostgreSQL MD5': re.compile(r'^md5[a-f0-9]{32}$', re.IGNORECASE),
        # md523b431acfeb41e15d466d75de822307c
    'PBKDF2-SHA1': re.compile(r'^\$pbkdf2(-sha1)?\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{27}$', re.IGNORECASE),
        # $pbkdf2$131000$WkR6UEU0NUM$.L1L.AVXTBSsc0FuHRQz4PNMVXc
    'PBKDF2-SHA256': re.compile(r'^\$pbkdf2-sha256\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        # '$pbkdf2-sha256$29000$WkR6UEU0NUM$pd1VbFkOA/VwbhJZhJ.25kHPsKVXika2XsuKYoudcug'
    'PBKDF2-SHA512': re.compile(r'^\$pbkdf2-sha512\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        # $pbkdf2-sha512$25000$WkR6UEU0NUM$S.ymDjKjwM9XaQsofRC6KX1s.pQvZvVmMxdrrLi16pCazREoyJGxe8.Tn6Zhi3S0B6H6rcrxITllAEo3rDwBng
    'MS SQL 2000': re.compile(r'^0x0100[a-f0-9]{88}$', re.IGNORECASE),
        # 0x01006EED7DAFD5917DB47D0B735192DFC78F41C18D938EF2C9CAFE1DB1DEA402D32506FB7BA82AFE9C14CB1493EC
    'Sun MD5 Crypt': re.compile(r'^(\$md5,rounds=[0-9]+\$|\$md5\$rounds=[0-9]+\$|\$md5\$)[a-z0-9\/.]{0,16}(\$|\$\$)[a-z0-9\/.]{22}$', re.IGNORECASE)
        # $md5,rounds=34000$ZDzPE45C$$RGKsbBUBhidHsaNDUMEEX0
}

# Get description of the algorithm from its Wikipedia page
def wiki_desc(algorithm):
    try:
        return wikipedia.summary(algorithm, sentences=2)
    except wikipedia.exceptions.DisambiguationError as err:
        list = f'"{algorithm}" may refer to:\n'
        for option in err.options:
            list += f'- {option}\n'
        return list
    except wikipedia.exceptions.PageError:
        return 'Sorry, but no Wikipedia page was found.'

def index(request):
    if request.method == 'POST':
        form = HashForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f"/hashid/{request.POST['value']}")
    else:
        form = HashForm()
    return render(request, 'hashid/index.html', { 'form': form })

def show(request, hash_value):
    result = find_algorithm(hash_value)
    return render(request, 'hashid/show.html', {
        'algorithm': result[0],
        'wiki_desc': result[1]
    })

def find_algorithm(hash_value):
    match = False
    for name, regex in hash_algorithms.items():
        if regex.match(urllib.parse.unquote(hash_value)):
            match = True
            return [name, wiki_desc(name)]
    if match == False:
        return ['Unknown hash.', '']
