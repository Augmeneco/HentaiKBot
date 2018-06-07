import untangle, random, requests
def rule34(req):
    try:
        try:
            req = req.replace(' ','+')
            blacklist = '-fur+-pony*+-friendship*+-scat*+-furry+-dragon+-guro+-animal_penis+-animal+-wolf+-fox+-webm+-my_little_pony+-monster*+-3d+-animal*+-ant+-insects+-mammal+-horse+-blotch+-deer+-real*+-shit+-everlasting_summer+-copro*+-wtf+'
            parse = untangle.parse('http://0s.oj2wyzjtgqxhq6dy.cmle.ru/index.php?page=dapi&s=post&q=index&limit=100&tags='+blacklist+req)
            randnum = random.randint(0,len(parse.posts.post))
            file_url = parse.posts.post[randnum]['file_url']
            tags = parse.posts.post[randnum]['tags'].split(' ')
            if file_url.find('img.rule34')<0:
                file_url = file_url.replace('rule34.xxx','0s.oj2wyzjtgqxhq6dy.cmle.ru')
                file_url = file_url.replace('https','http')
            else:
                file_url = file_url.replace('img.rule34.xxx','nfwwo.oj2wyzjtgqxhq6dy.cmle.ru')
                file_url = file_url.replace('https','http')
                pic = requests.get(file_url).content
            return [{"type":"photo", "from":"rule34.xxx", "photo":pic, "tags": tags}]
            #return [{"type":"hentai", "from":"rule34.xxx", "photo":"тут картинка", "tags": tags}]
        except UnicodeEncodeError:
                return [{"type":"error", "from":"rule34.xxx", "text":"Ничего не найдено"}]
    except AttributeError:
        return [{"type":"error", "from":"rule34.xxx", "text":"Ничего не найдено"}]
print(rule34('saber'))