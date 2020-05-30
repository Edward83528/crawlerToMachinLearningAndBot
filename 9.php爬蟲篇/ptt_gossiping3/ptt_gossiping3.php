<?php
  $p = isset($_GET['p']) ? $_GET['p']+0 : 1;
  if (!function_exists('curl_init'))
  {
    die('Sorry cURL is not installed!');
  }  
  $GLOBALS['res'] = array();
  $ch = curl_init();
  curl_setopt($ch,CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36');
  curl_setopt($ch,CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
  curl_setopt($ch,CURLOPT_COOKIESESSION, true);
  curl_setopt($ch,CURLOPT_COOKIE, 'over18=1; Path=/'); 
  
  fetchPTT($ch,$p);
  curl_close($ch);
  
  function fetchPTT($ch, $p=1)
  {
    for($i=0;$i<$p;$i++)
    {
      if($i==0)
      {
        $url = 'https://www.ptt.cc/bbs/Gossiping/index.html';
      }
      echo 'i='.$i.'<br>';
      echo 'uri='.$url.'<br>';
      curl_setopt($ch,CURLOPT_URL,$url);
      $html_data=curl_exec($ch);
      $aryTemp01 = @explode('<div class="title">',$html_data);
      for($j=1;$j<count($aryTemp01);$j++)
      {
        $aryTemp02 = @explode('</a>',$aryTemp01[$j]);
        $aryTemp03 = @explode('>',$aryTemp02[0]);
        $title = stripNewline($aryTemp03[1]);
        $aryTemp04 = @explode('href="',$aryTemp01[$j]);
        $aryTemp05 = @explode('"',$aryTemp04[1]);
        $url = 'https://www.ptt.cc'.stripNewline($aryTemp05[0]);
        if($title!='')
        {
          $GLOBALS['res'][$url]=$title;
        }
      }
      foreach($GLOBALS['res'] as $key => $value)
      {
        echo 'title='.$value.'<br>url='.$key.'<hr>';
      }
      $aryTemp11 = @explode('btn wide" href="',$html_data);
      for($k=1;$k<count($aryTemp11);$k++)
      {
        if(preg_match('/'.urldecode('%E4%B8%8A%E9%A0%81').'/i',$aryTemp11[$k]))
        {
          $aryTemp12 = @explode('">',@$aryTemp11[$k]);
          $url = preg_replace('#(\\\r|\\\r\\\n|\\\n)#', '', trim($aryTemp12[0]));
          $url = preg_replace("/[\n\r]/","",$url).'';
          $url = 'https://www.ptt.cc'.$url;
          echo 'next page='.$url.'<hr>';
          break;
        }
      }
      sleep(1);
    }
  }
  
  function stripNewline($s)
  {
    $s = preg_replace('#(\\\r|\\\r\\\n|\\\n)#','',trim(strip_tags($s)));
    $s = preg_replace("/[\n\r]/","",$s);
    return $s;
  }
  
  //echo 'HTTP GET='.htmlspecialchars($html_data);
?>