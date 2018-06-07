import untangle, random, requests
def booru(req, pid=None):
    # if pid is None:
    #     print(0)
    #     r = requests.post('http://safebooru.org/index.php',
    #         params={
    #             'page': 'dapi',
    #             's': 'post',
    #             'q': 'index',
    #             'limit': '100',
    #             'pid': 0,
    #             'tags': ' '.join(req)
    #         })
    #     parse = untangle.parse(r.text)
    #     pid = int(random.randint(0, int(parse.posts['count'])) / 100)

    pid = 0
    
    r = requests.post('http://safebooru.org/index.php',
        params={
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'limit': '100',
            'pid': pid,
            'tags': ' '.join(req)
        })
    parse = untangle.parse(r.text)
    if parse.posts['count'] != '0':
        #randnum = random.randint(0,len(parse.posts.post))
        ret = []
        for booru_c in range(len(parse.posts.post)):
            file_url = 'http:' + parse.posts.post[booru_c]['file_url']
            tags = parse.posts.post[booru_c]['tags'].split(' ')
            # pic = requests.get(file_url).content
            file_type = file_url.split('.')[-1]

            if file_type in ('jpeg', 'png', 'jpg'):
                ret.append({"type": "photo", "from": "safebooru.org", "url": file_url, "tags": tags})

            elif file_type == 'gif':
                ret.append({"type": "gif", "from": "safebooru.org", "url": file_url, "tags": tags})

            elif file_type == 'video':
                ret.append({"type": "video", "from": "safebooru.org", "url": file_url, "tags": tags})

        return ret
    else:
        return [{"type": "error", "from": "safebooru.org", "error_type": 1, "text": "Ничего не найдено"}]