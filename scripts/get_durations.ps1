$shell = New-Object -COMObject Shell.Application
$folder = $shell.Namespace('C:\Users\manet\Downloads')
$files = Get-ChildItem 'C:\Users\manet\Downloads' -Filter *.mp3 | Sort-Object LastWriteTime -Descending

foreach ($f in $files) {
    $item = $folder.ParseName($f.Name)
    $duration = $folder.GetDetailsOf($item, 27)
    [PSCustomObject]@{
        Time = $f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        Duration = $duration
        Size = $f.Length
        Name = $f.Name
    } | Format-Table -AutoSize
}
