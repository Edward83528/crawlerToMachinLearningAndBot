import urllib.request, urllib.parse

data = {
  'name' : 'David',
  'password' : '1234'
}
data = bytes( urllib.parse.urlencode( data ).encode() )

req1 = urllib.request.Request('http://jumpin.cc/HelloForm/post.php')
handler = urllib.request.urlopen(req1,data);
cookie = handler.headers.get('Set-Cookie')
print( handler.read().decode( 'utf-8' ) );

req2 = urllib.request.Request('http://jumpin.cc/HelloForm/content.php')
req2.add_header('cookie', cookie)
handler = urllib.request.urlopen(req2);
print( handler.read().decode( 'utf-8' ) );
