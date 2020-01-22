import argparse
import urllib

from company.microsoft import MicrosoftDocument

URL_MAPPING = {
    'careers.microsoft.com': MicrosoftDocument
}


def main(url, debug=True):
    result = urllib.parse.urlparse(url)
    pdf = URL_MAPPING.get(result.hostname)(url)
    if debug:
        pdf.debug()
    else:
        pdf.build()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create printable job description')
    parser.add_argument('url', type=str)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    main(args.url, args.debug)

