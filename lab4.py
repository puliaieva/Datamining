import re

import httplib2
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, SoupStrainer

global root_link
global nodes


class Node:
    def __init__(self, href):
        self.href = href
        self.links = list()

    def __repr__(self):
        return 'link:' + self.href + ' links:' + str(self.links) + '\n\n---------------------\n'

    def add_link(self, link):
        self.links.append(link)


def main():
    global root_link
    global nodes
    nodes = list()
    print('Enter please website link')
    input_str = input()
    res = re.match('(.+?\\..+?)/', input_str)
    if not res:
        res = re.match('(.+?\\..+?)/', input_str + "/")
        if not res:
            print('invalid link')
            return
    root_link = res.group(1)
    http = httplib2.Http()
    get_content(http, input_str)
    # print(nodes)
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node.href)
    for node in nodes:
        for link in node.links:
            graph.add_edge(node.href, link)
    nx.draw(graph, with_labels=True)
    # plt.savefig("simple_path.png")  # save as png
    plt.show()  # display


def get_content(http, href):
    global root_link
    global nodes
    if has_link(href):
        return
    status, response = http.request(href)
    if status.status != 200:
        print('request error, status:' + str(status.status))
        print('request url:' + href)
        return
    node = Node(href)
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
        if link.has_attr('href') and link['href'].startswith('/') and len(link['href']) > 1:
            full_link = root_link + link['href']
            if full_link == href or full_link in node.links:
                continue
            # print(full_link)
            node.links.append(full_link)
    nodes.append(node)
    for link in node.links:
        get_content(http, link)


def has_link(link):
    global nodes
    for node in nodes:
        if node.href == link:
            return True
    return False


main()
