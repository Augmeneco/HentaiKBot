import untangle, random , requests
def rule34(req, pid=None):
    tor = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }

    # if pid is None:
    #     r = requests.post('http://rule34.xxx/index.php',
    #         params={
    #             'page': 'dapi',
    #             's': 'post',
    #             'q': 'index',
    #             'limit': '100',
    #             'pid': 0,
    #             'tags': ' '.join(req)
    #         },
    #         proxies=tor)
    #     parse = untangle.parse(r.text)
    #     pid = int(random.randint(0, int(parse.posts['count'])) / 100)

    pid = 0

    r = requests.post('http://rule34.xxx/index.php',
        params={
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'limit': '100',
            'deleted':'show',
            'pid': pid,
            'tags': ' '.join(req)
        },
        proxies=tor)
    parse = untangle.parse(r.text)

    if parse.posts['count'] != '0':
        #randnum = random.randint(0,len(parse.posts.post))
        ret = []
        for r34_c in range(len(parse.posts.post)):
            file_url = parse.posts.post[r34_c]['file_url']
            tags = parse.posts.post[r34_c]['tags'].split(' ')
            # pic = requests.get(file_url).content
            file_type = file_url.split('.')[-1]

            if file_type in ('jpeg', 'png', 'jpg'):
                ret.append({"type": "photo", "from": "rule34.xxx", "url": file_url, "tags": tags})

            elif file_type == 'gif':
                ret.append({"type": "gif", "from": "rule34.xxx", "url": file_url, "tags": tags})

            elif file_type == 'video':
                ret.append({"type": "video", "from": "rule34.xxx", "url": file_url, "tags": tags})

        return ret
    else:
        return [{"type": "error", "from": "rule34.xxx", "error_type": 1, "text": "Ничего не найдено"}]
