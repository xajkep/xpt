<!DOCTYPE>
<html>
<head>

</head>
<body>
<iframe srcdoc="<?php
$c = $_GET['c'];
$c = htmlentities($c, ENT_QUOTES);
echo $c;
?>" ></iframe>
</body>
</html>
