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
  echo 'HTTP GET='.htmlspecialchars($html_data);
?>