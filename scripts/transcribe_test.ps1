Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class AudioChecker {
    // We can use standard COM Media Foundation or ACM to decode MP3
}
"@
Write-Host "AudioChecker loaded"
