$bytes = [System.Text.Encoding]::UTF8.GetBytes('{"user_input":"Explique à un étudiant débutant ce qu est une classe abstraite en C# avec un exemple."}')
$base64 = [System.Convert]::ToBase64String($bytes)
#uv run python -m datadrivencrew.run_from_db --crew-code DataDrivenCrew --input-json $base64
uv run python -m datadrivencrew.run_from_db --crew-code TestInputCrew --input-json $base64
