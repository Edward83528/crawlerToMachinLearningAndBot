import urllib.request, urllib.parse

data = {
  'name' : 'David',
  'password' : '1234'
}
data = bytes( urllib.parse.urlencode( data ).encode() )
handler = urllib.request.urlopen( 'http://jumpin.cc/HelloForm/post.php', data );
print( handler.read().decode( 'utf-8' ) );