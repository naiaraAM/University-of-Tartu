<html>
<head>
    <title>Multiple Attacks</title>
    <script>
        function startDownload() {
            var downloadLink = document.createElement("a");
            downloadLink.href = "suspicious-file.exe";
            downloadLink.download = "suspicious-file";
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        }

        document.addEventListener("DOMContentLoaded", function(){
            startDownload();

            setTimeout(function(){
                var msg = new SpeechSynthesisUtterance("Multiple Attacks, surprise!");
                window.speechSynthesis.speak(msg);
                window.print();
            }, 1000);
        });

        function buttonClick() {
            navigator.clipboard.writeText("This is your newest clipboard content");

            var popup = window.open("", "popup", "width=200,height=200,left=0,top=0");
            if (popup) {
                popup.opener = null;

                popup.document.open();
                popup.document.write('<html><head><title>Popup</title></head><body>');
                popup.document.write('<h1>Click anywhere to show Clipboard content</h1>');
                popup.document.write('</body></html>');
                popup.document.close();

                popup.onclick = function() {
                    navigator.clipboard.readText().then(function(text) {
                        popup.document.body.innerHTML = "<h3>Clipboard content:</h3><p>" + text + "</p>";
                    });
                };

                // Mover continuamente el popup usando un intervalo
                setInterval(function(){
                    var x = popup.screenX + Math.floor(Math.random() * 100) - 50;
                    var y = popup.screenY + Math.floor(Math.random() * 100) - 50;
                    try {
                        popup.moveTo(x, y);
                    } catch(e) {
                        console.error("Error al mover el popup:", e);
                    }
                }, 500);
            }
        }
    </script>
</head>
<body>
    <h1>Multiple Attacks</h1>
    <button onclick="buttonClick()">Click here, nothing bad is going to happen :)</button>
</body>
</html>