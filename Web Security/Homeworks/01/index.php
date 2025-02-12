<?php
if (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off') {
    header("Location: https://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'], true, 301);
    exit();
}

# Header space
header("Strict-Transport-Security: max-age=31536000; includeSubDomains; preload");

# Cookies space
setcookie("theme", "dark", time() + 3600, "/", ".websec.ee", true, false);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello word</title>
</head>
<body>
<h1>Hello world!</h1>
<p>Cookie set to force <a href="https://websec.ee">https://websec.ee</a> to be always in dark mode</p>
</body>
</html>
