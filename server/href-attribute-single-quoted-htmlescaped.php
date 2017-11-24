<!DOCTYPE>
<html>
<head>

</head>
<body>
<a href='<?php
$c = $_GET['c'];
$c = htmlentities($c, ENT_QUOTES);
echo $c;
?>'>click</a>
</body>
</html>
