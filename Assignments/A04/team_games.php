<?php
//Connect to mysql
$host = "localhost";             // because we are ON the server
$user = "software_tools";        // user name

// Get username and password from slack
// The DB username and pass not the ones
// I sent you to log into the server.
$password = "horseblanketdonkey";         // password 
$database = "nfl_data";              // database 
$mysqli = mysqli_connect($host, $user, $password, $database);

if (mysqli_connect_errno($mysqli)) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


/**
 * This function runs a SQL query and returns the data in an associative array
 * that looks like:
 * $response [
 *      "success" => true or false
 *      "error" => contains error if success == false
 *      "result" => associative array of the result
 * ]
 *
 */
function runQuery($mysqli,$sql){
    $response = [];

    // run the query
    $result = $mysqli->query($sql);

    // If we were successful
    if($result){
        $response['success'] = true;
        // loop through the result printing each row
        while($row = $result->fetch_assoc()){
            $response['result'][] = $row;
        }
        $result->free();
    }else{
        $response['success'] = false;
        $response['error'] = $mysqli->error;
    }

    return $response;
}


$sql = "SELECT * 
        FROM `games` 
        WHERE (`home_club` = 'DAL' or `away_club` = 'DAL') 
        AND season = '2018'";

$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters

if($response['success']){
    foreach($response['result'] as $row){
        echo "{$row['season']} {$row['home_club']}:{$row['home_score']}  {$row['away_club']}:{$row['away_score']} {$row['winner']} {$row['win_type']} \n";
    }
}