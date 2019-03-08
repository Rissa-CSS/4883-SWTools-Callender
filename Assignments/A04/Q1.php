
<?php

/*
Course: CMPS 4883
Assignemt: A04
Date: 3/01/19
Github username: Rissa-CSS
Repo url: https://github.com/Rissa-CSS/4883-SWTools-Callender/tree/master/Assignments/A04
Name: Clorissa Callender
Description: 
    To calculate NFL stats using SQL queries and display the results using PHP.

*/
//Connect to mysql
$host = "localhost";             // because we are ON the server
$user = "***********";        // user name


$password = "**********";         // password 
$database = "******";              // database 
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

// SQL query that gets the top 10 the player IDs, names and the # of teams they played for.
$sql = "SELECT id,  name, count( DISTINCT(club)) as Teams FROM `players` 
        GROUP BY id ORDER By Teams desc limit 10";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

echo "<pre>";   // so whitespace matters

// Prints the results in a table
echo "\n\nQuestion 1 \n\n";
echo "# \t PlayerID \t Name \t\t\t # Teams \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        // variable that numbers the output
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['id']} \t {$row['name']} \t\t {$row['Teams']} \n";
    }
}


//Finds the top 5 rushing players per year

$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Yards 
        from players_stats join players on players.id=players_stats.playerid 
        where statid = 10 group by playerid, season order by Yards desc limit 5";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 2 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Yards']} \n";
    }
}


//Finds the bottom 5 passing players per year.
$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Passes 
        FROM `players_stats` join players on players.id=players_stats.playerid 
        WHERE statid = 15 group by playerid, season order by Passes limit 5";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 3 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Passes']} \n";
    }
}

//Finds the top 5 players that had the most rushes for a loss.
$sql = "SELECT players_stats.playerid, players.name, players_stats.season, sum(players_stats.yards) as Yards 
        FROM `players_stats` join players on players.id=players_stats.playerid 
        WHERE statid = 10 and yards <0 group by playerid order by Yards asc limit 5";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 4 \n\n";
echo "# \t PlayerID \t Name \t\t Year \t Yards \n";
echo "==========================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['playerid']} \t {$row['name']} \t {$row['season']} \t {$row['Yards']} \n";
    }
}

//Finds the top 5 teams with the most penalties
$sql = "SELECT club, sum(pen) as Total from game_totals group by club order by Total desc LIMIT 5";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 5 \n\n";
echo "# \tTeam Name \t Penalties \n";
echo "=======================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['club']} \t\t  {$row['Total']} \n";
    }
}

//Finds the average number of penalties per year.
$sql = "SELECT season, count(pen) as TotalGames, sum(pen) as TotalPen,  count(pen)/sum(pen) as AvgPen
        FROM game_totals GROUP BY season";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 6 \n\n";
echo "# \tYear \tTotal Penalties \tAvg Penalties\n";
echo "======================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['season']} \t\t  {$row['TotalGames']} \t\t {$row['AvgPen']} \n";
    }
}

//Finds the Team with the least amount of average plays every year.
$sql = "SELECT season,count(distinct(gameid)) As Games, count(playid) as Plays, clubid, (count(playid)/count(distinct(gameid))) As Average 
        FROM `plays` NATURAL Join games group by season, clubid order by Average limit 10";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 7 \n\n";
echo "# \tTeam \t\tSeason \t\tAvg Plays\n";
echo "======================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['season']} \t\t  {$row['clubid']} \t\t {$row['Average']} \n";
    }
}

//Finds the top 5 players that had field goals over 40 yards.
$sql = "SELECT count(yards) as Yards, playerid , name,players_stats.season
        FROM `players_stats` join players on players.id=players_stats.playerid
         WHERE statid = 70 and yards > 40 
        group by playerid order by yards desc limit 5";

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 8 \n\n";
echo "# \tPlayer ID \tPlayer Name \tSeason \t# of Field Goals\n";
echo "==============================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Yards']} \n";
    }
}

//Find the top 5 players with the shortest avg field goal length.
$sql = "SELECT count(yards) as NumYards,  name,sum(yards) as SumYards, playerid , players_stats.season, (count(yards)/sum(yards)) as Average 
        FROM `players_stats` join players on players.id = players_stats.playerid WHERE statid = 70  
        group by playerid order by Average limit 5";
// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table
echo "\n\nQuestion 9 \n\n";
echo "# \tPlayer ID \tPlayer Name \tSeason \t Average Field Goal\n";
echo "==============================================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['playerid']}  \t{$row['name']}\t {$row['season']}\t   {$row['Average']} \n";
    }
}
//Ranks the NFL by win loss percentage (worst first).

$sql = 'SELECT club, wonloss, sum(if(STRCMP(wonloss,"won")=0, 1,0)) as Wins, sum(if(STRCMP(wonloss,"loss")=0, 1,0)) as Loss, sum(if(STRCMP(wonloss,"won")=0, 1,0))/sum(if(STRCMP(wonloss,"loss")=0, 1,0)) as WinLossPer 
        FROM `game_totals` GROUP by club order by WinLossPer';

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table 
echo "\n\nQuestion 10 \n\n";
echo "Rank \tTeam Name \tWin/Loss \n";
echo "===================================================\n";
$count =33;
if($response['success']){
    foreach($response['result'] as $row){
        //Calculate the ranking of teams
        $count--;
        // Prints each row in the result table
        echo "$count \t {$row['club']}  \t\t{$row['WinLossPer']} \n";
    }
}

//Most common last name

$sql = 'SELECT name FROM `players` group by id';

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table 
echo "\n\nQuestion 11 \n\n";
echo "# \tLast Name \t Occurences \n";
echo "======================================================\n";
$count =0;
#Array for the last names
$lastnames=[];
if($response['success']){
    foreach($response['result'] as $row){
        
        #Separates the last name from the first inital
        $name =  explode(".",$row['name']);
        #Places last name in a variable
        $ln = $name[1];
        #Checks to see if the name in in the array already
        if (!array_key_exists($ln,$lastnames) )
            #Creates a key with the last name
            $lastnames[$ln] = 1;
        else 
            #Increments the occurence counter by 1
            $lastnames[$ln]++;
    }
}

# Reverse Sorts the array of lastnames by the # of occurences
arsort($lastnames);
#Gets the 5 most common last names
$mostcommon = array_slice($lastnames, 0, 5, true);
#Prints the 5 most common last names
foreach($mostcommon as $name => $occurence){
    #Increments the counter for the listings
    $count++;
    #Prints results
    echo"$count \t $name \t   $occurence \n";
}


//Gives the overall away win %

$sql = 'SELECT count(away_club) as AwayGames ,sum(if(STRCMP( win_type,"away" )=0, 1,0)) as AwayWins, away_club, sum(if(STRCMP( win_type,"away" )=0, 1,0))/count(away_club) as AwayWinPer FROM `games` group by away_club';

// Call the function to execute the query
$response = runQuery($mysqli, $sql);

// Prints the results in a table 
echo "\n\nBonus Question 3\n\n";
echo "# \tTeam \t\tAway % \n";
echo "=======================================\n";
$count =0;
if($response['success']){
    foreach($response['result'] as $row){
        //Calculate the ranking of teams
        $count++;
        // Prints each row in the result table
        echo "$count \t {$row['away_club']}  \t\t{$row['AwayWinPer']} \n";
    }
}

