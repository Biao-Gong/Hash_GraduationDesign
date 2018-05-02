<?php
	// echo "12";
	// echo $_FILES["file"]["size"]. $_FILES["file"]["tmp_name"];
	move_uploaded_file($_FILES["file"]["tmp_name"],"/var/www/hash/testing/".$_POST["text"]);
?>