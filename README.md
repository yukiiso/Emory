# Emory
AI-powered counseling assistant with emotion visualization and conversation summarization. Users interact with a pre-talk system, while counselors receive non-verbal insights without recording conversations. Features include avatar-based mood tracking, a public/private mode, and a counselor dashboard for intervention timing.


# セットアップコマンド
```
docker compose --env-file config.env up --build -d
```

立ち上げ直し時コピペ用: 
```
docker compose --env-file config.env down --volumes 
docker compose --env-file config.env up --build -d
```

