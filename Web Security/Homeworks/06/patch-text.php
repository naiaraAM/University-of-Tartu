<?php

$hostname = '';
$filename = '';
$error = '';
if (isset($_POST['url'])) {
    $url = $_POST['url'];
    if (filter_var($url, FILTER_VALIDATE_URL) && substr($url, 0, 8) === "https://") {
       $hostname = "https://".parse_url($url)['host'];
       $filename = rawurldecode(basename(parse_url($url)['path']));
    } else {
       $error = 'Invalid URL';
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insecure dialog</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }

        .container {
            width: 80%;
            max-width: 600px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }

        .url-input {
            width: 95%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }

        .dialog-block {
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .dialog-block p {
            white-space: nowrap;
            overflow: hidden;
            font-size: 16px;
            color: #333;
        }

        .error {
            color: red;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method=POST>
        <input type="text" name="url" class="url-input" placeholder="Enter file URL here" value="<?php echo(htmlspecialchars($url)); ?>" />
	</form>
<?php

if (strlen($error)) {
    echo '<div id="error-message" class="error">'.htmlspecialchars($error).'</div>';
}

if (strlen($hostname)) {

echo '
        <div class="dialog-block">
            <p>You are about to download '.htmlspecialchars($filename).' from '.htmlspecialchars($hostname).'</p>
';

}
?>
        </div>
    </div>
</body>
</html>
