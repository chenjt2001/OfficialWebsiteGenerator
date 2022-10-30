from flask import Flask, abort, escape, send_file, Markup, render_template
import os
import json
import time
import markdown

# 使用pipreqs ./ --encoding=utf8 --force生成requirements.txt

app = Flask(__name__)


def getMetaDir(name: str) -> str:
    """获取meta文件夹"""
    metaDir = os.path.join(app.instance_path, f"{escape(name)}")
    if not os.path.exists(metaDir):
        abort(404)
    return metaDir


@app.route('/')
def index():
    """首页，应用列表"""
    appList = []
    for name in os.listdir(app.instance_path):
        if os.path.exists(os.path.join(app.instance_path, name, "metadata.json")):
            appList.append({"name": name, "url": f"./{name}"})
    return render_template('index.html', appList=appList)


@app.route('/<name>/', methods=['GET'])
def officialWebsite(name=None):
    """访问官方网站"""

    # 读取meta文件
    with open(os.path.join(getMetaDir(name), "metadata.json"), encoding="utf-8") as f:
        meta = json.load(f)

    # 生成一些字段
    title = meta["title"]
    name = meta["name"]
    description = meta["description"]
    header = meta["header"]
    contact = meta["contact"]
    copyright = meta["copyright"]
    year = time.localtime(time.time()).tm_year
    history = sorted(
        meta["history"], key=lambda x: x["publishDate"], reverse=True)
    currentVersionName = "V" + history[0]["versionNumber"]
    keywords = ' '.join(set(meta['keywords'] + [meta['name']] + meta["alias"] + [
                        '官方网站'] + meta['authors'] + [currentVersionName]))

    features = [feature.strip() + "；" for feature in meta["features"]]
    if len(features) > 0:
        features[-1] = features[-1][:-1] + "。"

    downloadUrls = meta["downloadUrls"]

    return render_template(
        'officialWebsite.html',
        title=title,
        name=name,
        keywords=keywords,
        description=description,
        header=header,
        features=features,
        downloadUrls=downloadUrls,
        contact=contact,
        copyright=copyright,
        year=year,
        currentVersionName=currentVersionName,
        history=history
    )


@app.route("/<name>/assets/<path:path>", methods=["GET"])
def assets(name, path):
    """获取资源"""

    assetsDirs = [getMetaDir(name), app.static_folder]
    for assetsDir in assetsDirs:
        assetsPath = os.path.join(assetsDir, path)
        if os.path.exists(assetsPath):
            return send_file(assetsPath)
    abort(404)


@app.route('/<name>/privacy/', methods=['GET'])
def privacy(name=None):
    """访问隐私策略"""
    getMetaDir(name)
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables', 'markdown.extensions.toc']

    with open(os.path.join(getMetaDir(name), "privacy.md"), 'r', encoding='utf-8') as f:
        html = markdown.markdown(f.read(), extensions=exts)
    content = Markup(html)
    return content


if __name__ == "__main__":
    # To allow aptana to receive errors, set use_debugger=False
    app.run(host="0.0.0.0", port=5000, debug=True)
