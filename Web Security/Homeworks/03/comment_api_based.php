<?php

$db = new SQLite3('.comments.sqlite', SQLITE3_OPEN_CREATE | SQLITE3_OPEN_READWRITE);
// Create a table.
$db->query('CREATE TABLE IF NOT EXISTS "comments" (
  "id" INTEGER PRIMARY KEY,
  "comment" VARCHAR,
  "ip" VARCHAR,
  "added" DATETIME
)');

function S($text) {
    return htmlspecialchars($text, ENT_QUOTES);
}

// Check for custom header in POST requests
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_SERVER['HTTP_X_REQUESTED_WITH']) || $_SERVER['HTTP_X_REQUESTED_WITH'] !== 'FetchAPI') {
        header('HTTP/1.1 403 Forbidden');
        die('Invalid request');
    }

    $data = json_decode(file_get_contents('php://input'), true);
    if (isset($data['comment'])) {
        // Insert data
        $db->exec('BEGIN');
        $sql = 'INSERT INTO "comments" ("comment", "ip", "added") VALUES (?, ?, datetime("now","localtime"))';
        $statement = $db->prepare($sql);
        $statement->bindValue(1, substr($data['comment'], 0, 70));
        $statement->bindValue(2, $_SERVER['REMOTE_ADDR']);
        $statement->execute();
        $db->exec('COMMIT');

        header('Content-Type: application/json');
        echo json_encode(['status' => 'success']);
        exit;
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Write a comment</title>
    <script>
        async function submitComment(event) {
            event.preventDefault();
            const comment = document.getElementById('commentId').value;

            try {
                const response = await fetch('', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'FetchAPI'
                    },
                    body: JSON.stringify({ comment: comment })
                });

                if (response.ok) {
                    location.reload(); // Reload to see new comment
                } else {
                    alert('Error submitting comment');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error submitting comment');
            }
        }
    </script>
</head>
<body>

<h1>Write a comment</h1>
<textarea id="commentId" name="comment" placeholder="Add your comment..." rows="3" cols="30"></textarea>
<form id="commentForm" onsubmit="submitComment(event)">
    <input type="submit" value="Add">
</form>
<h2>Comments</h2>
<ul>
    <?php

    $statement = $db->prepare('SELECT * FROM "comments" ORDER BY "added" DESC LIMIT 30');
    $result = $statement->execute();
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        echo '<li>['.S($row['added']).'] ('.S($row['ip']).') '.S($row['comment']).'</li>';
        echo "\n";
    }

    $db->close();

    ?>
</ul>

</body>
</html>