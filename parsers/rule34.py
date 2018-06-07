import untangle, random, requests
def rule34(req):
    print(req)
    try:
        try:
            tor = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            r = requests.post('http://rule34.xxx/index.php',
                params={
                    'page': 'dapi',
                    's': 'post',
                    'q': 'index',
                    'limit': '100',
                    'tags': ' '.join(req)
                },
                proxies=tor)
            parse = untangle.parse(r.text)
            #randnum = random.randint(0,len(parse.posts.post))
            ret = []
            for r34_c in range(len(parse.posts.post)):
                file_url = parse.posts.post[r34_c]['file_url']
                tags = parse.posts.post[r34_c]['tags'].split(' ')
                # pic = requests.get(file_url).content
                file_type = file_url.split('.')[-1]
                if file_type in ('jpeg', 'png', 'jpg'):
                    ret.append({"type": "photo", "from": "rule34.xxx", "photo": file_url, "tags": tags})
                elif file_type == 'gif':
                    ret.append({"type": "gif", "from": "rule34.xxx", "gif": file_url, "tags": tags})
                elif file_type == 'video':
                    ret.append({"type": "video", "from": "rule34.xxx", "video": file_url, "tags": tags})
                # ret.append([{"type":"hentai", "from":"rule34.xxx", "photo":file_url, "tags": tags}])
            return ret
        except UnicodeEncodeError:
            return [{"type":"error", "from":"rule34.xxx", "text":"Ничего не найдено"}]
    except AttributeError:
        return [{"type":"error", "from":"rule34.xxx", "text":"Ничего не найдено"}]
