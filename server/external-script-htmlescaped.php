<!DOCTYPE>
<html>
<head>

</head>
<body>
<?php
$c = "".$_GET['c']."";
$c = htmlentities($c, ENT_QUOTES);
file_put_contents(__DIR__.'/tmp.php', $c);
?>
<script src='tmp.php'></script>
</body>
</html>
