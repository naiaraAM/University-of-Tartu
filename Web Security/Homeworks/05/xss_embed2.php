<?php
$scriptNonce = base64_encode(random_bytes(16));
$styleNonce = base64_encode(random_bytes(16));

header("Content-Security-Policy: " .
    "default-src 'none'; " .
    "script-src 'nonce-{$scriptNonce}'; " .
    "style-src 'nonce-{$styleNonce}'; " .
    "frame-src https://websec.ee; " .
    "base-uri 'none'; " .
    "frame-ancestors 'self'; " .
    "object-src 'none'; " .
    "connect-src https://websec.ee; " .
    "img-src 'none'; " .
    "form-action 'none'; " .
    "navigate-to 'none'; " .
    "require-trusted-types-for 'script'; ");
?>
<!DOCTYPE html>
<html lang="en">
<body>
<iframe
        src="https://websec.ee/xss/csp_hardening2.php"
        sandbox="allow-scripts allow-same-origin"
        referrerpolicy="no-referrer"
        height="1000px"
        width="1000px">
</iframe>
</body>
</html>