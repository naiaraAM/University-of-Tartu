<?php

$authenticated = false; // initialize variable

if ($_SERVER['REQUEST_METHOD'] !== 'GET' && $_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method Not Allowed';
    exit();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($username === 'user' && $password === 'pass') {
        $authenticated = true;

        // Generate a secure random session token
        $cookie_val = bin2hex(random_bytes(16));

        // Set cookie with specified attributes (if not specified, default values are used)
        setcookie('__Host-session', $cookie_val, [
            'expires' => time() + 3600,
            'path' => '/',
            'secure' => true,
            'httponly' => true,
            'samesite' => 'Strict'
        ]);

        // Store username in session for obtaining it in next requests
        $_SESSION['username'] = $username;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Check if the session cookie exists
    if (isset($_COOKIE['__Host-session'])) {
        $cookie = $_COOKIE['__Host-session'];
        // Validate session cookie format
        if (strlen($cookie) !== 32 || !ctype_xdigit($cookie)) {
            $authenticated = false; // go back to login page
        } else {
            $authenticated = true;
        }
    }

    // Do log out
    if (isset($_GET['action']) && $_GET['action'] === 'logout') {
        setcookie('__Host-session', '', [
            'expires' => time() - 3600,
            'path' => '/',
            'secure' => true,
            'httponly' => true,
            'samesite' => 'Strict'
        ]);
        header('Location: user_and_pass.php');

        $authenticated = false;
    }
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Input</title>
</head>
<body>
<h1 id="topMessage"><?php echo $authenticated ? "Welcome" : "Introduce the requested information"; ?></h1>

<?php if ($authenticated): ?>
    <p>Hello, user</p>
    <form id="logoutForm" action="user_and_pass.php" method="get">
        <input type="hidden" name="action" value="logout">
        <input type="submit" value="Logout">
    </form>
<?php else: ?>
    <form id="loginForm" action="user_and_pass.php" method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>

    <?php if ($_SERVER['REQUEST_METHOD'] === 'POST'): ?>
        <h2 style="color: red;">Incorrect, try again</h2> <!-- Shows just a message after it has been checked that the login is not correct -->
    <?php endif; ?>
<?php endif; ?>

<script>
    document.getElementById('loginForm')?.addEventListener('submit', function(event) {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;

        if (username.trim() === '' || password.trim() === '') {
            alert('Both fields are required.');
            event.preventDefault();
        }
    });
</script>
</body>
</html>
