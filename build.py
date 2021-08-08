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

    try:
        os.makedirs(os.path.join(dist, "entries"))
    except:
        print("Already have content")
    shutil.rmtree(os.path.join(dist, "src"))
    shutil.rmtree(os.path.join(dist, "images"))
    shutil.copytree(source, os.path.join(dist, "src"))
    shutil.copytree(images, os.path.join(dist, "images"))
    
    pages = listPages()

    summary_templ = getTemplateHTML("summary.html")

    summariesHTML = "\n".join(
            [
                formatEntry(summary_templ, page)
                    .replace(
                            "%content%", 
                            "\n".join(page["html"].split("\n")[:summary_max])
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


    item_templ = getTemplateHTML("item.xml")
    rss_templ = getTemplateHTML("rss.xml")
    itemsXML = "\n".join(
                [
                    formatEntry(item_templ, page).replace("%content%", page["html"])
                    for page in pages
                    ]
            )

    with open(os.path.join(dist, "rss.xml"), "w") as index:
        index.write(
                    rss_templ.replace("%items%", itemsXML)
                )

    print(f"built in {len(pages)} pages")
make()

        

