<!DOCTYPE html>
<html>
  <head>
    <title>College Crush Results</title>
    <link rel="stylesheet" type="text/css" href="/styles/site.css">
  </head>
  <body>
    <h1>College Crush Results</h1>
    
    <?php
    // Get the form data using the POST method
    $location = $_POST['location'];
    $major = $_POST['major'];
    $size = $_POST['size'];
    
    // Process the form data and display the results
    echo "<p>Based on your preferences, we recommend the following colleges:</p>";
    
    // TODO: Add code here to generate the recommended colleges based on the user's preferences
    // Using a database, API, or some other method to generate the results
    
    ?>
    
  </body>
</html>