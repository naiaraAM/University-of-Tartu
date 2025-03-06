<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Reflected name</title>
    </head>
    <body>
        <form method="GET" action="">
            <label>Enter your name:</label>
            <label>
                <input type='text' name='name' value='<?php echo htmlspecialchars($_GET['name'] ?? '', ENT_QUOTES); ?>'>
            </label>
            <input type='submit'>
        </form>
        <h1 id="name"></h1>

        <script>
            var name = '<?php echo json_encode($_GET['name'] ?? ''); ?>';
            if (name) {
                document.getElementById("name").innerHTML = 'Your name is: ' + name;
            }
        </script>


        <?php
        if (isset($_GET['name']) && strlen($_GET['name'])) {

            echo "<script>alert('Dear ".htmlspecialchars($_GET['name'], ENT_QUOTES).", welcome to our website!');</script>\n";

        }
        ?>
    </body>
</html>
