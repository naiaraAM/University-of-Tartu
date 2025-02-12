<?php

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User input</title>
</head>
<body>
<h1>Introduce the requested information</h1>
<form action="user_and_pass.php" method="post">
    <label for="username">Username:</label><br>
    <input type="text" id="username" name="username"><br>
    <label for="password">Password:</label><br>
    <input type="password" id="password" name="password"><br><br>
    <input type="submit" value="Login">
</body>



<script>
    const button = document.querySelector('input[type="submit"]');
    button.addEventListener('click', () => {
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;
        // Check if username is empty
        if (username === '' || username === null) {
            alert('Username is empty');
        }
        // Check if password is empty
        if (password === '' || password === null) {
            alert('Password is empty');
        }
        if (username === 'user' && password === 'pass' {
            document.cookie("username=user", expires=Thu, 01 Jan 1970 00:00:00 UTC);
        })

    });
</script>
</html>
