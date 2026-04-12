from flask import Flask, send_from_directory, abort, request, Response
import os
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime, timedelta
from datetime import datetime
from datetime import date
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Asset directories
DIRS = {
    "calendar": os.path.join(BASE_DIR, "Assets", "Calendar"),
    "category": os.path.join(BASE_DIR, "Assets", "CategoryImages"),
    "coupon": os.path.join(BASE_DIR, "Assets", "Coupon"),
    "delivery": os.path.join(BASE_DIR, "Assets", "Delivery"),
    "intro": os.path.join(BASE_DIR, "Assets", "Intro"),
    "pictures": os.path.join(BASE_DIR, "Assets", "Pictures"),
    "specials": os.path.join(BASE_DIR, "Assets", "Specials"),
    "urllink": os.path.join(BASE_DIR, "Assets", "UrlLink"),
    "wall": os.path.join(BASE_DIR, "Assets", "Wall"),
    "pay_wall": os.path.join(BASE_DIR, "Assets", "Theatre", "Wall"),
    "pay_intro": os.path.join(BASE_DIR, "Assets", "Theatre", "intro"),
    "theatre_posters": os.path.join(BASE_DIR, "Assets", "Theatre", "Movie"),
    "movies_posters": os.path.join(BASE_DIR, "Assets","Movie"),
}

# Config + Crypto
CONFIG_PATH = os.path.join(BASE_DIR, "Config", "v770config.txt")
V1025_CONFIG_PATH = os.path.join(BASE_DIR, "Config", "v1025config.txt")

KEY_HEX = "943B13DD87468BA5D9B7A8B899F91803"
IV_HEX = "66B33FC1373FE506EC2B59FB6B977C82"

KEY = binascii.unhexlify(KEY_HEX)
IV = binascii.unhexlify(IV_HEX)

# -----------------------
# Helper (safe file serving)
# -----------------------
def serve_file(directory, filename):
    if not os.path.exists(directory):
        abort(404, description="Directory not found")

    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404, description="File not found")

    return send_from_directory(directory, filename)

# -----------------------
# Static endpoints
# -----------------------
    
@app.route('/v770/url1/calimg/<path:filename>')
def calendar_images(filename):
    return serve_file(DIRS["calendar"], filename)

@app.route('/v1025/url1/list/category/img/<path:filename>')
@app.route('/v770/url1/list/category/img/<path:filename>')
def category_images(filename):
    return serve_file(DIRS["category"], filename)

@app.route('/v1025/url1/coupon/<path:filename>')
@app.route('/v770/url1/coupon/<path:filename>')
def coupon_files(filename):
    return serve_file(DIRS["coupon"], filename)

@app.route('/v1025/url1/delivery/<path:filename>')
@app.route('/v770/url1/delivery/<path:filename>')
def delivery_files(filename):
    return serve_file(DIRS["delivery"], filename)


@app.route('/v1025/url1/intro/<path:filename>')
def intro_files(filename):
    return serve_file(DIRS["intro"], filename)

@app.route("/v1025/url1/movie/<movieid>/<path:filename>")
@app.route("/v770/url1/movie/<movieid>/<path:filename>")
def movie_files(movieid, filename):
    return serve_file(DIRS["movies_posters"], filename)


@app.route("/v1025/url3/pay/movie/<unk>/<movieid>/<path:filename>")
@app.route("/v770/url3/pay/movie/<unk>/<movieid>/<path:filename>")
def theatre_movie_files(unk, movieid, filename):
    return serve_file(DIRS["theatre_posters"], filename)

@app.route('/v1025/url3/pay/intro/<path:filename>')
def pay_intro_files(filename):
    return serve_file(DIRS["pay_intro"], filename)

@app.route('/v1025/url1/pictures/<path:filename>')
@app.route('/v770/url1/pictures/<path:filename>')
def pictures_files(filename):
    return serve_file(DIRS["pictures"], filename)

@app.route('/v1025/url1/special/<sppageid>/img/<path:filename>')
@app.route('/v770/url1/special/<sppageid>/img/<path:filename>')
def specials_files(sppageid, filename):
    special_dir = os.path.join(DIRS["specials"], sppageid)
    return serve_file(special_dir, filename)

@app.route('/v1025/url1/urllink/<path:filename>')
@app.route('/v770/url1/urllink/<path:filename>')
def urllink_files(filename):
    return serve_file(DIRS["urllink"], filename)

