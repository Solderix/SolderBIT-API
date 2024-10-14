$vendorID = "303A"
$productID = "4001"

$comPorts = Get-WMIObject Win32_PnPEntity | Where-Object {
    $_.Name -match "COM" -and $_.DeviceID -match "VID_$vendorID&PID_$productID"
}

foreach ($port in $comPorts) {
    if ($port.Name -match "COM\d+") {
        $comPort = $matches[0] 
        Write-Host "Device found on port: $comPort"
        ampy --port $comPort put .\main.py
        return
    }
}

if ($comPorts.Count -eq 0) {
    Write-Host "No COM ports found with VendorID: $vendorID and ProductID: $productID"
}