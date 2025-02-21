<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); // Allow all origins
header('Access-Control-Allow-Methods: POST, GET, OPTIONS'); // Allow specific methods
header('Access-Control-Allow-Headers: Content-Type'); // Allow specific headers


// All the headers we need to allow, if not we will get an error

// Get data from POST
$requestData = file_get_contents('php://input');

$data = json_decode($requestData, true);

if (isset($data['timestamp'])) {
    $timestamp = $data['timestamp'];
    $weekday = date('l', $timestamp);
    $response = [
        'weekday' => $weekday
    ];
    echo json_encode($response);
} else {
    echo json_encode(['error' => 'No timestamp provided']);
}
?>