@app.route('/v1025/url1/wall/<path:filename>')
@app.route('/v770/url1/wall/<path:filename>')
def wall_files(filename):
    return serve_file(DIRS["wall"], filename)

@app.route('/v1025/url3/pay/wall/<path:filename>')
@app.route('/v770/url3/pay/wall/<path:filename>')
def pay_wall_files(filename):
    return serve_file(DIRS["pay_wall"], filename)

# -----------------------
# Dynamic encrypted endpoint
# -----------------------

@app.route('/v770/first.bin')
def generate_first_bin():
    # Check config exists
    if not os.path.exists(CONFIG_PATH):
        abort(404, description="Config file not found")

    # Read config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace placeholder with current host:port
    host = request.host  # e.g. 192.168.1.27:80
    content = content.replace("IPADRESS:PORT", host)

    # Encrypt (AES-128-CBC)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))

    # Return binary
    return Response(
        encrypted,
        mimetype="application/octet-stream",
        headers={
            "Content-Disposition": "attachment; filename=first.bin"
        }
    )

@app.route('/v1025/first.bin')
def v1025_generate_first_bin():
    # Check config exists
    if not os.path.exists(V1025_CONFIG_PATH):
        abort(404, description="Config file not found")

    # Read config
    with open(V1025_CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace placeholder with current host:port
    host = request.host  # e.g. 192.168.1.27:80
    content = content.replace("IPADRESS:PORT", host)

    # Encrypt (AES-128-CBC)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))

    # Return binary
    return Response(
        encrypted,
        mimetype="application/octet-stream",
        headers={
            "Content-Disposition": "attachment; filename=first.bin"
        }
    )


# -----------------------
# Run server
# -----------------------

def now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


@app.route("/v770/url1/conf/datetime.xml")
def datetime_xml():
    xml = f"""<datetime>
<upddt>{now()}</upddt>
</datetime>"""
    return Response(xml, mimetype="application/xml")


@app.route("/v1025/url2/reginfo.cgi")
def reginfo():
    t = now()
    xml = f"""<RegionInfo>
<ver>1</ver>
<sdt>{t}</sdt>
<cdt>{t}</cdt>
<limited>1</limited>
</RegionInfo>"""
    return Response(xml, mimetype="application/xml")

# ----------------------------- #
# PARSE FILE
# ----------------------------- #
def parse_event_file(path="files/event.txt"):
    data = {
        "color": "",
        "Frameid": "",
        "news_blocks": [],
        "intro_blocks": [],
        "poster_blocks": []
    }

    current_intro = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # ---------------- POSTER ----------------
            if line.startswith("Posterid:"):
                data["poster_blocks"].append({
                    "posterid": line.split(":", 1)[1].strip(),
                    "linktype": "0",
                    "linkid": ""
                })
                current_intro = None  # reset context

            # ---------------- NEWS ----------------
            elif line.startswith("News:"):
                data["news_blocks"].append(
                    line.split(":", 1)[1].strip()
                )
                current_intro = None

            # ---------------- INTRO ----------------
            elif line.startswith("Cntid:"):
                current_intro = {
                    "cntid": line.split(":", 1)[1].strip(),
                    "linktype": "0",
                    "linkid": ""
                }
                data["intro_blocks"].append(current_intro)

            # ---------------- LINK HANDLING ----------------
            elif line.startswith("LinkType:"):
                value = line.split(":", 1)[1].strip()

                if current_intro:
                    current_intro["linktype"] = value
                elif data["poster_blocks"]:
                    data["poster_blocks"][-1]["linktype"] = value

            elif line.startswith("Linkid:"):
                value = line.split(":", 1)[1].strip()

                if current_intro:
                    current_intro["linkid"] = value
                elif data["poster_blocks"]:
                    data["poster_blocks"][-1]["linkid"] = value

            # ---------------- OTHER ----------------
            elif line.startswith("Color:"):
                data["color"] = line.split(":", 1)[1].strip()

            elif line.startswith("Frameid:"):
                data["Frameid"] = line.split(":", 1)[1].strip()

    return data


# ----------------------------- #
# NEWS
# ----------------------------- #
def build_news(news_list):
    return "\n".join(
        f"""<newsinfo>
    <page>{i}</page>
    <news>{news}</news>
</newsinfo>"""
        for i, news in enumerate(news_list, start=1)
    )


# ----------------------------- #
# INTRO
# ----------------------------- #
def build_intro(intro_list):
    blocks = []

    for i, item in enumerate(intro_list, start=1):
        cntid = item["cntid"]
        linktype = item.get("linktype", "0")
        linkid = item.get("linkid", "")

        # build link section
        if linktype == "0":
            link_xml = f"<linktype>0</linktype>"
        else:
            link_xml = f"""<linktype>{linktype}</linktype>
    <linkid>{linkid}</linkid>"""

        if len(cntid) >= 16:
            blocks.append(f"""<introinfo>
    <seq>{i}</seq>
    <cntid>{cntid}</cntid>
    <cnttype>0</cnttype>
    <random>1</random>
    {link_xml}
</introinfo>""")

        elif len(cntid) == 1:
            blocks.append(f"""<introinfo>
    <seq>{i}</seq>
    <cntid>{cntid}</cntid>
    <cnttype>1</cnttype>
    <random>0</random>
    <dispsec>5</dispsec>
    <dimg>1</dimg>
    {link_xml}
</introinfo>""")

        else:
            blocks.append(f"""<introinfo>
    <seq>{i}</seq>
    <cntid>{cntid}</cntid>
    <cnttype>0</cnttype>
    <random>0</random>
    {link_xml}
</introinfo>""")

    return "\n".join(blocks)


# ----------------------------- #
# POSTER
# ----------------------------- #
def build_poster(version, poster_list):

    # -------- v770 --------
    if str(version) == "770":
        return "\n".join(
            f"""<posterid>{p["posterid"]}</posterid>"""
            for p in poster_list
        )

    # -------- v1025 --------
    if str(version) == "1025":
        return "\n".join(
            f"""<posterinfo>
    <seq>{i}</seq>
    <posterid>{p["posterid"]}</posterid>
</posterinfo>"""
            for i, p in enumerate(poster_list, start=1)
        )

    return ""


# ----------------------------- #
# ROUTE
# ----------------------------- #
@app.route("/v<int:version>/url1/event/today.xml")
def event_today(version):

    data = parse_event_file("files/event.txt")

    today = date.today().isoformat()

    news_xml = build_news(data["news_blocks"])
    intro_xml = build_intro(data["intro_blocks"])
    poster_xml = build_poster(version, data["poster_blocks"])

    xml = f"""<Event>
  <ver>1</ver>
  <date>{today}</date>
  <color>{data["color"]}</color>
  <frameid>{data["Frameid"]}</frameid>
  <postertime>5</postertime>
{poster_xml}
{news_xml}
  <adinfo>
    <pref>2</pref>
    <adid>1</adid>
    <pref>1</pref>
    <adid>1</adid>
  </adinfo>
{intro_xml}
</Event>"""

    return Response(xml, mimetype="application/xml")


# -----------------------------
# PARSE FILE (PAGEINFO)
# -----------------------------
def parse_page_file(path="files/SpPage.txt"):
    data = {
        "version": "1",
        "upddt": "2026-01-01T00:00:00",
        "pages": []
    }

    current_page = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Pageinfo"):
                current_page = {
                    "sppageid": "",
                    "name": "",
                    "level": "",
                    "miiid": "",
                    "color1": "",
                    "color2": "",
                    "logo1id": "",
                    "news": "",
                    "valid": "1",
                    "pref": ""
                }
                data["pages"].append(current_page)

            elif ":" in line and current_page is not None:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "sppageid":
                    current_page["sppageid"] = value
                elif key == "name":
                    current_page["name"] = value
                elif key == "level":
                    current_page["level"] = value
                elif key == "miiid":
                    current_page["miiid"] = value
                elif key == "color1":
                    current_page["color1"] = value
                elif key == "color2":
                    current_page["color2"] = value
                elif key == "logo1id":
                    current_page["logo1id"] = value
                elif key == "news":
                    current_page["news"] = value
                elif key == "pref":
                    current_page["pref"] = value

    return data


# -----------------------------
# BUILD PAGEINFO XML
# -----------------------------
def build_pageinfo(pages):
    return "\n".join(
        f"""<pageinfo>
    <sppageid>{p['sppageid']}</sppageid>
    <name>{p['name']}</name>
    <level>{p['level']}</level>
    <miiid>{p['miiid']}</miiid>
    <color1>{p['color1']}</color1>
    <color2>{p['color2']}</color2>
    <logo1id>{p['logo1id']}</logo1id>
    <news>{p['news']}</news>
    <valid>1</valid>
    <pref>11111111111111111111111111111111111111111111111</pref>
  </pageinfo>"""
        for p in pages
    )


# -----------------------------
# ROUTE
# -----------------------------
@app.route("/v<int:version>/url1/special/all.xml")
def sppage(version):

    data = parse_page_file("files/SpPageList.txt")

    xml = f"""<SpPageList>
  <ver>1</ver>
{build_pageinfo(data["pages"])}

  <upddt>{data["upddt"]}</upddt>
</SpPageList>"""

    return Response(xml, mimetype="application/xml")

def parse_payeven_file(filepath):
    data = {
        "Posterid1": "",
        "Posterid2": "",
        "intros": []
    }

    current_intro = None

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # Start new IntroInfo block
            if line == "IntroInfo":
                if current_intro:
                    data["intros"].append(current_intro)

                current_intro = {
                    "IntroMovid": "",
                    "cntid": "",
                    "Linktype": "",
                    "Linkid": ""
                }
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if current_intro is not None:
                    current_intro[key] = value
                else:
                    data[key] = value

    # Add last intro block
    if current_intro:
        data["intros"].append(current_intro)

    return data


@app.route('/v<int:version>/url3/pay/event/today.xml')
def pay_event(version):
    file_path = os.path.join("files", "PayEvent.txt")

    if not os.path.exists(file_path):
        return Response("File not found", status=404)

    data = parse_payeven_file(file_path)
    today = date.today().isoformat()

    # Build introinfo XML blocks
    intro_xml = ""
    for i, intro in enumerate(data["intros"], start=1):
        linkid_xml = ""
        if intro.get("Linktype") != "0":
            linkid_xml = f"<linkid>{intro.get('Linkid', '')}</linkid>"

        intro_xml += f"""
<introinfo>
<seq>{i}</seq>
<cntid>{intro.get('cntid', '')}</cntid>
<intromovid>{intro.get('IntroMovid', '')}</intromovid>
<cnttype>1</cnttype>
<random>0</random>
<dispsec>5</dispsec>
<dimg>1</dimg>
<linktype>{intro.get('Linktype', '')}</linktype>
{linkid_xml}
</introinfo>
"""

    # Final XML
    xml = f"""
<PayEvent>
<ver>1</ver>
<date>{today}</date>

<posterid1>{data.get('Posterid1', '')}</posterid1>
<posterid2>{data.get('Posterid2', '')}</posterid2>
<postertime>5</postertime>

<posterinfo>
<seq>1</seq>
<posterid>{data.get('Posterid1', '')}</posterid>
<geofilter>0</geofilter>
</posterinfo>

<posterinfo>
<seq>2</seq>
<posterid>{data.get('Posterid2', '')}</posterid>
<geofilter>0</geofilter>
</posterinfo>

{intro_xml}

</PayEvent>
"""

    return Response(xml, mimetype="application/xml")

def movielink_parse_file(filepath):
    groups = []
    current = {}

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.lower() == "linkinfo":
                if current:
                    groups.append(current)
                    current = {}
            else:
                if ":" in line:
                    key, value = line.split(":", 1)
                    current[key.strip().lower()] = value.strip()

        # append last group
        if current:
            groups.append(current)

    return groups


def movielink_build_xml(groups, version):
    root = ET.Element("MovieLink")

    ver = ET.SubElement(root, "ver")
    ver.text = "1"

    for g in groups:
        # 👉 skip entire block if v770 and no paymovid
        if version == "v770" and "paymovid" not in g:
            continue

        linkinfo = ET.SubElement(root, "linkinfo")

        # always include movieid
        if "movieid" in g:
            ET.SubElement(linkinfo, "movieid").text = g["movieid"]

        if version == "v770":
            # only include paymovid
            ET.SubElement(linkinfo, "paymovid").text = g["paymovid"]
        else:
            # include all available fields
            for key in ["paymovid", "categid", "shopid"]:
                if key in g:
                    ET.SubElement(linkinfo, key).text = g[key]

    return ET.tostring(root, encoding="utf-8")

@app.route('/<version>/url1/conf2/paylink.xml')
def paylink(version):
    groups = movielink_parse_file("Files/MovieLink.txt")
    xml_data = movielink_build_xml(groups, version)

    return Response(xml_data, mimetype="application/xml")


POSTER_META_PATH = "Files/PosterMeta.txt"
MOVIE_META_PATH = "Files/MovieMeta.txt"

# ----------------------------
# CONFIG
# ----------------------------

WEEKDAY_MAP = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

# ----------------------------
# LOAD MOVIE META
# ----------------------------

def load_movies():
    movies = {}
    current = {}

    with open("files/moviemeta.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("MovieId:"):
                if current:
                    movies[current["MovieId"]] = current
                    current = {}

                current["MovieId"] = line.split(":", 1)[1]

            elif ":" in line:
                k, v = line.split(":", 1)
                current[k] = v

        if current:
            movies[current["MovieId"]] = current

    return movies


# ----------------------------
# LOAD CALENDAR DAILY
# ----------------------------

def load_caldaily():
    data = {}
    default_blocks = []
    default_movieids = []

    current_date = None
    current_block = None
    mode = None

    with open("files/Caldaily.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            # -------------------------
            # DATE
            # -------------------------
            if line.startswith("Date:"):
                current_date = line.split(":", 1)[1].strip()
                data[current_date] = {
                    "blocks": [],
                    "movieids": []
                }
                mode = "date"
                current_block = None
                continue

            # -------------------------
            # DEFAULT SECTION
            # -------------------------
            if line.startswith("Default String"):
                mode = "default"
                current_block = None
                continue

            # -------------------------
            # TINDEX BLOCK
            # -------------------------
            if line.startswith("Tindex:"):
                block = {
                    "Tindex": line.split(":", 1)[1].strip(),
                    "Thead": "",
                    "Tdetails": "",
                    "timg": "0",
                    "timgnum": "0",
                    "tbgm": "0"
                }

                current_block = block

                if mode == "default":
                    default_blocks.append(block)
                elif mode == "date":
                    data[current_date]["blocks"].append(block)

                continue

            # -------------------------
            # MOVIE IDS
            # -------------------------
            if line.startswith("movieid:"):
                mid = line.split(":", 1)[1].strip()

                if mode == "default":
                    default_movieids.append(mid)
                elif mode == "date" and current_date:
                    data[current_date]["movieids"].append(mid)

                continue

            # -------------------------
            # BLOCK VALUES
            # -------------------------
            if ":" in line and current_block is not None:
                k, v = line.split(":", 1)
                current_block[k.strip()] = v.strip()

    return data, default_blocks, default_movieids


# ----------------------------
# GET WEEK (MON-SUN)
# ----------------------------

def get_week_dates(date_str):
    d = datetime.strptime(date_str, "%Y%m%d")
    start = d - timedelta(days=d.weekday())
    return [start + timedelta(days=i) for i in range(7)]


# ----------------------------
# BUILD XML
# ----------------------------
def build_calendar(date_str):
    movies = load_movies()
    caldaily, default_blocks, default_movieids = load_caldaily()

    root = ET.Element("Calendar")
    ET.SubElement(root, "ver").text = "1"

    week_dates = get_week_dates(date_str)

    for i, day in enumerate(week_dates):
        date_key = day.strftime("%Y-%m-%d")

        dayinfo = ET.SubElement(root, "dayinfo")
        ET.SubElement(dayinfo, "date").text = date_key
        ET.SubElement(dayinfo, "wday").text = WEEKDAY_MAP[i]
        ET.SubElement(dayinfo, "holiday").text = "0"
        ET.SubElement(dayinfo, "thead").text = "Thead"

        # -------------------------
        # USE DATE OR DEFAULT
        # -------------------------
        if date_key in caldaily:
            movie_ids = caldaily[date_key]["movieids"]
            blocks = caldaily[date_key]["blocks"]
        else:
            movie_ids = default_movieids
            blocks = default_blocks

        # -------------------------
        # BUILD MOVIES
        # -------------------------
        for idx, mid in enumerate(movie_ids[:3], start=1):
            movieinfo = ET.SubElement(dayinfo, "movieinfo")

            ET.SubElement(movieinfo, "seq").text = str(idx)
            ET.SubElement(movieinfo, "movieid").text = mid

            meta = movies.get(mid, {})

            ET.SubElement(movieinfo, "title").text = meta.get("Title", "")
            ET.SubElement(movieinfo, "strdt").text = "2000-01-01T00:00:00"
            ET.SubElement(movieinfo, "enddt").text = "2036-01-01T00:00:00"

        # (optional) you can also output Tindex blocks if needed

    return ET.tostring(root, encoding="utf-8", xml_declaration=False)


# ----------------------------
# FLASK ROUTE
# ----------------------------

@app.route("/v770/url1/cal/<date>.xml")
def calendar(date):
    try:
        xml_data = build_calendar(date)
        return Response(xml_data, mimetype="application/xml")
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", mimetype="application/xml", status=500)


# ----------------------------
# RUN APP
# ----------------------------

def parse_blocks(file_path):
    """Parse blocks separated by blank lines into dicts"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    blocks = content.split("\n\n")
    result = []

    for block in blocks:
        data = {}
        for line in block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        result.append(data)

    return result

@app.route("/v770/url1/wall/<posterid>.met")
@app.route("/v1025/url1/wall/<posterid>.met")
def get_poster_meta(posterid):
    # Load poster meta
    poster_data = parse_blocks(POSTER_META_PATH)

    movie_id = None
    for entry in poster_data:
        if entry.get("PosterId") == posterid:
            movie_id = entry.get("MovieId")
            break

    if not movie_id:
        return Response("Poster not found", status=404)

    # Load movie meta
    movie_data = parse_blocks(MOVIE_META_PATH)

    title = "Unknown"
    for entry in movie_data:
        if entry.get("MovieId") == movie_id:
            title = entry.get("Title", "Unknown")
            break

    # Build XML response
    xml_response = f"""<PosterMeta>
    <ver>1</ver>
    <posterid>{posterid}</posterid>
    <msg>{title}</msg>
    <movieid>{movie_id}</movieid>
    <title>{title}</title>
</PosterMeta>
"""

    return Response(xml_response, mimetype="application/xml")

PAY_POSTER_META_PATH = "Files/PayPosterMeta.txt"
PAY_MOVIE_META_PATH = "Files/PayMovieMeta.txt"


def parse_blocks(file_path):
    """Parse blocks separated by blank lines into dicts"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    blocks = content.split("\n\n")
    result = []

    for block in blocks:
        data = {}
        for line in block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        result.append(data)

    return result


@app.route("/v770/url3/pay/wall/<posterid>.met")
@app.route("/v1025/url3/pay/wall/<posterid>.met")
def pay_get_poster_meta(posterid):

    # Load poster meta
    poster_data = parse_blocks(PAY_POSTER_META_PATH)

    movie_id = None
    poster_type = "1"   # default type if not found

    for entry in poster_data:
        if entry.get("PosterId") == posterid:
            movie_id = entry.get("MovieId")
            poster_type = entry.get("Type", "1")
            break

    if not movie_id:
        return Response("Poster not found", status=404)

    # Load movie meta
    movie_data = parse_blocks(PAY_MOVIE_META_PATH)

    title = "Unknown"
    aspect = "0"

    for entry in movie_data:
        if entry.get("MovieId") == movie_id:
            title = entry.get("Title", "Unknown")
            aspect = entry.get("aspect", "0")
            break

    # Build XML response (matching your required format)
    xml_response = f"""<PayPosterMeta>
<ver>1</ver>
<posterid>{posterid}</posterid>
<msg>{title}</msg>
<movieid>{movie_id}</movieid>
<type>1</type>
<aspect>{aspect}</aspect>
</PayPosterMeta>
"""

    return Response(xml_response, mimetype="application/xml")
    
@app.route("/v770/url1/conf/eula.xml")
@app.route("/v1025/url1/conf/eula.xml")
def eula_xml():
    file_path = os.path.join("files", "eula.txt")

    # read the text file
    with open(file_path, "r", encoding="utf-8") as f:
        eula_text = f.read().strip()

    # build XML response
    xml = f"""<LicenseAgree>
  <ver>1</ver>
  <agree>{eula_text}</agree>
</LicenseAgree>"""

    return Response(xml, mimetype="application/xml")

def parse_txt_to_xml(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    root = ET.Element("PayCategoryHeader")

    ver = ET.SubElement(root, "ver")
    ver.text = "1"

    img_value = None
    listinfo_elements = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("Img:"):
            img_value = line.split(":", 1)[1].strip()

        elif line == "Listinfo":
            # next expected fields
            type_val = None
            name_val = None

            i += 1
            while i < len(lines) and lines[i] != "Listinfo":
                if lines[i].startswith("Type:"):
                    type_val = lines[i].split(":", 1)[1].strip()
                elif lines[i].startswith("Name:"):
                    name_val = lines[i].split(":", 1)[1].strip()
                i += 1
            i -= 1  # step back because outer loop will i += 1

            listinfo_elements.append((type_val, name_val))

        i += 1

    # img node
    img = ET.SubElement(root, "img")
    img.text = img_value if img_value else "0"

    # listinfo nodes
    for idx, (t, n) in enumerate(listinfo_elements, start=1):
        li = ET.SubElement(root, "listinfo")

        place = ET.SubElement(li, "place")
        place.text = str(idx)

        typ = ET.SubElement(li, "type")
        typ.text = t if t else "0"

        text = ET.SubElement(li, "text")
        text.text = n if n else ""

    return ET.tostring(root, encoding="utf-8", xml_declaration=False)

@app.route("/v770/url3/pay/list/category/header.xml")
@app.route("/v1025/url3/pay/list/category/header.xml")
def header_xml():
    xml_data = parse_txt_to_xml("Files/PayCategoryHeader.txt")
    return Response(xml_data, mimetype="application/xml")

CATEGORY_LIST_FILE_PATH = "Files/CategoryList.txt"


def load_categories():
    categories = []

    with open(CATEGORY_LIST_FILE_PATH, "r", encoding="utf-8") as f:
        block = {}

        for line in f:
            line = line.strip()

            if not line:
                if block:
                    categories.append(block)
                    block = {}
                continue

            if line.startswith("Categid:"):
                block["categid"] = line.split(":", 1)[1].strip()

            elif line.startswith("Name:"):
                block["name"] = line.split(":", 1)[1].strip()

        # last block
        if block:
            categories.append(block)

    return categories

@app.route("/v770/url1/list/category/01.xml")
@app.route("/v1025/url1/list/category/01.xml")
def category_list():
    categories = load_categories()

    xml = []
    xml.append("<CategoryList>")
    xml.append("  <ver>1</ver>")
    xml.append("  <type>1</type>")

    for idx, cat in enumerate(categories, start=1):
        xml.append("  <categinfo>")
        xml.append(f"    <place>{idx}</place>")
        xml.append(f"    <categid>{cat.get('categid','')}</categid>")
        xml.append(f"    <name>{cat.get('name','')}</name>")
        xml.append("  </categinfo>")

    xml.append("</CategoryList>")

    return Response("\n".join(xml), mimetype="application/xml")

@app.route("/v770/url1/beacon/<path:request>")
@app.route("/v1025/url1/beacon/<path:request>")
def beacon(request):
    xml_response = """<SampleRequest>
  <code>1</code>
  <msg>Viinoma</msg>
</SampleRequest>"""

    return Response(xml_response, mimetype="application/xml")

caldaily_FILE_PATH = "files/caldaily.txt"
caldaily_MOVIE_FILE = "files/MovieMeta.txt"


# ----------------------------
# WEEKDAY
# ----------------------------
def caldaily_get_calwday(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return ["MO", "TU", "WE", "TH", "FR", "SA", "SU"][dt.weekday()]


# ----------------------------
# MOVIE META LOADER
# ----------------------------
def caldaily_load_movie_meta():
    with open(caldaily_MOVIE_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    movies = {}
    current = None

    for line in lines:
        if line.startswith("MovieId:"):
            current = line.split(":", 1)[1].strip()
            movies[current] = {}
            continue

        if ":" in line and current:
            k, v = line.split(":", 1)
            movies[current][k.strip()] = v.strip()

    return movies


# ----------------------------
# CALDAILY PARSER
# ----------------------------
def parse_caldaily_file():
    with open(caldaily_FILE_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    entries = {}
    default_blocks = []

    current_date = None
    current_block = None
    current_default = None
    in_default = False

    def start_block():
        return {
            "Tindex": None,
            "Thead": "",
            "Tdetails": "",
            "timg": "0",
            "timgnum": "0",
            "tbgm": "1",
            "movieid": []
        }

    def flush_date():
        nonlocal current_block
        if current_date and current_block and current_block["Tindex"] is not None:
            entries.setdefault(current_date, []).append(current_block)
        current_block = None

    def flush_default():
        nonlocal current_default
        if current_default and current_default["Tindex"] is not None:
            default_blocks.append(current_default)
        current_default = None

    for line in lines:

        # -------------------------
        # DATE
        # -------------------------
        if line.startswith("Date:"):
            flush_date()
            flush_default()

            current_date = line.split(":", 1)[1].strip()
            current_block = start_block()
            in_default = False
            continue

        # -------------------------
        # DEFAULT
        # -------------------------
        if line.startswith("Default String"):
            flush_date()
            flush_default()

            current_date = None
            current_block = None
            current_default = start_block()
            in_default = True
            continue

        if ":" not in line:
            continue

        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()

        # -------------------------
        # NEW TRIVIA BLOCK
        # -------------------------
        if k == "Tindex":

            if in_default:
                flush_default()
                current_default = start_block()
                current_default["Tindex"] = v
                continue
            else:
                flush_date()
                current_block = start_block()
                current_block["Tindex"] = v
                continue

        # -------------------------
        # ASSIGN FIELDS
        # -------------------------
        target = current_default if in_default else current_block

        if target is None:
            continue

        if k == "movieid":
            target["movieid"].append(v)
        else:
            target[k] = v

    flush_date()
    flush_default()

    return entries, default_blocks


# ----------------------------
# BUILD MOVIE INFO
# ----------------------------
def build_movieinfo(movie_ids, movie_meta):
    xml = ""

    for i, mid in enumerate(movie_ids):
        meta = movie_meta.get(str(mid), {})
        title = meta.get("Title", f"Movie{mid}")

        xml += f"""
<movieinfo>
<seq>{i+1}</seq>
<movieid>{mid}</movieid>
<strdt>2000-01-01T00:00:00</strdt>
<enddt>2036-01-01T00:00:00</enddt>
<title>{title}</title>
</movieinfo>"""

    return xml


# ----------------------------
# BUILD XML
# ----------------------------
def build_xml(blocks, date_str, calwday, movie_meta):

    trivia_xml = ""

    all_movie_ids = []

    for b in blocks:

        all_movie_ids.extend(b.get("movieid", []))

        trivia_xml += f"""
<trivia>
<tindex>{b.get("Tindex","1")}</tindex>
<thead>{b.get("Thead","")}</thead>
<tdetail>{b.get("Tdetails","")}</tdetail>
<timg>{b.get("timg","0")}</timg>
<timgnum>{b.get("timgnum","0")}</timgnum>
<tbgm>{b.get("tbgm","1")}</tbgm>
</trivia>
"""

    # remove duplicates but keep order
    all_movie_ids = list(dict.fromkeys(all_movie_ids))

    movie_xml = build_movieinfo(all_movie_ids, movie_meta)

    return f"""<CalDaily>
<ver>1</ver>
<date>{date_str}</date>
<wday>{calwday}</wday>
<holiday>0</holiday>
{trivia_xml}
{movie_xml}
</CalDaily>"""


# ----------------------------
# ROUTE
# ----------------------------
@app.route("/v770/url1/caldaily/<date>.xml")
def caldaily(date):

    entries, default_blocks = parse_caldaily_file()
    movie_meta = caldaily_load_movie_meta()

    formatted = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    if formatted in entries:
        blocks = entries[formatted]
    else:
        blocks = default_blocks

    calwday = caldaily_get_calwday(formatted)

    xml = build_xml(blocks, formatted, calwday, movie_meta)

    return Response(xml, mimetype="application/xml")


# ----------------------------
# Load Movie IDs
# ----------------------------
def load_movie_ids(path):
    ids = []

    if not os.path.exists(path):
        return ids

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("Movieid:"):
                ids.append(line.split(":", 1)[1].strip())

    return ids


# ----------------------------
# Load Movie Meta
# ----------------------------
def load_movie_meta(path):
    movies = {}
    current = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                if "MovieId" in current:
                    movies[str(current["MovieId"]).strip()] = current
                current = {}
                continue

            if ":" in line:
                k, v = line.split(":", 1)
                current[k.strip()] = v.strip()

    if "MovieId" in current:
        movies[str(current["MovieId"]).strip()] = current

    return movies


# ----------------------------
# XML Route
# ----------------------------
@app.route("/v770/url3/pay/list/new/all.xml")
def new_pay_movies():

    movie_ids = load_movie_ids("files/NewPayMovies.txt")
    meta = load_movie_meta("files/PayMovieMeta.txt")

    xml = []
    xml.append("<NewPayMovies>")
    xml.append("<ver>1</ver>")

    rank = 1

    for mid in movie_ids:

        if mid not in meta:
            continue

        m = meta[mid]

        title = m.get("Title", "")
        released = m.get("Released", "2000-01-01")
        price = m.get("Price", "0")

        xml.append("<movieinfo>")
        xml.append(f"<rank>{rank}</rank>")
        xml.append(f"<movieid>{mid}</movieid>")
        xml.append(f"<title>{title}</title>")
        xml.append("<kana>12345678</kana>")
        xml.append("<refid>01234567890123456789012345678912</refid>")
        xml.append("<strdt>2000-01-01T00:00:00</strdt>")
        xml.append("<pop>1</pop>")
        xml.append(f"<released>{released}</released>")
        xml.append("<term>1</term>")
        xml.append(f"<price>{price}</price>")
        xml.append("</movieinfo>")

        rank += 1

    xml.append("</NewPayMovies>")

    return Response("\n".join(xml), mimetype="application/xml")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)