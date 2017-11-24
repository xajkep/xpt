<!DOCTYPE>
<html>
<head>

</head>
<body>
<object data="data:text/html;<?php
$c = $_GET['c'];
$c = htmlentities($c, ENT_QUOTES);
echo $c;
?>"></object>
</body>
</html>
