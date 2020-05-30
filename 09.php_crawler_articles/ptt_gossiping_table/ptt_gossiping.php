<?php
  if (!function_exists('curl_init'))
  {
    die('Sorry cURL is not installed!');
  }
  $ch = curl_init();
  $url = 'https://www.ptt.cc/bbs/Gossiping/index.html';
  curl_setopt($ch,CURLOPT_URL,$url);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
  curl_setopt($ch,CURLOPT_COOKIE, 'over18=1; Path=/'); 
  $html_data=curl_exec($ch);
  curl_close($ch);
  
  $res = array();
  $aryTemp01 = @explode('<div class="title">',$html_data);
  for($i=1;$i<count($aryTemp01);$i++)
  {
    $aryTemp02 = @explode('</a>',$aryTemp01[$i]);
    $aryTemp03 = @explode('>',$aryTemp02[0]);
    $title = $aryTemp03[1];
    $aryTemp04 = @explode('href="',$aryTemp01[$i]);
    $aryTemp05 = @explode('"',$aryTemp04[1]);
    $url = $aryTemp05[0];
    $res[$url]=$title;
  }
  
  foreach($res as $key => $value)
  {
    //echo 'title='.$value.'<br>url='.$key.'<hr>';
  }
  //echo 'HTTP GET='.htmlspecialchars($html_data);
?>
<html>
    <head>
        <title>FixedHeaderTable Test</title>
        <link href="css/960.css" rel="stylesheet" media="screen" />
        <link href="ss/defaultTheme.css" rel="stylesheet" media="screen" />
        <link href="css/myTheme.css" rel="stylesheet" media="screen" />
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
        <script src="jquery.fixedheadertable.js"></script>
        <script src="demo.js"></script>
    </head>
    <body>
      <div class="grid_8 height250">
          <table class="fancyTable" id="myTable01" cellpadding="0" cellspacing="0">
              <thead>
                  <tr>
                      <th>Title</th>
                      <th>Link</th>
                  </tr>
              </thead>
              <tbody>
<?php
  foreach($res as $key => $value)
  {
    echo '<tr>';
    echo '<td>'.$value.'</td>';
    echo '<td>'.$key.'</td>';
    echo '</tr>';
    //echo 'title='.$value.'<br>url='.$key.'<hr>';
  }
?>
              </tbody>
          </table>
        </div>
        <div class="clear"></div>
      </div>
    </body>
</html>
