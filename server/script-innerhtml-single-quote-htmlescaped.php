<!DOCTYPE>
<html>
<head>

</head>
<body>
<div id='d'></div><script>var a='<?php
$c = $_GET['c'];
$c = htmlentities($c, ENT_QUOTES);
echo $c;
?>';document.getElementById('d').innerHTML = a;</script>
</body>
</html>
