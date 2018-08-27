import sys
import os
import json
from pixivpy3 import *


class Collector(AppPixivAPI):
    def __init__(self):
        super().__init__()

    def _load_file(self, path):
        file_name = os.path.basename(path)
        try:
            file = open(path, 'r')
        except IOError:
            print(path, 'not found')

        if file_name == 'pixiv.json':
            token = json.load(file)
            file.close()
            return token

        elif file_name == 'target.txt':
            tags = []
            tag = file.readline().replace('\n', '')
            while tag:
                tags.append(tag)
                tag = file.readline().replace('\n', '')
            file.close()
            return tags

    def _set_get_illusts(self, target):
        current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current, 'pixiv.json')
        token = self._load_file(path)
        self.login(token['pixiv_id'], token['password'])

        if not os.path.exists(self.output):
            os.makedirs(self.output)

        if target == True:
            path = os.path.join(current, 'target.txt')
            self.targets = self._load_file(path)
        else:
            self.targets = []
        self.target = target
        self.illust_tags = {}

    def _get_illust_with_tags(self, illust, name):
        name = str(name)
        if self.target == True:
            illust_tags = []
            for tag in illust.tags:
                illust_tags.append(tag.name)
            if len(set(self.targets)&set(illust_tags)) > 0:
                self.illust_tags[name] = illust.tags
                self.download(illust.image_urls.large, path=self.output, name=name+'.png')
                return True

            else:
                return False
        else:
            self.illust_tags[name] = illust.tags
            self.download(illust.image_urls.large, path=self.output, name=name+'.png')
            return True

    def _save_tags(self):
        file = open(os.path.join(self.output, 'tags.json'), 'w')
        json.dump(self.illust_tags, file)

    def get_ranking(self, mode, output, target=False):
        self.output = output
        self._set_get_illusts(target)

        json_result = self.illust_ranking(mode=mode)
        while(True):
            illusts = json_result.illusts
            for illust in illusts:
                bool = self._get_illust_with_tags(illust, illust.id)
                if bool == True:
                    print('title %s' % illust.title)
                    print('id %d' % illust.id)
                    print('_'*40)

            next_qs = self.parse_qs(json_result.next_url)
            if isinstance(next_qs, type(None)):
                break
            json_result = self.illust_ranking(**next_qs)

        print('total %d' % len(self.illust_tags))

        self._save_tags()

    def get_illusts(self, startid, endid, min_bookmarks, output, target=False):
        self.output = output
        self._set_get_illusts(target)

        for illust_id in range(startid, endid):
            try:
                json_result = self.illust_detail(illust_id)
                illust = json_result.illust
            except:
                continue
            if illust.total_bookmarks > min_bookmarks:
                bool = self._get_illust_with_tags(illust, illust.id)
                if bool == True:
                    print('title %s' % illust.title)
                    print('id %d' % illust.id)
                    print('_'*40)

        self._save_tags()
