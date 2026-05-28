# update_pages.ps1
# This script propagates the latest header, footer, head elements, and scripts from index.html to all other pages.

# 1. Read the source of truth (index.html)
$indexContent = Get-Content "index.html" -Raw

# 2. Extract Header (Top Bar + Nav)
if ($indexContent -match "(?s)(<!-- TOP BAR -->.*?<header.*?</header>)") {
    $header = $Matches[1]
} else {
    Write-Error "Could not find Header in index.html"
    exit
}

# 3. Extract Footer
if ($indexContent -match "(?s)(<footer.*?</footer>)") {
    $footer = $Matches[1]
} else {
    Write-Error "Could not find Footer in index.html"
    exit
}

# 4. Extract Head Elements (Styles, Fonts, Tailwind)
# We look for the block between the first preconnect and the end of the style tag
if ($indexContent -match "(?s)(<link rel=`"preconnect`".*?</style>)") {
    $headElements = $Matches[1]
} else {
    Write-Error "Could not find Head Elements in index.html"
    exit
}

# 5. Extract Script
if ($indexContent -match "(?s)(<script>.*?</script>)") {
    # Get the last script tag which contains our logic
    $scripts = [regex]::Matches($indexContent, "(?s)<script>.*?</script>")
    $script = $scripts[$scripts.Count - 1].Value
} else {
    Write-Error "Could not find Script in index.html"
    exit
}

# 6. Get all other HTML files
$files = Get-ChildItem "snapticle-media-*.html"

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # Update Head Elements
    # We replace everything between the first preconnect/link and the end of style, or just insert before </head>
    if ($content -match "(?s)<link rel=`"preconnect`".*?</style>") {
        $content = $content -replace "(?s)<link rel=`"preconnect`".*?</style>", $headElements
    } elseif ($content -match "</head>") {
        $content = $content -replace "</head>", "$headElements`n</head>"
    }

    # Update Header
    # Replace from body start until the end of the first <header> or <nav>
    if ($content -match "(?s)<body[^>]*>.*?<header.*?</header>") {
        $content = $content -replace "(?s)<body[^>]*>.*?<header.*?</header>", "<body>`n$header"
    } elseif ($content -match "(?s)<body[^>]*>.*?<nav.*?</nav>") {
        $content = $content -replace "(?s)<body[^>]*>.*?<nav.*?</nav>", "<body>`n$header"
    } elseif ($content -match "<body[^>]*>") {
        $content = $content -replace "(<body[^>]*>)", "`$1`n$header"
    }

    # Update Footer
    if ($content -match "(?s)<footer.*?</footer>") {
        $content = $content -replace "(?s)<footer.*?</footer>", $footer
    } elseif ($content -match "</body>") {
        $content = $content -replace "</body>", "$footer`n</body>"
    }

    # Update Script
    # Remove existing toggleSubmenu scripts to avoid duplicates, then insert the latest one before </body>
    if ($content -match "(?s)<script>.*?toggleSubmenu.*?</script>") {
        $content = $content -replace "(?s)<script>.*?toggleSubmenu.*?</script>", $script
    } elseif ($content -match "</body>") {
        $content = $content -replace "</body>", "$script`n</body>"
    }

    # Final cleanup: Ensure body class is consistent if needed
    $content = $content -replace "<body", "<body class=`"bg-gray-50`""

    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Successfully updated $($files.Count) pages with latest Header, Footer, and Scripts from index.html!"
