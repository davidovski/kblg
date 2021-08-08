import markdown
import os
import time
import shutil

from const import *

def getTemplateHTML(name):
    html = ""
    with open(os.path.join(templates, name), "r") as file:
        html = file.read();
    return html

def listPages():
    return [
        (lambda path: 
            (lambda content: 
                (lambda timestamp: 
                    (lambda name: {
                        "source_file" : path,
                        "source_content" : content,
                        "html" : markdown.markdown(content),
                        "timestamp" : timestamp,
                        "date": time.strftime(date_format, time.localtime(timestamp)),
                        "name" : name,
                        "url" : f"entries/{name}.html"
                    })(".".join(p.split(".")[:-1]))
                )(os.stat(path).st_ctime)
            )(open(path, "r").read())
        )(os.path.join(source, p)) for p in os.listdir(source)
    ]

def formatEntry(content, page):
        return content.replace("%date%", page["date"])\
            .replace("%name%", page["name"])\
            .replace("%time%", str(page["timestamp"]))\
            .replace("%source%", site_index + page["source_file"])\
            .replace("%url%", site_index + page["url"])

def make():

    shutil.rmtree(dist)
    os.makedirs(os.path.join(dist, "entries"))
    shutil.copytree(source, os.path.join(dist, "src"))
    shutil.copytree(images, os.path.join(dist, "images"))
    
    pages = listPages()

    summary_templ = getTemplateHTML("summary.html")

    summariesHTML = "\n".join(
            [
                formatEntry(summary_templ, page)
                    .replace(
                            "%content%", 
                            "\n".join(page["html"].split("\n")[:10])
                        ) 
                
                for page in pages
            ]
    )

    entry_templ = getTemplateHTML("page.html")
    
    for page in pages:
        with open(os.path.join(dist, page["url"]), "w") as entry:
            entry.write(
                        formatEntry(
                                entry_templ,
                                page
                            )
                        .replace("%content%", page["html"])
                    )

        

    index_templ = getTemplateHTML("index.html")

    with open(os.path.join(dist, "index.html"), "w") as index:
        index.write(
                    index_templ.replace("%entries%", summariesHTML)
                )


make()

        

