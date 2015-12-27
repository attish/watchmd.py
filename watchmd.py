#!/usr/bin/env python

import web as webpy
import os
import sys
import threading
import time
import datetime
import time
import random
import markdown
import codecs

count = 0

urls = (
    '/', 'Frame',
    '/longpoll/([0-9]+)', 'LongPoll',
    '/stop', 'Stop',
    '/jquery.js', 'jQuery'
    )

def file_mtime(fname):
    return datetime.datetime.fromtimestamp(os.path.getmtime(fname))

def file_data(fname):
    with codecs.open(fname, encoding="utf-8") as f:
        data = f.read()
    return markdown.markdown(data, tab_length=2)

class LongPoll:
    def GET(self, session_id):
        global last_refresh, filename
        webpy.header('Content-type', 'text/html')
        filename = sys.argv[2]
        last_seen = file_mtime(filename)
        while last_seen == file_mtime(filename):
            time.sleep(1)
        return file_data(sys.argv[2])

class Stop:
    def GET(self):
        os._exit(0)

class jQuery:
    def GET(self):
        raise webpy.seeother('https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js')

class Frame:
    def GET(self):
        randnum = random.randint(0, 2000000000)
        data = file_data(sys.argv[2])
        page = """
        <html>
            <head>
                <title>Markdown viewer</title>
                <script type="text/javascript" src="/jquery.js"></script>
            </head>
            <body>
                <input name="stop" type="button" value="Stop" onclick="stop()"></input>
                <div id="closed" style="width: 30em; background-color: aliceblue; border: 1px solid lightblue; margin: 3em auto; padding: 1em; color: blue; text-align: center; display: none">The server is stopped. You may close the window.</div>
                <div id="content">%s</div>
                <script type="text/javascript">
                    function stop() {
                        $.ajax({url: '/stop'});
                        $('#stop').hide();
                        $('#closed').show(400);
                        $('#content').css('color', 'lightgrey');
                    }


                    function getContent() {
                        $.ajax({
                            url: '/longpoll/%d',
                            dataType: 'text',
                            type: 'get',
                            success: function(doc){
                                $('#content').html(doc);
                                setTimeout('getContent()', 100);
                                }
                        });
                    }
                    getContent();
                </script>
            </body>
        </html>
        """
        return page % (data, randnum)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        filename = sys.argv[2]
    else:
        print "Usage: watchmd.py <port_num> <filename>"
        sys.exit(1)
    webapp = webpy.application(urls, globals())
    webapp.run()

