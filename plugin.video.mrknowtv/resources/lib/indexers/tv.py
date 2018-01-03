# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2016 mrknow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os,sys,re,urllib,urlparse,datetime
import json
import re

try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None

from resources.lib.lib import control
from resources.lib.lib import client
from resources.lib.lib import cache
#from resources.lib.lib import favourites
from resources.lib.lib import workers
from resources.lib.sources import looknij
from resources.lib.sources import videostar
from resources.lib.sources import yoy
from resources.lib.sources import weeb
from resources.lib.sources import wizja
from resources.lib.sources import ipla
from resources.lib.sources import telewizjadanet
from resources.lib.sources import pierwsza
from resources.lib.sources import itivi



from resources.lib.lib import views



class tv:
    def __init__(self):
        self.list = []

        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.telewizjadanet_link = 'http://www.telewizjada.net'
        self.videostar_link = 'https://api-pilot.wp.pl'
        self.yoy_link = 'http://yoy.tv'
        self.weeb_link = 'http://weeb.tv'
        self.wizja_link = 'http://wizja.tv'
        self.eskago_link = 'http://www.eskago.pl/tv'
        self.itivi_link = 'http://itivi.pl/program-telewizyjny/'
        self.looknij_link = 'https://looknij.in'
        self.ipla = 'http://ipla.tv/'
        self.pierwsza_link = 'http://pierwsza.tv'



    def get(self, url, idx=True):
        try:

            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass

            if url in self.telewizjadanet_link:
                control.log('TUU')
                self.telewizjadanet_list(url)
            if url in self.pierwsza_link:
                self.pierwsza_list(url)

            if url in self.ipla:
                self.ipla_list(url)
            if url in self.itivi_link:
                self.itivi_list(url)
            if url in self.eskago_link:
                control.log('1AAAi %s' % url)

                self.eskago_list(url)
            if url in self.videostar_link:
                self.videostar_list(url)
            if url in self.yoy_link:
                self.yoy_list(url)
            if url in self.weeb_link:
                self.weeb_list(url)
            if url in self.wizja_link:
                self.wizja_list(url)

            if url in self.looknij_link:
                if sys.version_info < (2, 7, 9):
                    mystring = 'Not Supported python version %s.%s.%s Minimum: 2.7.9' % (sys.version_info[:3])
                    control.dialog.ok(control.addonInfo('name'), mystring.encode('utf-8'), '')

                self.looknij_list(url)

            if idx == True: self.movieDirectory(self.list)

            return self.list

        except Exception as e:
            control.log('Error: %s' % e)
            pass

    def telewizjadanet_list(self,url):
        try:
            next = ''
            #items = cache.get(telewizjadanet.chanels, 2)
            items = telewizjadanet.chanels()
            #control.log('Items %s' % items)
            self.list=items
            import operator
            self.list.sort(key=operator.itemgetter('title'))
            control.log('Ile %s' %len(self.list))
            return self.list

        except Exception as e:
            control.log('ERR TELEWIZJADA %s' % e)
            pass

    def ipla_list(self,url):
        try:
            next = ''
            #items = cache.get(ipla.ipla_chanels, 2)
            items = ipla.ipla_chanels()
            #control.log('Items %s' % items)
            self.list=items
            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        except Exception as e:
            control.log('ERR IPLA %s' % e)
            pass

    def looknij_list(self,url):
        try:
            next = ''
            #items = cache.get(weeb.weebchanels, 8640)
            items = looknij.weebchanels()
            #control.log('Items %s' % items)
            self.list=items
            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        except:
            pass

    def itivi_list(self, url):
        items = []
        next = ''

        try:
            #items = cache.get(weeb.weebchanels, 8640)
            items = itivi.itivichanels()
            #control.log('Items %s' % items)
            self.list=items
            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        except:
            pass

        try:
            result = client.request(url)
            result = re.compile('<a href="([^"]+)"><img alt="([^"]+)" src="([^"]+)" style="width:155px;height:155px; margin: 30px; border: 1px solid #CCC; border-radius: 30px;"/></a>').findall(result)
            if len(result)>0:
                for i in result:
                    try:
                        control.log('i %s' % i[1])
                        id = str(i[0])
                        id = id.encode('utf-8')

                        title = i[1].replace('Telewizja online - ','').replace('_',' ')
                        title = client.replaceHTMLCodes(title)
                        title = title.encode('utf-8')

                        poster = '0'
                        try:
                            poster = i[2]
                        except: pass
                        poster = poster.encode('utf-8')

                        try:
                            fanart = control.addonFanart()
                            fanart = fanart.encode('utf-8')
                        except:
                            fanart = '0'
                            fanart = fanart.encode('utf-8')
                            pass


                        plot = '0'
                        plot = plot.encode('utf-8')

                        tagline = '0'
                        tagline = client.replaceHTMLCodes(tagline)
                        try: tagline = tagline.encode('utf-8')
                        except: pass

                        self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'itivi', 'next': next})
                #control.log("##################><><><><> pierwsza item  %s" % self.list)
                    except:
                        pass


        except Exception as e:
            control.log('Error itiv tv.get2 %s' % e)
            pass
        import operator
        self.list.sort(key=operator.itemgetter('title'))
        return self.list

        return self.list

    def eskago_list(self, url):
        control.log('AAAi %s' % url)

        items = []
        next = ''

        try:
            result = client.request(url)
            result = re.compile('''<li><a href="([^"]+)" title="([^"]+)"><i class="big_icon"></i><img alt="([^"]+)" src="([^"]+)"/></a><span>([^"]+)</span></li>''').findall(result)
            control.log('AAAi %s' % result)

            if len(result)>0:
                for i in result:

                    control.log('i %s' % i[3])
                    id = str(i[0])
                    id = id.encode('utf-8')

                    title = i[1]
                    title = client.replaceHTMLCodes(title)
                    title = title.encode('utf-8')

                    poster = '0'
                    try:
                        poster = i[3]
                    except: pass
                    poster = poster.encode('utf-8')

                    try:
                        fanart = control.addonFanart()
                        fanart = fanart.encode('utf-8')
                    except:
                        fanart = '0'
                        fanart = fanart.encode('utf-8')
                        pass


                    plot = '0'
                    plot = plot.encode('utf-8')

                    tagline = '0'
                    tagline = client.replaceHTMLCodes(tagline)
                    try: tagline = tagline.encode('utf-8')
                    except: pass

                    self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'eskago', 'next': next})
                #control.log("##################><><><><> pierwsza item  %s" % self.list)

        except Exception as e:
            control.log('Error EskaGo tv.get2 %s' % e)
            pass
        #self.list.sort()
        import operator
        self.list.sort(key=operator.itemgetter('title'))
        #control.log("##################><><><><> pierwsza item  %s" % newlist)

        return self.list

    def wizja_list(self, url):
        try:
            next = ''
            items = wizja.wizjachanels()

            for item in items:
                id = item['id']
                title = item['title']
                title = client.replaceHTMLCodes(title)

                poster = '0'
                try:
                    poster = item['img']
                except: pass
                poster = poster.encode('utf-8')

                try:
                    fanart = control.addonFanart()
                    fanart = fanart.encode('utf-8')
                except:
                    fanart = '0'
                    fanart = fanart.encode('utf-8')
                    pass


                plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = None
                if tagline == None and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'wizja', 'next': next})
                #control.log("##################><><><><> pierwsza item  %s" % self.list)

            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        except:
            pass

    def weeb_list(self, url):
        try:
            next = ''
            #items = cache.get(weeb.weebchanels, 8640)
            items = weeb.weebchanels()
            #control.log('Items %s' % items)
            self.list=items
            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        except:
            pass

    def yoy_list(self, url):
        #try:
            next = ''
            items = cache.get(yoy.getchanels, 4)
            #items = yoy.getchanels()

            for item in items:
                id = item['id']
                title = item['title']
                title = client.replaceHTMLCodes(title)

                poster = '0'
                try:
                    poster = 'http://yoy.tv/channel/covers/%s.jpg' % id
                except: pass
                poster = poster.encode('utf-8')

                try:
                    fanart = control.addonFanart()
                except:
                    fanart = '0'
                    pass
                fanart = fanart.encode('utf-8')

                plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = None
                if tagline == None and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'yoy', 'next': next})
                #control.log("##################><><><><> yoy item  %s" % self.list)

            import operator
            self.list.sort(key=operator.itemgetter('title'))
            return self.list

        #except:
        #    pass

    def videostar_list(self, url):
        items = []

        try:
            result = videostar.get('/channels/list/ios-plus')
            result = json.loads(result)
            control.log('A tv.get %s' % result)
            if result['status'] == 'error':
                control.infoDialog(result['errors'][0]['msg'])
                raise Exception(result['errors'][0]['msg'])
            for i in result['channels']:
                control.log('Result %s' % i)
                if i['access_status']== 'subscribed' or i['access_status']== 'free':
                    try: items.append(i)
                    except: pass
            if len(items) == 0:
                items = result
        except Exception as e:
            control.log('Error tv.get %s' % e)
        next = ''

        for item in items:
            control.log('Result %s' % item)

            try:
                id = str(item['id'])
                id = id.encode('utf-8')

                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                poster = '0'
                try:
                    poster = item['thumbnail']
                except: pass
                poster = poster.encode('utf-8')

                try:
                    fanart = control.addonFanart()
                except:
                    fanart = '0'
                    pass
                fanart = fanart.encode('utf-8')

                plot = '0'
                try: plot = item['overview']
                except: pass
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: tagline = item['tagline']
                except: tagline = None
                if tagline == None and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'videostar', 'next': next})
                #control.log("##################><><><><> pierwsza item  %s" % self.list)

            except Exception as e:
                control.log('Error videostar tv.get2 %s' % e)
                pass
        #self.list.sort()
        import operator
        self.list.sort(key=operator.itemgetter('title'))
        #control.log("##################><><><><> pierwsza item  %s" % newlist)

        return self.list

    def pierwsza_list(self, url):
        #items = cache.get(pierwsza.chanels, 2)
        items = pierwsza.chanels()
        next = ''

        for item in items:
            try:
                id = str(item['id'])
                id = id.encode('utf-8')

                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                poster = '0'
                try:
                    poster = item['thumbail']
                    poster = self.pierwsza_link+poster
                except: pass
                poster = poster.encode('utf-8')

                try:
                    fanart = control.addonFanart()
                except:
                    fanart = '0'
                    pass
                fanart = fanart.encode('utf-8')

                plot = '0'
                try: plot = item['overview']
                except: pass
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: tagline = item['tagline']
                except: tagline = None
                if tagline == None and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'name':title, 'tagline': tagline,  'poster': poster, 'fanart': fanart, 'id':id, 'service':'pierwsza', 'next': next})
                #control.log("##################><><><><> pierwsza item  %s" % self.list)

            except:
                #control.log("##################><><><><> pierwsza item  %s" % newlist)
                pass
        import operator
        self.list.sort(key=operator.itemgetter('title'))
        return self.list

    def widget(self):
        setting = control.setting('movie_widget')

        if setting == '2':
            self.get(self.featured_link)
        elif setting == '3':
            self.get(self.trending_link)
        else:
            self.get(self.added_link)

    def favourites(self):
        try:
            items = favourites.getFavourites('movies')
            self.list = [i[1] for i in items]

            for i in self.list:
                if not 'name' in i: i['name'] = '%s (%s)' % (i['title'], i['year'])
                try: i['title'] = i['title'].encode('utf-8')
                except: pass
                try: i['name'] = i['name'].encode('utf-8')
                except: pass
                if not 'duration' in i: i['duration'] = '0'
                if not 'imdb' in i: i['imdb'] = '0'
                if not 'tmdb' in i: i['tmdb'] = '0'
                if not 'tvdb' in i: i['tvdb'] = '0'
                if not 'tvrage' in i: i['tvrage'] = '0'
                if not 'poster' in i: i['poster'] = '0'
                if not 'banner' in i: i['banner'] = '0'
                if not 'fanart' in i: i['fanart'] = '0'

            self.worker()
            self.list = sorted(self.list, key=lambda k: k['title'])
            self.movieDirectory(self.list)
        except:
            return

    def search(self, query=None):
        #try:
            if query == None:
                t = control.lang(30201).encode('utf-8')
                k = control.keyboard('', t) ; k.doModal()
                self.query = k.getText() if k.isConfirmed() else None
            else:
                self.query = query

            if (self.query == None or self.query == ''): return


            url = self.search_link % (urllib.quote_plus(self.query))
            self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

            self.worker()
            self.movieDirectory(self.list)
            return self.list
        #except:
        #    return

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass
        #control.log('@@ TRAKT LIST %s - %s' %(userlists,activity))
        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '': raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        #self.addDirectory(self.list, queue=True)
        self.addDirectory(self.list)

        return self.list

    def trakt_list(self, url, user):
        #control.log('### TRAKT LISTS')
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full,images'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTrakt(u)
            result = json.loads(result)

            items = []
            for i in result:
                try: items.append(i['movie'])
                except: pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            p = str(int(q['page']) + 1)
            if p == '5': raise Exception()
            q.update({'page': p})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                poster = '0'
                try: poster = item['thumbail']
                except: pass
                poster = poster.encode('utf-8')

                fanart = '0'
                try: fanart = item['thumbail']
                except: pass
                fanart = fanart.encode('utf-8')

                plot = '0'
                try: plot = item['overview']
                except: pass
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                try: tagline = item['tagline']
                except: tagline = None
                if tagline == None and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'genre': '0', 'plot': plot, 'tagline': tagline, 'name': name, 'poster': poster, 'fanart': fanart, 'next': next})
            except:
                pass

        return self.list

    def trakt_user_list(self, url, user):
        try:
            result = trakt.getTrakt(url)
            items = json.loads(result)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['name'].lower()))
        return self.list

    def imdb_list(self, url, idx=True):
        try:
            if url == self.imdbwatchlist_link:
                def imdb_watchlist_id(url):
                    return re.compile('/export[?]list_id=(ls\d*)').findall(client.request(url))[0]
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url


            headers = {'Accept-Language': 'en-US'}
            result = str(client.request(url,headers=headers))

            try:
                if idx == True: raise Exception()
                pages = client.parseDOM(result, 'div', attrs = {'class': 'desc'})[0]
                pages = re.compile('Page \d+? of (\d*)').findall(pages)[0]
                for i in range(1, int(pages)):
                    u = url.replace('&start=1', '&start=%s' % str(i*100+1))
                    result += str(client.request(u))
            except:
                pass

            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'tr', attrs = {'class': '.+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'span', attrs = {'class': 'pagination'})
            next += client.parseDOM(result, 'div', attrs = {'class': 'pagination'})
            name = client.parseDOM(next[-1], 'a')[-1]
            if 'laquo' in name: raise Exception()
            next = client.parseDOM(next, 'a', ret='href')[-1]
            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                try: title = client.parseDOM(item, 'a')[1]
                except: pass
                try: title = client.parseDOM(item, 'a', attrs = {'onclick': '.+?'})[-1]
                except: pass
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs = {'class': 'year_type'})[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = 'tt' + re.sub('[^0-9]', '', imdb.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                poster = '0'
                try: poster = client.parseDOM(item, 'img', ret='src')[0]
                except: pass
                try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except: pass
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})
                genre = client.parseDOM(genre, 'a')
                genre = ' / '.join(genre)
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = re.compile('(\d+?) mins').findall(item)[-1]
                except: duration = '0'
                duration = client.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')

                try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except: rating = '0'
                try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except: rating = '0'
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': 'rating rating-list'})[0]
                except: votes = '0'
                try: votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except: mpaa = '0'
                try: mpaa = client.parseDOM(mpaa, 'span', ret='title')[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                director = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                director += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try: director = [i for i in director if 'Director:' in i or 'Dir:' in i][0]
                except: director = '0'
                director = director.split('With:', 1)[0].strip()
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                cast = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                cast += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try: cast = [i for i in cast if 'With:' in i or 'Stars:' in i][0]
                except: cast = '0'
                cast = cast.split('With:', 1)[-1].strip()
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []: cast = '0'

                plot = '0'
                try: plot = client.parseDOM(item, 'span', attrs = {'class': 'outline'})[0]
                except: pass
                try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except: pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                fanart = 'http://films4u.org/imdb/bgs/'+imdb+'.jpg'
                fanart = fanart.encode('utf-8')


                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': '0', 'cast': cast, 'plot': plot, 'tagline': tagline, 'name': name, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'tvrage': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass

        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'div', attrs = {'class': 'list_name'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        return self.list

    def scn_list(self, url):

        def predb_items():
            try:
                years = [(self.datetime).strftime('%Y'), (self.datetime - datetime.timedelta(days = 365)).strftime('%Y')]
                months = (self.datetime - datetime.timedelta(days = 180)).strftime('%Y%m%d')

                result = ''
                for i in years:
                    result += client.request(self.scn_page % (str(i), '1'))
                    result += client.request(self.scn_page % (str(i), '2'))

                items = client.parseDOM(result, 'div', attrs = {'class': 'post'})
                items = [(client.parseDOM(i, 'a', attrs = {'class': 'p-title'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in items]
                items = [(i[0][0], i[1][0]) for i in items if len(i[0]) > 0 and len(i[1]) > 0]
                items = [(re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|3D)(\.|\)|\]|\s)(.+)', '', i[0]), re.compile('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]').findall(i[0]), re.sub('[^0-9]', '', i[1])) for i in items]
                items = [(i[0], i[1][-1], i[2]) for i in items if len(i[1]) > 0]
                items = [i for i in items if int(months) <= int(i[2])]
                items = sorted(items,key=lambda x: x[2])[::-1]
                items = [(re.sub('(\.|\(|\[|LIMITED|UNCUT)', ' ', i[0]).strip(), i[1]) for i in items]
                items = [x for y,x in enumerate(items) if x not in items[:y]]
                items = items[:150]

                return items
            except:
                return


        def predb_list(i):
            try:
                url = self.imdb_by_query % (urllib.quote_plus(i[0]), i[1])
                item = client.request(url, timeout='10')
                item = json.loads(item)

                title = item['Title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['Year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                name = '%s (%s)' % (title, year)
                try: name = name.encode('utf-8')
                except: pass

                imdb = item['imdbID']
                if imdb == None or imdb == '' or imdb == 'N/A': raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                poster = item['Poster']
                if poster == None or poster == '' or poster == 'N/A': poster = '0'
                if not ('_SX' in poster or '_SY' in poster): poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = poster.encode('utf-8')

                genre = item['Genre']
                if genre == None or genre == '' or genre == 'N/A': genre = '0'
                genre = genre.replace(', ', ' / ')
                genre = genre.encode('utf-8')

                duration = item['Runtime']
                if duration == None or duration == '' or duration == 'N/A': duration = '0'
                duration = re.sub('[^0-9]', '', str(duration))
                duration = duration.encode('utf-8')

                rating = item['imdbRating']
                if rating == None or rating == '' or rating == 'N/A' or rating == '0.0': rating = '0'
                rating = rating.encode('utf-8')

                votes = item['imdbVotes']
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None or votes == '' or votes == 'N/A': votes = '0'
                votes = votes.encode('utf-8')

                mpaa = item['Rated']
                if mpaa == None or mpaa == '' or mpaa == 'N/A': mpaa = '0'
                mpaa = mpaa.encode('utf-8')

                director = item['Director']
                if director == None or director == '' or director == 'N/A': director = '0'
                director = director.replace(', ', ' / ')
                director = re.sub(r'\(.*?\)', '', director)
                director = ' '.join(director.split())
                director = director.encode('utf-8')

                writer = item['Writer']
                if writer == None or writer == '' or writer == 'N/A': writer = '0'
                writer = writer.replace(', ', ' / ')
                writer = re.sub(r'\(.*?\)', '', writer)
                writer = ' '.join(writer.split())
                writer = writer.encode('utf-8')

                cast = item['Actors']
                if cast == None or cast == '' or cast == 'N/A': cast = '0'
                cast = [x.strip() for x in cast.split(',') if not x == '']
                try: cast = [(x.encode('utf-8'), '') for x in cast]
                except: cast = []
                if cast == []: cast = '0'

                plot = item['Plot']
                if plot == None or plot == '' or plot == 'N/A': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline, 'name': name, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'tvrage': '0', 'poster': poster, 'banner': '0', 'fanart': '0'})
            except:
                pass


        try:
            items = cache.get(predb_items, 24)

            start = re.compile('start=(\d*)').findall(url)[-1]
            start = int(start)

            if len(items) > (start + 30): next = self.scn_link + '?start=%s' % (start + 30)
            else: next = ''
        except:
            return

        threads = []
        for i in range(start - 1, start + 29):
            try: threads.append(workers.Thread(predb_list, items[i]))
            except: pass
        [i.start() for i in threads]
        [i.join() for i in threads]

        for i in range(0, len(self.list)): self.list[i].update({'next': next})

        return self.list

    def worker(self):

        self.meta = []
        total = len(self.list)
        #control.log("##################><><><><> WORKER TOTAL  %s" % total)


        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.info_lang)

        for r in range(0, total, 25):
            threads = []
            for i in range(r, r+25):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        self.list = [i for i in self.list if not i['imdb'] == '0']
        #control.log("##################><><><><> WORKER   %s" % str(len(self.meta)))

        if len(self.meta) > 0: metacache.insert(self.meta)

    def super_info(self, i):
        try:
            #control.log("##################><><><><> META ID  %s" % str(i))
            zero ='0'.encode('utf-8')

            if self.list[i]['metacache'] == True: raise Exception()

            try: imdb = self.list[i]['imdb']
            except: imdb = '0'

            if not imdb == '0': url = self.imdb_info_link % imdb
            else: raise Exception()

            item = client.request(url, timeout='10')
            item = json.loads(item)
            #control.log("##################><><><><> META TITLE  %s" % item['Title'])
            #control.log("##################><><><><> META ALL %s" % item)

            imdb = item['imdbID']
            if imdb == '' or imdb == None: imdb = '0'
            if not imdb == '0': imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
            imdb = imdb.encode('utf-8')
            if not imdb == '0': self.list[i].update({'imdb': imdb, 'code': imdb})

            """
            try:
                #url2 = 'http://webservice.fanart.tv/v3/movies/%s?api_key=%s' % (imdb, self.fanarttv_key)
                #item2 = client.request(url2, timeout='10')
                #item2 = json.loads(item2)
                #control.log("><><><><> ITEM4  %s" % item2['moviebackground'][0]['url'])

            except:
                pass

            try:
                tmdb = item2['tmdb_id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                if not tmdb == '0': self.list[i].update({'tmdb': tmdb})
            except:
                tmdb = zero

            """
            try:
                poster = item['Poster']
                if poster == '' or poster == None: poster = '0'
                #if not poster == '0': poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')
                if not poster == '0': self.list[i].update({'poster': poster})
            except:
                poster = zero

            """
            try:
                fanart = item2['moviebackground'][0]['url']
                if fanart == '' or fanart == None: fanart = '0'
                #if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                if not fanart == '0' and self.list[i]['fanart'] == '0': self.list[i].update({'fanart': fanart})
            except:
                fanart = zero
            """

            try:
                if not imdb == '0':
                    fanart = 'http://films4u.org/imdb/bgs/'+imdb+'.jpg'
                    fanart= fanart.encode('utf-8')

                else:
                    fanart = zero
            except:
                fanart = zero

            #    http://fanart.filmkodi.com/tt0006333.jpg
            try:
                premiered = item['Released']
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except: premiered = '0'
            if premiered == '' or premiered == None: premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})

            #studio = item['production_companies']
            #try: studio = [x['name'] for x in studio][0]
            #except:
            studio = '0'
            #if studio == '' or studio == None: studio = '0'
            studio = studio.encode('utf-8')
            #if not studio == '0': self.list[i].update({'studio': studio})

            try: genre = item['Genre']
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: duration = str(item['Runtime'].replace(' min',''))
            except: duration = '0'
            if duration == '' or duration == None: duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})

            try: rating = str(item['imdbRating'])
            except: rating = '0'
            if rating == '' or rating == None: rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})

            try:
                votes = str(item['imdbVotes'])
                votes = str(format(int(votes),',d'))
            except:
                votes = '0'
            if votes == '' or votes == None: votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})


            try:
                mpaa = item['Country']
            except:
                mpaa = '0'
            if mpaa == '' or mpaa == None: mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})

            try: cast = item['Actors']
            except: cast = '0'
            if cast == None or cast == '' or cast == 'N/A': cast = '0'
            cast = [x.strip() for x in cast.split(',') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []
            if cast == []: cast = '0'
            if not cast == '0': self.list[i].update({'cast': cast})

            try: writer = item['Writer']
            except: writer = '0'
            if writer  == '' or writer == None: writer= '0'
            writer = writer.encode('utf-8').replace(', ', ' / ')
            if len(writer) > 0: self.list[i].update({'writer': writer})


            """
            tagline = item['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline == None: tagline = '0'
            try: tagline = tagline.encode('utf-8')
            except: pass
            if not tagline == '0': self.list[i].update({'tagline': tagline})
            """
            plot = item['Plot']
            if plot == '' or plot == None: plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})

            director = item['Director']
            if director == '' or director == None or director == []: director = '0'
            director = director.encode('utf-8')
            if not director == '0': self.list[i].update({'director': director})

            #self.meta.append({'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.info_lang, 'item': {'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
            self.meta.append({'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'lang': self.info_lang, 'item': {'code': imdb, 'imdb': imdb, 'tmdb': '0', 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': zero}})
            #control.log("><><><><> ITEM META IMDB %s" % imdb)

        except:
            pass

    def movieDirectory(self, items):
        if items == None or len(items) == 0: return

        isFolder = True if control.setting('autoplay') == 'false' and control.setting('host_select') == '1' else False
        isFolder = False if control.window.getProperty('PseudoTVRunning') == 'True' else isFolder

        playbackMenu = control.lang(30204).encode('utf-8') if control.setting('autoplay') == 'true' else control.lang(30203).encode('utf-8')

        cacheToDisc = False if not action == 'movieSearch' else True

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        sysaddon = sys.argv[0]

        #try:
        #    favitems = favourites.getFavourites('movies')
        #    favitems = [i[0] for i in favitems]
        #except:
        #    pass

        for i in items:
            try:
                label = i['name']
                syshandle = int(sys.argv[1])
                sysname = urllib.quote_plus(label)
                systitle = urllib.quote_plus(i['title'])
                #imdb, tmdb, year = i['imdb'], i['tmdb'], i['year']
                service = i['service']

                poster, fanart = i['poster'], i['fanart']
                if poster == '0': poster = addonPoster

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&name=%s&title=%s&service=%s&meta=%s' % (sysaddon, sysname, systitle, service, sysmeta)
                sysurl = urllib.quote_plus(url)

                item = control.item(label=label, iconImage=poster, thumbnailImage=poster)
                try: item.setArt({'poster': poster})
                except: pass

                if settingFanart == 'true' and not fanart == '0':

                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)


                isFolder = False
                item.setInfo(type='Video', infoLabels = meta)
                item.setProperty('IsPlayable', 'true')
                #item.addContextMenuItems(cm, replaceItems=True)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()
            url = '%s?action=movies&url=%s' % (sysaddon, urllib.quote_plus(url))
            addonNext = control.addonNext()
            item = control.item(label=control.lang(30213).encode('utf-8'), iconImage=addonNext, thumbnailImage=addonNext)
            item.addContextMenuItems([], replaceItems=False)
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass


        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=cacheToDisc)
        #control.directory(syshandle)
        #views.setView('movies', {'skin.confluence': 500})


    def addDirectory(self, items):
        if items == None or len(items) == 0: return

        sysaddon = sys.argv[0]
        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()

        for i in items:
            try:
                try: name = control.lang(i['name']).encode('utf-8')
                except: name = i['name']

                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                try: cm.append((control.lang(30211).encode('utf-8'), 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except: pass

                item = control.item(label=name, iconImage=thumb, thumbnailImage=thumb)
                item.addContextMenuItems(cm, replaceItems=False)
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
            except:
                pass

        control.directory(int(sys.argv[1]), cacheToDisc=True)


