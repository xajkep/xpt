<!DOCTYPE>
<html>
<head>

</head>
<body>
<script>var bonjour = "<?php
$c = $_GET['c'];
$c = htmlentities($c, ENT_QUOTES);
echo $c;
?>";</script>
</body>
</html>
