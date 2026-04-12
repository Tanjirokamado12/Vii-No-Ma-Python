from flask import Flask, Response
from datetime import datetime

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)