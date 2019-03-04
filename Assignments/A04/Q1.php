
<?php
             // database 
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


$sql = "SELECT id,  name, count( DISTINCT(club)) as Teams FROM `players` 
        GROUP BY id ORDER By Teams desc limit 10";


$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters


echo "\n\nQuestion 1 \n\n";
echo "# \t PlayerID \t Name \t\t\t # Teams \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['id']} \t {$row['name']} \t\t {$row['Teams']} \n";
    }
}



$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Yards 
        from players_stats join players on players.id=players_stats.playerid 
        where statid = 10 group by playerid, season order by Yards desc limit 5";


$response = runQuery($mysqli, $sql);


//echo "<pre>";   // so whitespace matters
echo "\n\nQuestion 2 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Yards']} \n";
    }
}



$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Passes 
        FROM `players_stats` join players on players.id=players_stats.playerid 
        WHERE statid = 15 group by playerid, season order by Passes limit 5";


$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 3 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Passes']} \n";
    }
}


$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Yards 
        FROM `players_stats` join players on players.id=players_stats.playerid 
        WHERE statid = 10 and yards <0 group by playerid order by Yards asc limit 5";


$response = runQuery($mysqli, $sql);

echo "\n\nQuestion 4 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Yards']} \n";
    }
}


$sql = "SELECT club, sum(pen) as Total from game_totals group by club order by Total desc LIMIT 5";


$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 5 \n\n";
echo "# \tTeam Name \t Penalties \n";
echo "=======================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['club']} \t\t  {$row['Total']} \n";
    }
}


$sql = "SELECT season, count(pen) as TotalGames, sum(pen) as TotalPen,  count(pen)/sum(pen) as AvgPen
        FROM game_totals GROUP BY season";


$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 6 \n\n";
echo "# \tYear \tTotal Penalties \tAvg Penalties\n";
echo "======================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['season']} \t\t  {$row['TotalGames']} \t\t {$row['AvgPen']} \n";
    }
}

$sql = "SELECT season,count(distinct(gameid)) As Games, count(playid) as Plays, clubid, (count(playid)/count(distinct(gameid))) As Average 
        FROM `plays` NATURAL Join games group by season, clubid order by Average limit 10";


$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 7 \n\n";
echo "# \tTeam \t\tSeason \t\tAvg Plays\n";
echo "======================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['season']} \t\t  {$row['clubid']} \t\t {$row['Average']} \n";
    }
}

$sql = "SELECT count(yards) as Yards, playerid , name,players_stats.season
        FROM `players_stats` join players on players.id=players_stats.playerid
         WHERE statid = 70 and yards > 40 
        group by playerid order by yards desc limit 5";

$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 8 \n\n";
echo "# \tPlayer ID \tPlayer Name \tSeason \t# of Field Goals\n";
echo "==============================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Yards']} \n";
    }
}

$sql = "SELECT count(yards) as NumYards,  name,sum(yards) as SumYards, playerid , players_stats.season, (count(yards)/sum(yards)) as Average 
        FROM `players_stats` join players on players.id = players_stats.playerid WHERE statid = 70  
        group by playerid order by Average limit 5";

$response = runQuery($mysqli, $sql);


echo "\n\nQuestion 9 \n\n";
echo "# \tPlayer ID \tPlayer Name \tSeason \t Average Field Goal\n";
echo "==============================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        echo "$count \t {$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Average']} \n";
    }
}

$sql = "SELECT count(winner) As wins, home_club from games group by (winner)";


$response = runQuery($mysqli, $sql);
$wins = array();
echo "\n\nQuestion 10 \n\n";
echo "# \tPlayer ID \tPlayer Name \tSeason \t Average Field Goal\n";
echo "==============================================================\n";
$count =0;
if($response['success']){
foreach($response['result'] as $row){
    $wins[{$row['home_club']} ] ={$row['wins']} ;
$count++;
//echo "$count \t {$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Average']} \n";
}
}
/*
for ($i=1;$i<$count;$i++){
    echo "$wins[$i]\n";
}*/