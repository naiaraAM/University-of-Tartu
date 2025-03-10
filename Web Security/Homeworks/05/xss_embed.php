<?php
$scriptNonce = base64_encode(random_bytes(16));
$styleNonce = base64_encode(random_bytes(16));

header("Content-Security-Policy: " .
    "default-src 'none'; " .  // Deny everything by default
    "script-src 'self' 'nonce-{$scriptNonce}' 'strict-dynamic'; " .
    "style-src 'self' 'nonce-{$styleNonce}'; " .
    "base-uri 'none'; " .
    "frame-src 'self' https://websec.ee; ");
?>
<!DOCTYPE html>
<html lang="en">
    <body>
    <iframe
        src="https://websec.ee/xss/csp_hardening1.php"
        sandbox="allow-scripts allow-same-origin"
        referrerpolicy="no-referrer"
        height="1000px"
        width="1000px">
    </iframe>
    </body>
</html>