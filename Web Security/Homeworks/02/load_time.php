<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Show time</title>
    </head>
    <body>
        <iframe id="hiddenIframe" src="time.php" hidden></iframe>
        <button id="showTime">Click me</button>
        <span id="time"></span>
    </body>
    <script>
        document.getElementById('showTime').addEventListener('click', function() {
            const iframe = document.getElementById('hiddenIframe'); // Get local iframe
            const iframeDocument = iframe.contentDocument || iframe.contentWindow.document; // Get the document of the iframe
            const time = iframeDocument.getElementById('time').textContent; // Because we know the id of the element
            document.getElementById('time').textContent = time; // Set the time to the local element
        });
    </script>
</html>