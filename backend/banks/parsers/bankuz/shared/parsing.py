import re


def parse_rate(text):

    if not text:
        return None

    text = text.lower().replace(",", ".")
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)

    try:

        match_range = re.findall(
            r"(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\s*%",
            text,
        )

        if match_range:

            vals = [
                float(match_range[0][0]),
                float(match_range[0][1]),
            ]

            vals = [v for v in vals if 0 < v < 200]

            if vals:
                return min(vals)

        match_range2 = re.findall(
            r"(\d+\.?\d*)-(\d+\.?\d*)%",
            text,
        )

        if match_range2:

            vals = [
                float(match_range2[0][0]),
                float(match_range2[0][1]),
            ]

            vals = [v for v in vals if 0 < v < 200]

            if vals:
                return min(vals)

        match_range3 = re.findall(
            r"(\d+\.?\d*)%\s*-\s*(\d+\.?\d*)%",
            text,
        )

        if match_range3:

            vals = [
                float(match_range3[0][0]),
                float(match_range3[0][1]),
            ]

            vals = [v for v in vals if 0 < v < 200]

            if vals:
                return min(vals)

        match_min = re.search(
            r"от\s*(\d+\.?\d*)\s*%",
            text,
        )

        if match_min:

            val = float(match_min.group(1))

            if 0 < val < 200:
                return val

        match_max = re.search(
            r"до\s*(\d+\.?\d*)\s*%",
            text,
        )

        if match_max:

            val = float(match_max.group(1))

            if 0 < val < 200:
                return val

        broken = re.findall(
            r"(\d+)\s+(\d+)\s*%",
            text,
        )

        if broken:

            vals = []

            for b in broken:

                val = float(b[1])

                if 0 < val < 200:
                    vals.append(val)

            if vals:
                return min(vals)

        matches = re.findall(
            r"(\d+\.?\d*)\s*%",
            text,
        )

        values = []

        zero_found = False

        for m in matches:

            try:

                val = float(m)

                if val == 0:
                    zero_found = True
                    continue

                if 0 < val < 200:
                    values.append(val)

            except:
                continue

        if values:
            return min(values)

        if zero_found:

            zero_keywords = [
                "без процентов",
                "беспроцент",
                "0% годовых",
                "без переплат",
                "без переплаты",
            ]

            if any(k in text for k in zero_keywords):
                return 0.0

    except:
        return None

    return None


def parse_amount(text):

    if not text:
        return None

    text = text.lower().replace(",", ".")

    match = re.search(
        r"([\d\s]+)\s*("
        r"сум|сумов|uzs|sum|"
        r"долл\.?\s*сша|доллар(?:ов)?|usd|\$|"
        r"евро|eur|€|euro"
        r")",
        text,
        re.IGNORECASE,
    )

    if match:

        raw = re.sub(r"\s+", "", match.group(1))

        if raw.isdigit():

            val = int(raw)

            # Поддерживаем небольшие суммы
            # для валютных вкладов (5 USD, 10 USD и т.д.)
            if 1 <= val < 1_000_000_000_000:
                return val

    match = re.search(
        r"(\d+\.?\d*)\s*(млн|mln)",
        text,
    )

    if match:
        return int(float(match.group(1)) * 1_000_000)

    match = re.search(
        r"(\d+\.?\d*)\s*(млрд|mlrd|billion)",
        text,
    )

    if match:
        return int(float(match.group(1)) * 1_000_000_000)

    return None


def parse_term(text):

    if not text:
        return None

    text = text.lower().replace("–", "-")

    try:

        match = re.search(
            r"(\d+)\s*(мес|месяц|год|лет)\s*[-до]+\s*(\d+)\s*(мес|месяц|год|лет)",
            text,
        )

        if match:

            value = int(match.group(3))

            unit = match.group(4)

            if "год" in unit or "лет" in unit:
                value *= 12

            return value if value <= 600 else None

        match = re.search(
            r"до\s*(\d+)\s*(мес|месяц|год|лет)",
            text,
        )

        if match:

            value = int(match.group(1))

            unit = match.group(2)

            if "год" in unit or "лет" in unit:
                value *= 12

            return value if value <= 600 else None

        match = re.search(
            r"(\d+)\s*(мес|месяц|месяцев|months?|год|года|лет|year|years|yil)",
            text,
        )

        if match:

            value = int(match.group(1))

            unit = match.group(2)

            if any(
                x in unit
                for x in [
                    "год",
                    "лет",
                    "year",
                    "yil",
                ]
            ):
                value *= 12

            return value if value <= 600 else None

    except:
        pass

    return None
