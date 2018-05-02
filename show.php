<html>
<head>
	<style type="text/css">	
		/* body {
			text-align: center;
		} */

		h1 {
			/*text-align: center;*/
			position: relative;
			top: 10%;
			text-shadow: 5px 5px 5px #888888;
		}
	</style>
	<script src="js/jquery-3.3.1.min.js"></script>
	<meta name="viewport" charset="UTF-8" content="width=device-width,initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" />
</head>

<body>
	<h2>Dataset:</h2>
	<p><b>CIFAR10</b></p>
	<p>data -- a 10000x3072 numpy array of uint8s. Each row of the array stores a 32x32 colour image. The first 1024 entries contain the red channel values, the next 1024 the green, and the final 1024 the blue. The image is stored in row-major order, so that the first 32 entries of the array are the red channel values of the first row of the image.</p>
	<p>labels -- a list of 10000 numbers in the range 0-9. The number at index i indicates the label of the ith image in the array data.</p>

	<h2>Your image:</h2>
	<img src="testing/<?php echo $_GET['text'] ?>" alt="image" width="150" height="150" >
	<p><b>USER:</b><?php echo $_GET['name'] ?> <b>IMG:</b><?php echo $_GET['text'] ?></p>

	<?php
	exec("python sketch.py ". $_GET['text'] . " " . $_GET['name'],$output);
	
	echo "<h2>HashCode:</h2>";
	echo "<p>" . $output[1] . "<p>";

	echo "<h2>Retrieval result:</h2>";
	echo "<p> The conversion process takes <b>" . $output[0] . "</b> seconds , retrieval costs <b>" .$output[2] . "</b> seconds. ";
	echo "<br>Powered by Alibaba ECS with Intel(R) Xeon(R) CPU E5-2682 v4 @ 2.50GHz (1 core) </p>"
	?>
	<img id="resu" src="result/<?php echo $_GET['name'] ?>.jpg" alt="resu" width="100%" >

	<h2>Training loss:</h2>
	<p>下图中的 <b>easybasic</b> 指代本次retrieval所采用的网络结构在训练过程中的目标函数收敛情况</p>
	<img id="lossimg" src="loss.png" alt="lossimg" width="100%" >
	
	<h2 align="center"><a href="http://gongbiao.cc/hash">BACK</a></h2>
	<p align="center" id="ppp">best wishes from gongbiao.cc</p>

	<script>
		if(window.innerWidth>640){
			$("#resu").attr("width","640");
			// $("#resu").attr("height","480");
		}
		if(window.innerWidth>802){
			$("#lossimg").attr("width","802");
			// $("#lossimg").attr("height","857");
		}
	</script>


</body>

</html>