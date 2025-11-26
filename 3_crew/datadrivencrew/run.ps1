$bytes = [System.Text.Encoding]::UTF8.GetBytes('{"user_input":"Test depuis CLI"}')
$base64 = [System.Convert]::ToBase64String($bytes)
uv run python -m datadrivencrew.run_from_db --crew-code DataDrivenCrew --input-json $base64
