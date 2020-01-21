import sys

from urllib.parse import urlparse

from company.microsoft import MicrosoftDocument

URL_MAPPING = {
    'careers.microsoft.com': MicrosoftDocument
}


def main(url):
    result = urlparse(url)
    pdf = URL_MAPPING.get(result.hostname)(url)
    pdf.build()


if __name__ == '__main__':
    main(sys.argv[1])

