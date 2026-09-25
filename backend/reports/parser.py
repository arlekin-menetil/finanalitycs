from bs4 import BeautifulSoup


def parse_credit_report(file):

    html = file.read()

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    return {

        "status": "ok",

        "title": soup.title.text
        if soup.title
        else "",

    }